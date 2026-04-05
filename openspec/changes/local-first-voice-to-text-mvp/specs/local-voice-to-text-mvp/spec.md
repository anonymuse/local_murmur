## ADDED Requirements

### Requirement: Local voice capture
The system MUST allow the user to record microphone audio locally from a simple in-app interface.

#### Scenario: Start and stop recording
- **WHEN** the user starts a recording session
- **THEN** the system begins capturing microphone audio locally
- **WHEN** the user stops the session
- **THEN** the system ends capture and prepares the audio for transcription

#### Scenario: Microphone unavailable
- **WHEN** the requested microphone cannot be accessed
- **THEN** the system surfaces a clear error and does not begin recording

### Requirement: Local transcription
The system MUST transcribe captured audio using a local ASR engine without sending audio to a remote service.

#### Scenario: Successful transcription
- **WHEN** a recording session ends successfully
- **THEN** the system produces a transcript from the captured audio using a local ASR backend

#### Scenario: ASR backend unavailable
- **WHEN** the configured local ASR backend cannot be reached or initialized
- **THEN** the system reports the failure and preserves the captured session only for the current run

### Requirement: Optional local LLM refinement
The system MUST support an optional local LLM step that can clean up punctuation, formatting, or phrasing after transcription.

#### Scenario: Refinement enabled
- **WHEN** the user enables transcript refinement
- **THEN** the system sends the draft transcript to a local LLM backend and displays the refined result

#### Scenario: Refinement disabled
- **WHEN** the user does not enable transcript refinement
- **THEN** the system displays the raw ASR transcript

### Requirement: Simple review interface
The system MUST present the recording and transcription flow in a single simple interface that allows the user to review, copy, and clear the result.

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
