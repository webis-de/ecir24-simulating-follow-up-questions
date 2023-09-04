#!/bin/bash

for input in $@;do
  cat $input \
    | jq '. as $context
        | .user_responses[]
        | . as $response
        | $context
        | .user_response = $response' \
    | jq '. as $context
        | .previous_turns
        | reverse
        | map(. | "User " + (.index|tostring) + ": " + .user_responses[0] + "\n\nSystem " + (.index|tostring) + ": " + .system + "\n\n")
        | join("")
        | . as $history
        | $context
        | .history = "System " + (.previous_turns|length+1|tostring) + ": " + .system + "\n\n" + $history + "User 0: " + .information_need + "\n\n"' \
    | jq '{"id":.id,"history":.history,"user_response":.user_response}' \
    | jq '{"id":.id,"data":.}' \
    | jq -s '.'
done

