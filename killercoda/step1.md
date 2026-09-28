## Step 1: Find what's wrong

```bash
cd ~/lab
cat Dockerfile
```

Look for:
- **No `USER` instruction** — the container runs as root by default.
- **A real secret in `ENV DB_PASSWORD=...`** — anyone who runs `docker
  history` or `docker inspect` on the built image can read it.
- **No memory limit** set when the container runs.

Confirm the secret is visible in the built image's history:

```bash
docker build -t northgate-app .
docker history --no-trunc northgate-app | grep -i DB_PASSWORD
```

You should see the plaintext password in the output — that's the bug.
