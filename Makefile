SHELL := /bin/bash

install: install_mlc_chat

install_venv:
	@if [ ! -d "venv" ]; then\
		python3 -m venv venv; \
	fi

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

clean:
	rm -rf venv
