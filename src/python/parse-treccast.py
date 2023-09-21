import sys, json

treccast_file_name = sys.argv[1]
treccast_question_target_file_name = sys.argv[2]

question_targets = {}
with open(treccast_question_target_file_name) as treccast_question_target_file:
    for line in treccast_question_target_file:
        record = json.loads(line)
        question_targets[record["id"]] = record

records = {}
with open(treccast_file_name) as treccast_file:
    treccast = json.load(treccast_file)
    for conversation in treccast:
        conversation_id = "cast-" + str(conversation["number"])
        information_need = conversation["turn"][0]["utterance"]
        previous_response = conversation["turn"][0]["response"]
        turns = []
        for t in range(len(conversation["turn"]))[1:]:
            turn = conversation["turn"][t]
            if "response" in turn:
                turn_id = conversation_id + "-" + str(turn["number"])
                turns.append({
                        "index": t,
                        "id": turn_id,
                        "system": previous_response,
                        "user_responses": turn["utterance"]
                    })
                previous_response = turn["response"]

                if turn_id in question_targets:
                    target = question_targets[turn_id]
                    target_turn_index = target["target_turn_index"]
                    target_turn_id = turns[target_turn_index - 1]["id"]
                    parent_turn_id = conversation_id
                    if target_turn_index > 1:
                        parent_turn_id = turns[target_turn_index - 2]["id"]

                    if not parent_turn_id in records:
                        def make_user_response_an_array(x):
                            x["user_responses"] = [ x["user_responses"] ] 
                            return x

                        previous_turns = [make_user_response_an_array(x.copy()) for x in turns[0:(target_turn_index - 1)]]
                        records[parent_turn_id] = {
                          "id": turn_id,
                          "conversation_id": conversation_id,
                          "information_need": information_need,
                          "system": turns[target_turn_index - 1]["system"],
                          "user_responses": [],
                          "previous_turns": previous_turns
                        }

                    user_response = target["user_response"].strip()
                    if not user_response in records[parent_turn_id]["user_responses"]:
                        records[parent_turn_id]["user_responses"].append(user_response)

for record in records:
    json.dump(records[record], sys.stdout)
    print()

