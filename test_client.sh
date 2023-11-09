#!/usr/bin/env bash

curl http://localhost:8899/v1/embeddings -X POST -H "Content-Type: application/json" -d '{
  "input": "Your text string goes here",
  "model": "text-embedding-ada-002"
}' | jq "."