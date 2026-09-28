## Step 2: Harden the Dockerfile

Edit `~/lab/Dockerfile`:

1. Add a non-root user and switch to it with `USER`, e.g.:
   ```dockerfile
   RUN useradd --create-home appuser
   USER appuser
   ```
2. Remove the hardcoded `ENV DB_PASSWORD=...` line entirely — the password
   should be passed in at `docker run` time with `-e` or `--env-file`, never
   baked into the image.
3. Rebuild:
   ```bash
   cd ~/lab
   docker build -t northgate-app .
   ```
4. Run it with a resource limit and the password supplied at runtime instead
   of at build time:
   ```bash
   docker run --rm --memory=128m -e DB_PASSWORD=runtime-secret northgate-app
   ```

Confirm the secret is gone from the image itself:

```bash
docker history --no-trunc northgate-app | grep -i DB_PASSWORD
```

This should now print nothing.
