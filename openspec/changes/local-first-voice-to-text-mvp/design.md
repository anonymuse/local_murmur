## Context

This change introduces a privacy-focused MVP that records microphone audio, runs local speech recognition, optionally refines the transcript with a local LLM, and shows the result in a clean one-screen interface. The repository currently has no product code, so the design needs to establish a simple architecture that supports local model providers without adding persistence or complex infrastructure.

## Goals / Non-Goals

**Goals:**

- Deliver an end-to-end local-first transcription flow.
- Keep audio, transcripts, and model outputs transient by default.
- Support open source local ASR and local LLM backends through a small adapter layer.
- Provide a polished, minimal interface that is comfortable to use repeatedly.

**Non-Goals:**

- No user accounts, authentication, or sharing.
- No database, history view, or saved transcript library.
- No multi-device sync or cloud fallback.
- No advanced editing workflow beyond copy, clear, and restart.

## Decisions

### 1. Use a local web app with a small local backend
The MVP should be implemented as a browser-based UI backed by a local service that orchestrates transcription. This keeps the interface easy to polish while making it straightforward to call local ASR and LLM processes.

Alternatives considered:

- Pure browser-only app: rejected because local model execution and provider orchestration become awkward and brittle.
- Full desktop shell first: rejected for MVP because packaging and cross-platform distribution add overhead before the core workflow is validated.

### 2. Keep audio and transcript state ephemeral
All session state should live in memory for the duration of the active run. If a temporary file is required to hand audio to an ASR engine, it should be created in a temp location and deleted immediately after use.

Alternatives considered:

- Persisting local transcripts to disk: rejected because it is not needed for MVP and weakens the no-persistence requirement.
- Structured local cache: rejected for the same reason.

### 3. Use provider adapters for ASR and LLM integrations
The backend should expose a narrow interface for ASR and LLM providers rather than binding the app to a specific tool. This lets the MVP support Vibe Voice or similar local ASR options and Ollama or LocalLM-style providers without changing the UI contract.

Alternatives considered:

- Hard-coding one provider: rejected because it makes the MVP less adaptable and risks lock-in to a single local setup.
- Dynamic plugin architecture: rejected as too much complexity for the first release.

### 4. Make transcript refinement optional and non-blocking
Refinement should be an opt-in post-processing step. If the local LLM is unavailable or the user disables it, the raw ASR transcript should still be returned.

Alternatives considered:

- Always refine: rejected because it adds latency and a second failure mode to the core flow.
- Remove refinement entirely: rejected because local LLM cleanup is a key differentiator in the product idea.

### 5. Design the UI around one primary action
The interface should foreground a single record button, a clear recording state, the live or final transcript, and lightweight actions like copy and reset. This keeps the experience approachable and supports the "beautiful and simple" goal.

Alternatives considered:

- Multi-pane editor layout: rejected because it shifts attention away from the primary capture flow.
- Dense settings-first interface: rejected because the MVP should feel immediate, not configurable-heavy.

## Risks / Trade-offs

- [Local model startup latency] → Show explicit loading and processing states, and keep the workflow to one request per recording.
- [Microphone permission or browser support issues] → Surface a friendly error path and keep capture controls obvious.
- [Provider variability across local environments] → Hide provider-specific details behind adapters and document one known-good default configuration.
- [No persistence means no recovery after refresh] → Make the transient nature explicit in the UI so users are not surprised when sessions disappear.

## Migration Plan

1. Ship the new local MVP as a separate flow with no migration from existing data because none is stored.
2. Wire the UI to the local backend and confirm audio capture, transcription, and optional refinement end-to-end.
3. Validate behavior with the default ASR and LLM providers, then document the local setup steps.
4. If issues arise, roll back by disabling the new flow; there is no data migration or restore step.

## Open Questions

- Which local ASR backend should be the default reference implementation for the MVP?
- Should transcript refinement be off by default or enabled via a visible toggle?
- Do we want a pure web app for MVP delivery, or should we wrap it in a desktop shell after the flow is validated?
