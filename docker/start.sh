#!/bin/bash
set -e

docker build -t sandbox:latest .
docker run -d --name c_sandbox --rm -v /tmp:/code sandbox:latest

echo "沙箱容器已启动：c_sandbox"
