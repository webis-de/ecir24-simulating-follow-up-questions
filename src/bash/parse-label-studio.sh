#!/bin/bash
cat $1 \
  | jq -c '.[]
      | . as $context
      | select(([ .annotations[].result[] | select(.to_name == "history") ] | length) > 0)
      | [ .annotations[].result[] | select(.to_name == "history") ][0].value.start as $target_offset 
      | if ([ .annotations[].result[] | select(.to_name == "user-response") ] | length) == 0 then
          .data.user_response
        else
          .annotations[].result[]  | select(.to_name == "user-response") | .value.text
        end
      | ($context.data.history | split("\n\nSystem")) as $turns
      | ($turns | length ) as $turn_index
      | ($context.data.history | split("\n\nSystem") | map(. | length | . + 10)) as $turn_lengths
      | (reduce $turn_lengths[] as $length ([0]; . + [.[-1] + $length])) as $turn_offsets
      | ([ $turn_offsets | to_entries[] | select(.value <= $target_offset) ][-1] | $turn_index - .key) as $target_turn
      | {
          id: $context.data.id,
          user_response: .,
          turn_index: $turn_index,
          target_turn_index: $target_turn
        }
      '

