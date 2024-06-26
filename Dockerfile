FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

COPY . /app
WORKDIR /app

RUN apt update && apt install -y build-essential bash && make clean install

SHELL ["/bin/bash", "-c"]

ENTRYPOINT source venv/bin/activate && python src/python/generate_inquisitive_questions.py --config run.yml

