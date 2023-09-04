#!/bin/bash

for input in $@;do
  cat $input \
    | jq '. as $context | .user_responses[] | . as $response | $context | .user_response = $response' \
    | jq '. as $context | .previous_turns | map(. | "System " + (.index|tostring) + ": " + .system + "\n\nUser " + (.index|tostring) + ": " + .user_responses[0] + "\n\n") | join("") | . as $history | $context | .history = "User 0: " + .information_need + "\n\n" + $history + "System " + (.previous_turns|length+1|tostring) + ": " + .system + "\n\nUser " + (.previous_turns|length+1|tostring) + ": " + .user_response | .turns = (.previous_turns|length+1)' \
    | jq '{"id":.id,"text":.history,"turns":.turns}' \
    | jq '{"id":.id,"data":.}' \
    | jq -s '.'
done

