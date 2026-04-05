## 1. Project Foundation

- [ ] 1.1 Scaffold the app shell and local backend structure for a browser UI plus a local orchestration service.
- [ ] 1.2 Add configuration for local ASR and local LLM providers, including temp-file handling for transient audio.

## 2. Capture and Transcription

- [ ] 2.1 Implement microphone capture and recording state handling in the UI.
- [ ] 2.2 Implement the local ASR adapter and transcription request flow for completed recordings.
- [ ] 2.3 Delete temporary audio artifacts immediately after transcription completes or fails.

## 3. Local LLM Refinement

- [ ] 3.1 Implement the optional transcript refinement toggle and local LLM adapter.
- [ ] 3.2 Ensure raw ASR output still renders when refinement is disabled or unavailable.

## 4. Polished Interface

- [ ] 4.1 Build the single-screen interface with a prominent record control, transcript viewer, copy action, and reset action.
- [ ] 4.2 Add friendly loading, permission, and error states for capture, ASR, and LLM failures.

## 5. Verification

- [ ] 5.1 Add checks that confirm no audio or transcript data persists across refresh or app restart.
- [ ] 5.2 Perform an end-to-end smoke test with one known-good local ASR provider and one known-good local LLM provider.
