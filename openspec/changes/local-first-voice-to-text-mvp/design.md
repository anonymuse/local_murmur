## Context

This change introduces Local Murmur, a privacy-focused speech-to-text MVP for the OpenAI/Codex-oriented stack. The MVP accepts an audio recording, sends it to a local FastAPI backend, transcribes it with Faster-Whisper, optionally refines it with an LLM, and returns raw plus cleaned transcript text. The first target is Docker in WSL on the Windows workstation, using the RTX 5080 Founders Edition for Faster-Whisper and calling Ollama on the Windows host for the default LLM path.

## Goals / Non-Goals

**Goals:**

- Deliver an end-to-end local-first transcription flow.
- Keep audio, transcripts, and model outputs transient by default.
- Support Faster-Whisper as the reference ASR path for MVP.
- Support Ollama as the default LLM provider and OpenAI API as the only optional cloud provider in this repository.
- Provide a minimal browser/curl test path that is comfortable enough to validate repeated use.

**Non-Goals:**

- No user accounts, authentication, or sharing.
- No database, history view, or saved transcript library.
- No multi-device sync or automatic cloud fallback.
- No Anthropic provider support in this OpenAI-oriented implementation.
- No iOS, iOS keyboard extension, Windows Tauri app, SaaS, or on-device mode in the MVP implementation.
- No streaming transcript requirement; MVP transcription is batch-oriented after an upload or recording stops.
- No advanced editing workflow beyond copy, clear, and restart.

## Decisions

### 1. Use FastAPI as the single backend entry point
The MVP backend should expose a small FastAPI gateway with `/health` and `/transcribe`. All clients call the gateway; no client talks directly to Faster-Whisper, Ollama, or OpenAI. `/transcribe` accepts an audio upload, validates type and duration, writes a temporary artifact if needed, runs ASR, optionally runs post-processing, deletes temporary files, and returns JSON.

The response contract should include at least:

```json
{
  "transcript": "cleaned or raw transcript",
  "raw": "raw ASR transcript",
  "duration_seconds": 12.3,
  "post_processing_provider": "ollama"
}
```

Alternatives considered:

- Direct client-to-model calls: rejected because it scatters privacy, provider, and error-handling concerns across clients.
- Job queue and polling: rejected for MVP because configurable short dictation recordings can complete inside a synchronous HTTP response.

### 2. Target WSL Docker first, then Unraid gateway deployment
The first working environment should run the backend stack in Docker inside WSL on the Windows workstation. Faster-Whisper runs there with access to the Windows GPU through WSL/Docker GPU support, and the backend container calls Ollama on the Windows host. This proves the full flow near the RTX 5080 Founders Edition machine before introducing Unraid networking and deployment concerns.

The later self-hosted deployment runs frontend/gateway containers on Unraid and calls GPU-backed inference services on the Windows workstation over LAN or Tailscale. The Unraid server is not assumed to have a suitable GPU for ASR or LLM inference, so Unraid must not be required to run Faster-Whisper locally.

Alternatives considered:

- Unraid first: deferred because the fastest validation path is WSL Docker next to the Windows-hosted Ollama service.
- Desktop shell first: deferred because browser/curl validation is enough to prove the backend pipeline.

### 3. Lock the MVP reference ASR to Faster-Whisper
The ASR implementation should use Faster-Whisper with Whisper Large-v3-Turbo as the reference model. The implementation can keep a narrow ASR adapter interface, but MVP verification anchors to this one known-good path.

Alternatives considered:

- Multi-provider ASR support: deferred until the reference path works reliably.
- Browser-only ASR: rejected because local model execution and audio conversion are better handled in the backend for this MVP.

### 4. Route LLM post-processing through Ollama by default, OpenAI optionally
The LLM post-processor should support `LLM_PROVIDER=ollama`, `LLM_PROVIDER=openai`, and `LLM_PROVIDER=none`. Ollama is the default and points to the Windows host from WSL Docker. OpenAI API is available only when explicitly configured with a user-supplied API key. Anthropic is out of scope for this repository.

