# Container & Secrets Hardening

Northgate Retail's contractor also left behind a container image with three
problems: it runs as **root**, it has a **database password baked into the
image**, and it has **no memory limit**, so one bad request can take down the
host.

You'll fix the `Dockerfile` in `~/lab`, rebuild the image, and write a risk
register — the same kind of work as the GitHub Codespaces version of this
lab, just for a container instead of a config file.

Click **Start** to set up your environment.
