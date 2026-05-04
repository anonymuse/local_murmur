# Local Murmur WSL Docker

Local Murmur runs as a dedicated FastAPI service in its own Compose stack.

## Startup

```bash
docker compose -p local-murmur -f compose/local-murmur/docker-compose.yml up --build
```

The API listens on host port `8001` by default to avoid colliding with any service already using `8000`.

## Local development dependencies

Install the development dependencies before running tests:

```bash
python3 -m pip install -e ".[dev]"
```

If you prefer an isolated environment, create and activate a virtualenv first, then run the same command inside it.

## Windows-hosted Ollama

The backend is allowed to call the same Windows-hosted Ollama service as an external dependency.

Default connection:

- `OLLAMA_BASE_URL=http://host.docker.internal:11434`

Example upload request with an explicit content type:

```bash
curl -F 'upload=@sample.wav;type=audio/wav' http://localhost:8001/transcribe
```

If the upload arrives with a generic or missing audio content type, the intake endpoint rejects it.
WAV uploads are also checked with Python's standard `wave` module so invalid or spoofed `.wav` files are rejected and duration can be reported.
Deeper media probing for non-WAV formats is deferred until a later ffmpeg-backed validation step.

If your Docker/WSL setup uses a different host alias or port, override it in `.env.local-murmur`.
