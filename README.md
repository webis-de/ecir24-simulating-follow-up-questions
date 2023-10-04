# ecir24-simulation-by-question-under-discussion

## Data formats

### Conversations

```json lines
{
  "id": "<text, points to the user's turn in the original data set>",
  "conversation_id": "<text, points to the conversation in the original data set>",
  "information_need": "<text, representation of the user's need with which they started the conversation>",
  "system": "<text produced by the system at this turn>",
  "user_responses": [
    "<text, 1st response of a user to the system text>",
    "<text, 2nd (alternative) response of a user to the system text>",
    ...
  ],
  "previous_turns": [
    { "index": 1, "id": "<text>", "system": "<text>", "user_responses": ["<text>" ,"<text>" ] },
    { "index": 2, "id": "<text>", "system": "<text>", "user_responses": ["<text>" ,"<text>" ] },
    ...
  ]
}
```

## Models

| Model       | Params | Requirements            |
|-------------|--------|-------------------------|
| Alpaca      | 7B     | Chatnoir API Token      |
| GODEL       | 2.7B?  | -                       |
| LLama2      | 7B     | GPU, Hugging Face Token | 
| LLama2      | 13B    | GPU, Hugging Face Token | 
| LLama2-Chat | 7B     | GPU, Hugging Face Token | 
| LLama2-Chat | 13B    | GPU, Hugging Face Token |  

## Authentication

1. The LLama2 model needs access permissions to their repository.
   Hence, you need to have a Hugging Face account with an access token (can be
   created [here](https://huggingface.co/settings/tokens)).
   Fill out [this Meta-AI form](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) and request
   permission
   to their models [here](https://huggingface.co/meta-llama/Llama-2-7b-hf).
2. The Alpaca model requires an Chatnoir API token which can be requested [here](https://www.chatnoir.eu/apikey).

## Setup

1. Run the following command to add your Hugging Face and Chatnoir API access token to the repo.
    ```bash
    make auth
    ```
2. Run the following command to install all dependencies.
   ```bash
   make clean install
   ```
3. Activate the virtual environment and run the experiment.
   ```bash
   source venv/bin/activate
   python src/python/generate_inquisitive_questions.py
   ```

## Deploy experiment on gammaweb

1. Configure models and datasets for the experiment.
   ```bash
   make configure
   ```
2. Build and push docker image to the registry.
   ```bash
   make deploy
   ```
3. Login to [ssh.webis.de]()
4. Submit job to Slurm
   ```bash
   sbatch generate-inquisitive-questions.slurm.sh
   ```

## Reproduction

### Parsing TREC CAsT

```bash
./src/bash/parse-label-studio.sh cast-question-target-annotation-at-2023-09-17-22-04-f5e8d8a3.json \
  | awk -F'-' '$2 >= 132' \
  | sort -g \
  > data/treccast22-question-targets.jsonl

git clone git@github.com:daltonj/treccastweb.git
python src/python/parse-treccast.py \
  treccastweb/2022/2022_evaluation_topics_flattened_duplicated_v1.0.json \
  data/treccast22-question-targets.jsonl \
  > data/conversational-questions/corpus-treccast22.jsonl 
```

### Parsing Human Annotations from Label Studio

```bash
cat data/human-assessment.json.gz \
  | gunzip \
  | python3 src/python/parse-label-studio-human-assessment.py /dev/stdin \
  | sort -g \
  > data/human-assessment.tsv
```

### Calculate Kappa

```
cat data/human-assessment.json.gz \
  | gunzip \
  | python3 src/python/parse-label-studio-human-assessment-for-kappa.py /dev/stdin \
  > data/human-assessment-single-annotations.tsv
./src/r/kappa.R data/human-assessment-single-annotations.tsv 
```

### Compute top-k most-frequent leading bigrams

```bash
source venv/bin/activate
python src/python/compute_leading_bigrams_frequency -f <path_to_dataset> -k <number_of_k>
```
