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
  "previous-turns": [
    { "index": 1, "id": "<text>", "system": "<text>", "user_responses": ["<text>" ,"<text>" ] },
    { "index": 2, "id": "<text>", "system": "<text>", "user_responses": ["<text>" ,"<text>" ] },
    ...
  ]
}
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
