# Simulating Follow-up Questions in Conversational Search

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

### Tuning Models

TODO

## Reproduction

### Automated Comparison (Table 1)

This computation may take a while depending on your hardware. A GPU is preferred for this experiment.

```bash
source venv/bin/activate
python src/python/compute_automatic_comparison.py
```

### Human Assessment (Table 2)

```bash
source venv/bin/activate
python src/python/compute_human_assessment.py
```

### User Modeling (Table 3)

```bash
source venv/bin/activate
python src/python/compute_user_model.py
```

### Calculate Kappa

TODO: does it calculate both? Adjust to downloaded corpus

```bash
cat data/human-assessment.json.gz \
  | gunzip \
  | python3 src/python/parse-label-studio-human-assessment-for-kappa.py /dev/stdin \
  > data/human-assessment-single-annotations.tsv
./src/r/kappa.R data/human-assessment-single-annotations.tsv 
```

### Compute top-k most-frequent leading bigrams (Appendix)

TODO: Adjust to downloaded corpus

```bash
source venv/bin/activate
python src/python/compute_leading_bigrams_frequency.py [-d nudged-questions|treccast] [-k <number_of_bigrams>]
```
