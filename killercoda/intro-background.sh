#!/bin/bash
set -e
mkdir -p /root/lab
cat > /root/lab/Dockerfile <<'DOCKERFILE'
FROM ubuntu:22.04
ENV DB_PASSWORD=SuperSecret123!
RUN apt-get update && apt-get install -y python3
COPY app.py /app/app.py
CMD ["python3", "/app/app.py"]
DOCKERFILE
cat > /root/lab/app.py <<'APP'
import os
print("Northgate app starting, DB_PASSWORD is set:", bool(os.environ.get("DB_PASSWORD")))
APP
cat > /root/lab/risk_register.md <<'REGISTER'
| Threat | Likelihood (1-5) | Impact (1-5) | Mitigation |
|---|---|---|---|
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |
REGISTER
echo "Lab files ready in ~/lab"
