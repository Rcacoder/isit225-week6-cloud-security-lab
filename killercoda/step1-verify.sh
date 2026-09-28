#!/bin/bash
docker image inspect northgate-app > /dev/null 2>&1 && exit 0
exit 1
