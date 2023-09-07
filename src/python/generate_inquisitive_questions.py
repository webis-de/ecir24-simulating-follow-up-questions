import dataclasses
import json
import logging
import os.path

import click
import dacite
import yaml

from constants import DATASETS, MODELS
from corpora import ConversationTurn


def load_config(path: str):
    with open(path, "r") as in_file:
        return yaml.safe_load(in_file)


def load_prompt_template(path: str):
    with open(path, "r") as in_file:
        return in_file.read()


@click.command()
@click.option("-d", "--dataset", "datasets", multiple=True, default=["nudged_questions", "treccast"],
              type=click.Choice(DATASETS), required=True)
@click.option("-m", "--model", "models", multiple=True, default=["Alpaca"], type=click.Choice(MODELS.keys()),
              required=True)
@click.option("-c", "--config", type=click.Path(exists=True, dir_okay=False), required=False, default=None)
def main(datasets, models, config):
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    data_conf = load_config("datasets.yml")
    prompt_template = load_prompt_template("prompt-template.txt")

    if config is not None:
        run_config = load_config(config)
        datasets = run_config["datasets"]
        models = run_config["models"]

    if not os.path.exists("data/conversational-questions"):
        os.makedirs("data/conversational-questions", exist_ok=True)

    for model in models:
        llm = MODELS[model]()

        for dataset in datasets:
            llm_name = llm.name().split("/")[-1]
            file_name = f"corpus-{dataset.lower()}-{llm_name}.jsonl"
            with (open(f"data/conversational-questions/{file_name}", "w+") as out_file):
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

                        prompt = prompt_template.format(turn.system)
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
