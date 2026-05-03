## 1. Project Foundation

- [ ] 1.1 Scaffold the FastAPI backend with `/health` and `/transcribe`.
- [ ] 1.2 Add Docker and Docker Compose support for WSL development.
- [ ] 1.3 Add configuration validation for Faster-Whisper, Ollama, OpenAI, max audio duration, and temp-file handling.
- [ ] 1.4 Document how WSL Docker reaches Windows-hosted Ollama.

## 2. Capture and Transcription

- [ ] 2.1 Implement audio upload handling for `wav`, `m4a`, `aac`, and other explicitly supported MVP formats.
- [ ] 2.2 Validate file type and duration before transcription.
- [ ] 2.3 Implement ffmpeg conversion where required before ASR.
- [ ] 2.4 Implement the Faster-Whisper adapter using Whisper Large-v3-Turbo.
- [ ] 2.5 Return raw transcript and duration metadata from `/transcribe`.
- [ ] 2.6 Delete temporary audio artifacts immediately after transcription completes or fails.

## 3. Local LLM Refinement

- [ ] 3.1 Implement `LLM_PROVIDER=none`, `LLM_PROVIDER=ollama`, and `LLM_PROVIDER=openai`.
- [ ] 3.2 Make Ollama the default provider and support `OLLAMA_BASE_URL` plus `OLLAMA_MODEL`.
- [ ] 3.3 Add OpenAI API support with `OPENAI_API_KEY` and `OPENAI_MODEL`.
- [ ] 3.4 Implement the post-processing prompt for punctuation, filler word removal, proper nouns, paragraph breaks, and light clarity.
- [ ] 3.5 Ensure raw ASR output still returns when refinement is disabled or unavailable.

## 4. Browser And Curl Client Path

- [ ] 4.1 Provide a documented `curl` example that posts an m4a or wav file to `/transcribe`.
- [ ] 4.2 Build a minimal browser upload UI with transcript viewer, raw transcript viewer, copy action, and reset action.
- [ ] 4.3 Add browser microphone recording only if it does not delay the upload-based MVP.
- [ ] 4.4 Add friendly loading and error states for upload, ASR, and LLM failures.

## 5. Verification

- [ ] 5.1 Add checks that confirm no audio or transcript data persists across refresh or app restart.
- [ ] 5.2 Verify temporary audio cleanup on success and ASR failure.
- [ ] 5.3 Verify logs do not contain raw transcript text, cleaned transcript text, or audio contents.
- [ ] 5.4 Verify raw transcript returns when Ollama is unavailable.
- [ ] 5.5 Verify OpenAI is never called unless `LLM_PROVIDER=openai` is explicitly configured.
- [ ] 5.6 Perform an end-to-end smoke test in WSL Docker with Faster-Whisper and Windows-hosted Ollama.

## 6. Roadmap Deferrals

- [ ] 6.1 Capture Windows Tauri app as post-MVP.
- [ ] 6.2 Capture iOS app and keyboard extension as post-MVP.
- [ ] 6.3 Capture Unraid deployment packaging as the next self-hosted deployment step after WSL validation.
- [ ] 6.4 Capture cloud SaaS and on-device iOS as later phases.
