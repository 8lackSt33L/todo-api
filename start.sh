#!/bin/bash

docker run -d \
  --name my-api \
  -p 5000:5000 \
  --restart unless-stopped \
  my-api
