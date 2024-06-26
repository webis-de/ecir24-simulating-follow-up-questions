SHELL := /bin/bash

auth: auth_hf auth_chatnoir


auth_hf:
	read -p "Huggingface access token: " hftoken;\
	echo "$${hftoken}" > hf-token.txt;

auth_chatnoir:
	read -p "Chatnoir API access token: " apitoken;\
	echo "$${apitoken}" > chatnoir-token.txt;

configure:
	source venv/bin/activate && python src/python/configure.py

install: download install_venv huggingface_login

install_venv:
	@if [ ! -d "venv" ]; then\
		python3 -m venv venv; \
	fi; \
	source venv/bin/activate && pip install -r requirements.txt;
	source venv/bin/activate && python -c "import nltk; nltk.download('wordnet');"
	source venv/bin/activate && python -c "import nltk; nltk.download('punkt');"
	source venv/bin/activate && python -m spacy download en_core_web_sm

huggingface_login: install_venv
	source venv/bin/activate && huggingface-cli login --token $(shell cat hf-token.txt)

install_mlc_chat: install_venv
	@if [ `command -v nvidia-smi` ]; then\
		echo "install with gpu support"; \
		source venv/bin/activate && pip install --pre --force-reinstall mlc-ai-nightly-cu116 mlc-chat-nightly-cu116 -f https://mlc.ai/wheels ;\
	else \
	    echo "install without gpu support"; \
		source venv/bin/activate && pip install --pre --force-reinstall mlc-ai-nightly mlc-chat-nightly -f https://mlc.ai/wheels ; \
	fi

	git lfs install

	mkdir -p dist/prebuilt
	git clone https://github.com/mlc-ai/binary-mlc-llm-libs.git dist/prebuilt/lib

	cd dist/prebuilt && git clone https://huggingface.co/mlc-ai/mlc-chat-Llama-2-7b-chat-hf-q4f16_1

docker-build:
	docker build -t registry.webis.de/code-lib/public-images/simulation-by-question-under-discussion:latest .

docker-push:
	docker push registry.webis.de/code-lib/public-images/simulation-by-question-under-discussion:latest

build: docker-build docker-push

deploy:
	sudo cp src/bash/generate-inquisitive-questions.slurm.sh /mnt/ceph/storage/data-tmp/current/${USER}/
	sudo cp -R src /mnt/ceph/storage/data-tmp/current/${USER}/generate-inquisitive-questions/
	sudo cp run.yml /mnt/ceph/storage/data-in-progress/data-research/conversational-search/ecir24-simulation-by-question-under-discussion/

download:
	wget -P data https://zenodo.org/records/10640348/files/corpus-webis-follow-up-questions-24.zip
	unzip data/corpus-webis-follow-up-questions-24.zip -d data/corpus-webis-follow-up-questions-24


clean:
	rm -rf venv dist
