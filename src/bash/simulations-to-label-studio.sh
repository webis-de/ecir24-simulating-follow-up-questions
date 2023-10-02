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
        | map(. |
            "System " + (.index|tostring) + ": " + .system + "\n\n"
            + "User " + (.index|tostring) + ": " + .user_responses[0] + "\n\n"
          )
        | join("")
        | {
            "id": $context.id,
            "dataset": "'"$test_data"'",
            "history": ("User 0: " + $context.information_need + "\n\n" + .),
            "system": $context.system,
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
    get_for_simulation $test_data gpt-4 "" "" ""
  done
  for user_experience in naive savvy;do
    for user_direction in reasons implications;do
      get_for_simulation $test_data alpaca-7b "" $user_experience $user_direction
      get_for_simulation $test_data Llama-2-13b-hf "" $user_experience $user_direction
      get_for_simulation $test_data Llama-2-13b-hf inquisitive $user_experience $user_direction
      get_for_simulation $test_data gpt-4 "" $user_experience $user_direction
    done
  done
done \
  | shuf \
  | python3 -c '
import json, sys
data = {}
counts = {}
for line in sys.stdin:
    record = json.loads(line)
    turn_id = record["id"]
    if turn_id not in data:
        data[turn_id] = {"id":turn_id}
        counts[turn_id] = 0
    number = str(counts[turn_id])
    counts[turn_id] += 1
    data[turn_id]["user_response_" + number] = record["user_response"]
    if "history" in record:
      data[turn_id]["history"] = record["history"]
      data[turn_id]["system"] = record["system"]
      data[turn_id]["dataset"] = record["dataset"]
      data[turn_id]["user_response_" + number + "_type"] = "original"
    else:
      data[turn_id]["user_response_" + number + "_type"] = "generated"
      data[turn_id]["user_response_" + number + "_base_model"] = record["base_model"]
      data[turn_id]["user_response_" + number + "_tuning"] = record["tuning"]
      data[turn_id]["user_response_" + number + "_user_experience"] = record["user_experience"]
      data[turn_id]["user_response_" + number + "_user_direction"] = record["user_direction"]
for turn_id in data:
  print(json.dumps({"id":turn_id, "data":data[turn_id]}))
' \
  | sort \
  | jq -s '.'


