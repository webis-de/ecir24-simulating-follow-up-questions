#!/bin/bash

for input in $@;do
  cat $input \
    | sed 's/\\"//g' \
    | jq -r '.[]
        | .number as $conversation
        | .turn
        | keys[] as $key
        | .[$key]
        | [$conversation, $key + 1, .number, .raw_utterance + .utterance, .passage + .response]
        | @tsv' \
     | awk -F '\t' '{
         conversation = $1
         cindex = $2
         turnNumber = $3
         utterance = $4
         response = $5

         if (cindex == 1) {
           delete history
           history[cindex] = "{\"index\":1,\"user_responses\":[\""utterance"\"]}"
           informationNeed = utterance
         } else {
           if (!(conversation"-"turnNumber in printed)) {
             printf "%s", "{\"id\":\"cast-"conversation"-"turnNumber"\",\"conversation_id\":\"cast-"conversation"\",\"system\":\""lastResponse"\",\"user_responses\":[\""utterance"\"],\"previous_turns\":["
             for (i = 1; i < cindex; i += 1) {
               if (i > 1) { printf "," }
               printf "%s", history[i]
             }
             printf "],\"information_need\":\""informationNeed"\"}\n"

             printed[conversation"-"turnNumber] = 1
           }
           history[cindex] = "{\"index\":"cindex",\"system\":\""lastResponse"\",\"user_responses\":[\""utterance"\"]}"
         }

         lastResponse = response
       }' \
     | python3 -c '
import sys, json
lastSystem = ""
lastRecord = ""
for line in sys.stdin:
  record = json.loads(line)
  if record["system"] == lastSystem:
    lastRecord["user_responses"].append(record["user_responses"][0]);
  else:
    if lastSystem != "":
      json.dump(lastRecord, sys.stdout)
      print()
    lastSystem = record["system"]
    lastRecord = record
json.dump(lastRecord, sys.stdout)
print()
         '
done

