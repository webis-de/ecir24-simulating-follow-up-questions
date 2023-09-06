# ecir24-simulation-by-question-under-discussion

## Data formats

### Conversations

```
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

| Model       | Params | Needs GPU | Implemented        |
|-------------|--------|-----------|--------------------|
| LLama2      | 7B     | yes       | :heavy_check_mark: |
| LLama2      | 13B    | yes       | :heavy_check_mark: |
| LLama2-Chat | 7B     | yes       | :heavy_check_mark: |
| LLama2-Chat | 13B    | yes       | :heavy_check_mark: |
| GODEL       | 2.7B?  | no        | :heavy_check_mark: |
| Alpaca      | 7B     | no (API)  | :heavy_check_mark: |

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

## Reproduction

### Parsing TREC CAsT

```
git clone git@github.com:daltonj/treccastweb.git
cd treccastweb
git checkout 3384661
./src/bash/parse-treccast.sh \
  treccastweb/2021/2021_manual_evaluation_topics_v1.0.json \
  treccastweb/2022/2022_evaluation_topics_flattened_duplicated_v1.0.json \
  > data/conversational-questions/corpus-treccast.jsonl
```
