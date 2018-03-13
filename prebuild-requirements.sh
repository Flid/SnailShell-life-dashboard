#!/usr/bin/env sh
set -e

docker build -f Dockerfile-requirements -t antonkir/snailshell_life_dashboard_requirements:latest .
docker push antonkir/snailshell_life_dashboard_requirements:latest
