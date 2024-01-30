import dataclasses
import json
import random

import dacite

from corpora import ConversationTurn
from generate_followup_questions import load_config


def main():
    data_conf = load_config("datasets.yml")
    data = []

    path = data_conf["nudged-questions"]["formatted_path"]
    with open(path) as in_file:
        for line in in_file:
            data.append(dacite.from_dict(ConversationTurn, json.loads(line)))

    for turn in data:
        turn.user_responses = random.sample(turn.user_responses, k=30)

    out_path = data_conf["nudged-questions"]["formatted_path"].replace(".jsonl", "-sampled.jsonl")
    with open(out_path, "w") as out_file:
        for turn in data:
            out_file.write(json.dumps(dataclasses.asdict(turn)))
            out_file.write("\n")


if __name__ == '__main__':
    main()
