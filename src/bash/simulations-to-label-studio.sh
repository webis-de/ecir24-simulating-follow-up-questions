#!/bin/bash

data_dir=$1

get_for_original() {
  local test_data="$1"

  data_file=$data_dir/corpus-$test_data.jsonl
  if [ "$test_data" == treccast ];then
    data_file=$data_dir/corpus-treccast22.jsonl
  fi

  cat $data_file \
    | jq -c '. as $context
        | .previous_turns
        | reverse
        | map(. | "User " + (.index|tostring) + ": " + .user_responses[0] + "\n\nSystem " + (.index|tostring) + ": " + .system + "\n\n")
        | join("")
        | {
            "id": $context.id,
            "history": ("System " + ($context.previous_turns|length+1|tostring) + ": " + $context.system + "\n\n" + . + "User 0: " + $context.information_need + "\n\n"),
            "user_response": $context.user_responses[0]
          }'
}

get_for_simulation() {
  local test_data="$1"
  local base_model="$2"
  local tuning="$3"
  local user_experience="$4"
  local user_direction="$5"

  for fold in 0 1 2;do
    simulation_file=$data_dir/simulations/$(echo "corpus-$test_data-$fold-$base_model-$tuning-$user_experience-$user_direction-run0.jsonl" | sed 's/--*/-/g')
    if [ -e "$simulation_file" ];then
      cat $simulation_file \
        | jq -c '{
              "id": .id,
              "test_data": "'"$test_data"'",
              "base_model": "'"$base_model"'",
              "tuning": "'"$tuning"'",
              "user_experience": "'"$user_experience"'",
              "user_direction": "'"$user_direction"'",
              "user_response": .user_responses[0]
            }'
    else
      echo "MISSING: $simulation_file" > /dev/stderr
    fi
  done
}

for test_data in treccast nudged-questions;do
  get_for_original $test_data
  for base_model in alpaca-7b Llama-2-7b-hf Llama-2-13b-hf;do
    for tuning in "" inquisitive treccast nudged-questions;do
      get_for_simulation $test_data $base_model $tuning "" ""
    done
  done
  for user_experience in naive savvy;do
    for user_direction in reasons implications;do
      get_for_simulation $test_data alpaca-7b "" $user_experience $user_direction
      get_for_simulation $test_data Llama-2-13b-hf "" $user_experience $user_direction
      get_for_simulation $test_data Llama-2-13b-hf inquisitive $user_experience $user_direction
    done
  done
done \
  | sort \
  | python3 -c '
import json, sys
turns = {}
for line in sys.stdin:
    record = json.loads(line)
    turn_id = record["id"]
    if turn_id not in turns:
        turns[turn_id] = {}
    if "history" in record:
      turns[turn_id]["history"] = record["history"]
      turns[turn_id]["original"] = record["user_response"]
    else:
      turns[turn_id][record["base_model"]+"_"+record["tuning"]+"_"+record["user_experience"]+"_"+record["user_direction"]] = record["user_response"]
for turn_id in turns:
  print(json.dumps({"id":turn_id, "data":turns[turn_id]}))
' \
  | jq -s '.'


