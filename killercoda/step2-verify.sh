#!/bin/bash
set -e
grep -q '^USER ' /root/lab/Dockerfile || exit 1
grep -qi 'ENV DB_PASSWORD' /root/lab/Dockerfile && exit 1
exit 0