The post-processor should perform five cleanup behaviors:

- punctuation cleanup
- filler word removal
- proper noun correction when context supports it
- paragraph breaks
- light clarity improvements while preserving speaker voice

If post-processing is disabled or unavailable, the backend must still return the raw ASR transcript.

Alternatives considered:

- Always refine: rejected because it adds latency and a second failure mode to the core flow.
- Remove refinement entirely: rejected because local LLM cleanup is a key differentiator in the product idea.

### 5. Keep audio and transcript state ephemeral
All session state should live in memory for the duration of the active run. If a temporary file is required for ASR or conversion, it should be created in a temp location and deleted on success or failure.

The backend must not log raw audio, transcript text, or model outputs. The browser UI must not place audio or transcripts in `localStorage`, `sessionStorage`, IndexedDB, or service-worker caches. Manual copy is allowed and transfers control to the operating system clipboard.

Alternatives considered:

- Persisting local transcripts to disk: rejected because it is not needed for MVP and weakens the no-persistence requirement.
- Structured local cache: rejected for the same reason.

### 6. Design the first client around upload and optional browser recording
The first client surface should support uploading an audio file and displaying raw plus cleaned transcript text. Browser microphone recording can be added in the same MVP if it stays small, but the backend must be testable with `curl` against an m4a or wav file.

Alternatives considered:

- iOS first: deferred because keyboard extension and app distribution complexity should not block backend validation.
- Windows Tauri first: deferred until the backend contract is proven.

## Runtime Boundary

For WSL development, the backend should bind to loopback or a developer-selected local interface. The backend should call the Windows Ollama host through documented Docker/WSL networking configuration. For self-hosted deployment, clients reach the FastAPI gateway over Tailscale or private LAN. The gateway may run on Unraid later, but ASR and LLM inference should stay on the Windows GPU host unless another suitable GPU host is introduced. No public inbound port is required for Mode 1.

Cloud OpenAI calls are allowed only when `LLM_PROVIDER=openai` is explicitly configured. ASR remains Faster-Whisper in the MVP and must not call a remote transcription service.

## Configuration

Initial configuration should include:

```text
WHISPER_MODEL=large-v3-turbo
WHISPER_DEVICE=cuda
WHISPER_COMPUTE_TYPE=float16
MAX_AUDIO_DURATION_SECONDS=300

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=gemma4:e4b

OPENAI_API_KEY=
OPENAI_MODEL=
```

## Risks / Trade-offs

- [GPU and Docker passthrough complexity] -> Start with WSL Docker and document the known-good path before Unraid deployment.
- [Local model startup latency] -> Show explicit loading and processing states, and keep the workflow to one request per recording.
- [Ollama host connectivity] -> Validate `OLLAMA_BASE_URL` at startup or first request and return a clear error while preserving raw ASR output.
- [Provider variability] -> Anchor MVP verification to Faster-Whisper plus Windows Ollama, with OpenAI as an explicitly configured optional path.
- [No persistence means no recovery after refresh] -> Make the transient nature explicit in the UI so users are not surprised when sessions disappear.

## Migration Plan

1. Ship the new local MVP as a separate flow with no migration from existing data because none is stored.
2. Build and validate the FastAPI `/transcribe` pipeline through `curl` using a known m4a or wav file.
3. Add the browser upload/record test UI once the backend contract is stable.
4. Validate behavior with Faster-Whisper plus Windows-hosted Ollama from WSL Docker.
5. Document the path from WSL Docker to Unraid plus Windows Ollama over LAN or Tailscale.
6. If issues arise, roll back by disabling the new flow; there is no data migration or restore step.

## Open Questions

- Should ASR run in the same FastAPI container for MVP, or should the Docker shape start with a separable sidecar even if it is deployed together?
- Should the browser recording control be included in the first implementation pass, or should file upload plus `curl` be the first acceptance target?
- What is the exact known-good Windows Ollama model name for the first smoke test?
