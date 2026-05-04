## ADDED Requirements

### Requirement: Local voice capture
The system MUST allow the user to provide microphone audio locally through a simple browser interface or direct API upload.

#### Scenario: Start and stop recording
- **WHEN** the user starts a recording session
- **THEN** the system begins capturing microphone audio locally
- **WHEN** the user stops the session
- **THEN** the system ends capture and prepares the audio for transcription

#### Scenario: Upload existing recording
- **WHEN** the user uploads a supported audio file through the browser UI or `curl`
- **THEN** the system accepts the file for transcription without requiring browser microphone capture

#### Scenario: Microphone unavailable
- **WHEN** the requested microphone cannot be accessed
- **THEN** the system surfaces a clear error and does not begin recording

### Requirement: Local transcription
The system MUST transcribe captured audio using Faster-Whisper without sending audio to a remote transcription service.

#### Scenario: Successful transcription
- **WHEN** a recording session ends successfully
- **THEN** the system produces a transcript from the captured audio using the configured Faster-Whisper backend

#### Scenario: ASR backend unavailable
- **WHEN** the configured local ASR backend cannot be reached or initialized
- **THEN** the system reports the failure and preserves the captured session only for the current run

### Requirement: Optional local LLM refinement
The system MUST support an optional local LLM step that can clean up punctuation, formatting, or phrasing after transcription.

#### Scenario: Refinement enabled
- **WHEN** the user enables transcript refinement
- **THEN** the system sends the draft transcript to the configured Ollama backend and displays the refined result

#### Scenario: OpenAI refinement explicitly configured
- **WHEN** `LLM_PROVIDER=openai` is configured with a valid user-supplied API key
- **THEN** the system may send the draft transcript to the OpenAI API for refinement
- **AND** the system does not treat this as local-only processing

#### Scenario: Refinement disabled
- **WHEN** the user does not enable transcript refinement
- **THEN** the system displays the raw ASR transcript

#### Scenario: Refinement unavailable
- **WHEN** transcription succeeds but the configured LLM provider is unavailable
- **THEN** the system reports the refinement failure and still returns the raw ASR transcript

### Requirement: Simple review interface
The system MUST present the recording or upload and transcription flow in a single simple interface that allows the user to review, copy, and clear the result.

#### Scenario: Review transcript
- **WHEN** transcription completes
- **THEN** the transcript is visible immediately in the interface
- **AND** the user can copy the transcript to the clipboard

#### Scenario: Reset the session
- **WHEN** the user clears the session or starts a new recording
- **THEN** the interface resets to an empty state ready for the next capture

### Requirement: No automatic persistence
The system MUST NOT persist audio, transcripts, or model outputs beyond the active session for the MVP.

#### Scenario: Refresh or exit
- **WHEN** the user closes, refreshes, or restarts the application
- **THEN** previously captured audio and transcripts are no longer available unless the user manually copied them

#### Scenario: No storage setup
- **WHEN** the application runs in MVP mode
- **THEN** it does not require a database, file storage, or account system

#### Scenario: Sensitive data excluded from storage and logs
- **WHEN** the system processes audio, raw transcripts, cleaned transcripts, or model outputs
- **THEN** it does not write those contents to application logs, browser storage, a database, or long-term files

#### Scenario: Temporary artifact cleanup
- **WHEN** transcription succeeds or fails
- **THEN** temporary audio artifacts are deleted before the request completes whenever the process can safely clean them up
