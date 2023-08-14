# User Simulation with LLMs

Repository for evaluating LLMs for user simulation for conversational agents. 

## Models

| Model  | Params | Needs GPU | Implemented            |
|--------|--------|-----------|------------------------|
| LLama2 | 7B     | yes       | :heavy_check_mark:     |
| LLama2 | 13B    | yes       | :x:                    |
| Alpaca | 7B     | no (API)  | :x:                    |

## Setup

1. The LLama2 model needs access permissions to their repository. 
Hence, you need to have a Hugging Face account with an access token (can be created [here](https://huggingface.co/settings/tokens)).
Fill out [this Meta-AI form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) and request permission 
to their models [here](https://huggingface.co/meta-llama/Llama-2-7b-hf). 
2. Run the following command to add your Hugging Face access token to the repo. 
    ```bash
    make configure
    ```
3. Run the following command to install all dependencies.
   ```bash
   make clean install
   ```
4. Activate the virtual environment and run the experiment.
   ```bash
   source venv/bin/activate
   python src/generate_inquisitive_questions.py
   ```

