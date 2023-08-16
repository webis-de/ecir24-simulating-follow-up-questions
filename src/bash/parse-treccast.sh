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
           history[cindex] = "{\"turnNumber\":\""turnNumber"\",\"user\":\""utterance"\"}"
         } else {
           if (!(conversation"-"turnNumber in printed)) {
             printf "%s", "{\"conversation\":"conversation",\"turnNumber\":\""turnNumber"\",\"system\":\""lastResponse"\",\"user\":\""utterance"\",\"history\":["
             for (i = 1; i < cindex; i += 1) {
               if (i > 1) { printf "," }
               printf "%s", history[i]
             }
             printf "]}\n"

             printed[conversation"-"turnNumber] = 1
           }
           history[cindex] = "{\"turnNumber\":\""turnNumber"\",\"system\":\""lastResponse"\",\"user\":\""utterance"\"}"
         }

         lastResponse = response
       }'
done

