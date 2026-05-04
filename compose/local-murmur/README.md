# Local Murmur Compose Stack

This directory contains the isolated Local Murmur Docker Compose stack.

Use the stack with an explicit project name:

```bash
docker compose -p local-murmur -f compose/local-murmur/docker-compose.yml up --build
```

The API container is named `local-murmur-api` and the default host port is `8001`.

The stack does not require a local `.env.local-murmur` file for `docker compose config`.
If you want overrides, copy `.env.local-murmur.example` to `.env.local-murmur` and run:

```bash
docker compose --env-file compose/local-murmur/.env.local-murmur -p local-murmur -f compose/local-murmur/docker-compose.yml up --build
```
