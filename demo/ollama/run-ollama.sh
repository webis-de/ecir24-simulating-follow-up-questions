#!/bin/bash
docker run --rm -it -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull llama2
