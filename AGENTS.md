# Local Murmur Agent Guide

## Project Identity

Local Murmur is the OpenAI/Codex-oriented implementation of a self-hosted speech-to-text platform. It pairs a local ASR layer with LLM post-processing to produce dictation-quality text from user-provided audio.

Use the product name `Local Murmur` in user-facing documentation. Avoid older placeholder names such as `voice_to_text`, `local_whisper`, or `OpenDictate` unless referring to historical context.

## Development Approach

- Use planning before coding sessions, especially before architecture or implementation changes.
- Work one phase at a time and keep the user oriented with concise explanations.
- Prefer the OpenSpec workflow for product and architecture changes before implementation.
- Make architectural decisions with security, efficiency, and future cloud portability in mind.
- Codex is the development agent. It is not a runtime LLM provider.
- Runtime cloud LLM support in this repository should use the OpenAI API, not Anthropic.

## Agent Collaboration Model

- The primary conversation agent acts as product owner and architect for this project.
- CLI coding agents may implement scoped changes after the OpenSpec plan is agreed.
- Implementation agents should propose their plan before making large changes.
- The product owner / architect should review suggested implementation plans, diffs, and tradeoffs before the project changes direction.
- Keep architecture, scope, provider choices, and privacy guarantees aligned with the OpenSpec documents.
- Coding work should stay inside the active phase unless the user explicitly expands scope.

## MVP Architecture

The MVP target is a fast functional path:

1. Accept an audio recording through a browser test UI or `curl`.
2. Send the recording to a FastAPI backend.
3. Transcribe with Faster-Whisper.
4. Optionally post-process with an LLM.
5. Return raw and cleaned transcript text as JSON.

The first deployment target is Docker running inside WSL on the Windows workstation. The FastAPI container should be able to call an Ollama server running on the Windows host with the RTX 5080 Founders Edition.

The later self-hosted target is Unraid running the frontend/gateway containers while calling GPU-backed inference services on the Windows workstation over LAN or Tailscale. The Unraid server is not assumed to have a suitable GPU for ASR or LLM inference.

## Provider Defaults

- ASR: Faster-Whisper with Whisper Large-v3-Turbo, running on the Windows GPU host for the first working path.
- Default LLM provider: Ollama on the Windows host.
- Optional cloud LLM provider: OpenAI API with a user-supplied API key.
- Disabled LLM mode must be supported so raw ASR output can be returned without post-processing.

Do not add Anthropic provider support to this implementation unless the user explicitly reopens that scope.

## Privacy And Security Defaults

- Do not persist audio, transcripts, or model outputs for the MVP.
- Do not log transcript text or raw audio contents.
- Delete temporary audio artifacts on success and failure.
- Do not use browser localStorage or sessionStorage for sensitive transcript/audio data.
- Treat OpenAI API use as explicit cloud processing only when configured by the user.
- For self-hosted access, assume Tailscale or a private LAN is the network boundary.

## Roadmap Boundaries

The MVP should prioritize backend core plus a simple browser/curl client path. Windows Tauri, iOS, iOS keyboard extension, cloud SaaS, and on-device iOS are roadmap phases unless the user explicitly moves one into the active phase.
