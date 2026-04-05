# 1. architecture verdict

Conditional approve with revisions before implementation.

The change is directionally solid: the proposal, spec, and design all converge on a small local-first product with a clear MVP boundary: local microphone capture, local ASR, optional local LLM refinement, a single review surface, and no automatic persistence. That is a coherent architecture for first delivery.

The remaining problems are not about product direction; they are about execution risk. The local runtime boundary is still underspecified, the reference provider stack is still unresolved, and the privacy model is not yet defined tightly enough to support the claims in the spec and proposal. The spec does exist, but it lives under `specs/local-voice-to-text-mvp/spec.md` rather than at the path originally requested, so traceability should be cleaned up.

Relevant references:
- [proposal.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/proposal.md#L7)
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L3)
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L23)
- [tasks.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/tasks.md#L3)

# 2. critical issues

## C1. The local deployment and trust boundary is still underspecified

Severity: Critical

The design selects a browser UI plus a small local backend, which is reasonable, but it still does not define the runtime topology clearly enough for implementation. The documents do not state how the backend is launched, how the UI locates it, whether it binds only to loopback, what transport is used, or what the browser security and permission model is expected to be. Because the spec requires local capture and explicitly forbids sending audio to a remote service during transcription, this boundary needs to be explicit rather than implied.

Without this, the team cannot validate the core architectural claim that audio remains local, and it will be difficult to reason about packaging, operability, and security.

Relevant references:
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L16)
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L23)
- [tasks.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/tasks.md#L3)

## C2. The MVP still lacks a locked reference ASR/LLM environment

Severity: Critical

The spec and tasks assume an end-to-end local path, but the design still leaves the default ASR backend open as an unresolved question. For an MVP with no existing product code, supporting provider abstraction before selecting one known-good ASR backend and one optional LLM backend creates avoidable instability. It weakens sequencing, testing, installation guidance, performance expectations, and supportability.

The current adapter approach is fine as an internal seam, but the shipped MVP needs one reference environment that all verification work is anchored to.

Relevant references:
- [proposal.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/proposal.md#L8)
- [proposal.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/proposal.md#L9)
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L39)
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L79)
- [tasks.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/tasks.md#L25)

## C3. The privacy model is still too loose for the stated local-first guarantees

Severity: Critical

The spec now clearly says the system must use a local ASR engine without sending audio to a remote service and must not persist audio, transcripts, or model outputs beyond the active session. That is good. The design and tasks still do not translate those requirements into enforceable operational constraints. They do not say whether sensitive text or audio can appear in logs, browser storage, crash dumps, debug traces, provider-side logs, or telemetry. They also do not define whether outbound network access is prohibited during transcription and refinement, or only discouraged.

For a privacy-focused MVP, “ephemeral” needs to be defined as a concrete artifact-retention policy, not just as a UX behavior after refresh or restart.

Relevant references:
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L16)
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L50)
- [proposal.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/proposal.md#L11)
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L31)
- [tasks.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/tasks.md#L24)

## C4. Failure semantics are incomplete relative to what the spec now requires

Severity: Critical

The spec defines minimum behavior for microphone unavailability and ASR backend unavailability, including preserving the captured session for the current run when the ASR backend cannot be reached or initialized. The design and tasks do not fully carry that forward into implementation detail or verification. There is no explicit behavior defined for retry, recovery, cancellation, backend crash mid-session, or how the retained in-run session state is represented after ASR failure.

This matters because the spec has moved beyond happy-path product intent and now contains concrete expectations. The architecture should reflect those failure and recovery paths directly.

Relevant references:
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L12)
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L23)
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L63)
- [tasks.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/tasks.md#L20)

# 3. non-blocking issues

## N1. Spec path and review path traceability are awkward

Severity: Medium

The spec exists, but not at the originally expected path. It is stored under `specs/local-voice-to-text-mvp/spec.md` rather than directly under the change root. That is not an architectural defect by itself, but it did cause review confusion and weakens discoverability. The change should make that structure explicit so reviewers and implementers do not assume the spec is missing.

Relevant references:
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md)
- [/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/.openspec.yaml](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/.openspec.yaml)

## N2. Streaming scope is still ambiguous

Severity: Medium

The design refers to “the live or final transcript,” but the spec only requires transcript availability after transcription completes. If streaming is not part of the MVP, the design should say so directly. Leaving that ambiguity in place risks accidental scope growth in both backend protocol and UI state management.

Relevant references:
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L41)
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L56)

## N3. Verification coverage is still too thin

Severity: Medium

The tasks cover persistence checks and a single smoke test, which is a start, but they do not yet verify several behaviors now implied by the spec: microphone denial, ASR unavailable, refinement unavailable, and session recovery within the current run after backend failure.

Relevant references:
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L12)
- [spec.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/specs/local-voice-to-text-mvp/spec.md#L23)
- [tasks.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/tasks.md#L22)

## N4. Rollback language remains more optimistic than designed

Severity: Low

The migration section says the new flow can be disabled if issues arise, but there is still no concrete release mechanism described that would make rollback low-risk in practice.

Relevant references:
- [design.md](/home/anony/code/voice_to_text/openspec/changes/local-first-voice-to-text-mvp/design.md#L70)

# 4. anything to remove or defer

- Defer true multi-provider support. Keep the adapter seam, but implement and validate exactly one ASR provider and at most one optional LLM provider for MVP.
- Defer any streaming or “live transcript” behavior unless the spec is expanded to make it a first-class requirement.
- Defer desktop-shell packaging decisions until the browser UI plus local backend flow is validated end to end.
- Remove vague provider wording such as “Vibe Voice or similar” from the implementation plan once the reference stack is chosen.
- Defer polish-oriented UI work until the raw local capture, failure handling, and privacy constraints are proven.

# 5. recommended revisions

1. Update the design to define the local runtime boundary explicitly.
Include:
- backend launch model
- UI-to-backend transport
- loopback-only binding expectation
- browser permission assumptions
- whether any outbound network traffic is permitted during ASR or refinement

2. Lock the MVP to a reference environment.
Specify:
- one ASR provider
- one optional local LLM provider
- supported browser and OS assumptions
- install prerequisites and expected local services
- the known-good configuration used for verification

3. Strengthen the privacy contract so it matches the spec.
State explicitly:
- no remote ASR calls
- no automatic persistence beyond the active session
- no transcript or audio in logs
- no browser storage of transcript or audio
- temp-file deletion on success and failure
- clipboard caveat, since manual copy transfers control to the OS

4. Carry the spec’s failure semantics into design and tasks.
Add explicit behavior and tests for:
- microphone unavailable
- ASR backend unavailable
- refinement unavailable while raw ASR still succeeds
- retained in-run session state after ASR failure
- retry and reset behavior
- backend crash or disconnect during processing

5. Tighten scope wording around transcript display.
If MVP is batch-only, say that directly in the design and tasks. Do not leave streaming implied.

6. Improve change traceability.
Make it explicit in the review and change metadata that the normative spec lives at `specs/local-voice-to-text-mvp/spec.md`, so future reviews do not treat it as missing.
