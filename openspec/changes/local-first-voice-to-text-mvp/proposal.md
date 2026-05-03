## Why

People need a fast, private way to turn spoken ideas into polished text without defaulting to a cloud dictation service. Local Murmur proves the core OpenAI/Codex-oriented stack: user-provided audio goes to a local FastAPI backend, Faster-Whisper produces raw text, and an optional LLM post-processor cleans punctuation, filler words, proper nouns, paragraphing, and light clarity while preserving the speaker's voice.

## What Changes

- Add a local-first voice-to-text MVP that accepts an audio recording through a browser test UI or `curl` and returns transcript text.
- Use Faster-Whisper with Whisper Large-v3-Turbo as the MVP ASR reference implementation.
- Run optional transcript cleanup through Ollama by default, with OpenAI API as the only optional cloud LLM provider for this repository.
- Dockerize the backend for WSL-based local development first, with a later path to Unraid deployment.
- Provide a simple interface focused on one primary flow: upload or record, transcribe, review, and copy.
- Do not add persistence for MVP; audio, transcripts, and derived outputs are transient unless the user manually copies them elsewhere.

## Capabilities

### New Capabilities

- `local-voice-to-text-mvp`: End-to-end audio ingestion, local Faster-Whisper transcription, optional Ollama or OpenAI post-processing, and a minimal review surface for raw and cleaned results.

### Modified Capabilities

None.

## Impact

- Adds a new end-to-end product flow and supporting ASR / LLM integrations.
- Introduces a FastAPI backend, Docker configuration for WSL development, a browser test UI, audio upload handling, model orchestration, and clipboard/export handling code.
- Avoids database or long-term storage work for the MVP.
