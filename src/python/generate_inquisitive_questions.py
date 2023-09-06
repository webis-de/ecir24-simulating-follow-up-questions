import dataclasses
import json
import logging
import os.path

import click
import dacite
import yaml

from constants import PROMPT_TEMPLATE, DATASETS, MODELS
from corpora import ConversationTurn


def load_config(path: str):
    with open(path, "r") as in_file:
        return yaml.safe_load(in_file)


@click.command()
@click.option("-d", "--dataset", "datasets", multiple=True, default=["nudged_questions", "treccast"],
              type=click.Choice(DATASETS), required=True)
@click.option("-m", "--model", "models", multiple=True, default=["Alpaca"], type=click.Choice(MODELS.keys()),
              required=True)
def main(datasets, models):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    data_conf = load_config("datasets.yml")

    if not os.path.exists("data"):
        os.mkdir("data")

    for model in models:
        llm = MODELS[model]()

        for dataset in datasets:
            llm_name = llm.name().split("/")[-1]
            file_name = f"corpus-{dataset.lower()}-{llm_name}.jsonl"
            with (open(f"data/{file_name}", "w+") as out_file):
                with open(data_conf[dataset]["formatted_path"]) as in_file:
                    conversation_turn = None
                    for line in in_file:
                        turn = dacite.from_dict(data_class=ConversationTurn, data=json.loads(line))
                        if conversation_turn is None \
                                or conversation_turn.conversation_id != turn.conversation_id:
                            conversation_turn = ConversationTurn(turn.id, turn.conversation_id, turn.system, [], [])
                        else:
                            past_turn = conversation_turn.to_past_turn()
                            conversation_turn.id = turn.id
                            conversation_turn.conversation_id = turn.conversation_id
                            conversation_turn.system = turn.system
                            conversation_turn.previous_turns.append(past_turn)

                        prompt = PROMPT_TEMPLATE.format(turn.system)
                        response = llm.generate(prompt)
                        questions = llm.parse_response(response)
                        if questions is not None:
                            conversation_turn.user_responses = questions
                        else:
                            conversation_turn.user_responses = [response]

                        out_file.write(json.dumps(dataclasses.asdict(conversation_turn)))
                        out_file.write("\n")

        del llm


if __name__ == '__main__':
    main()
