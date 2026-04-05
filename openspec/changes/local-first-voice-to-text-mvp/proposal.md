## Why

People need a fast, private way to turn spoken ideas into text without sending audio or transcripts to a cloud service. This MVP proves that we can deliver a clean local-first experience with open source ASR and a local LLM while keeping the product simple and disposable.

## What Changes

- Add a local-first voice-to-text MVP that records microphone audio and produces transcript text entirely on-device or on the user's machine.
- Use an open source ASR engine for transcription, with the implementation able to support options such as Vibe Voice or similar local models.
- Optionally run transcript cleanup, punctuation, or light rewriting through a local LLM provider such as Ollama or LocalLM.
- Provide a beautiful, simple interface focused on one primary flow: record, transcribe, review, and copy.
- Do not add persistence for MVP; audio, transcripts, and derived outputs are transient unless the user manually copies them elsewhere.

## Capabilities

### New Capabilities

- `local-voice-to-text-mvp`: End-to-end local voice capture, offline transcription, optional local LLM post-processing, and a minimal polished UI for reviewing results.

### Modified Capabilities

None.

## Impact

- Adds a new end-to-end product flow and supporting local ASR / local LLM integrations.
- Likely introduces UI, audio capture, model orchestration, and clipboard/export handling code.
- Avoids database or long-term storage work for the MVP.
