import dataclasses
import json
import os.path

import click
import dacite
import yaml

from constants import *
from corpora import ConversationTurn


def load_config(path: str):
    with open(path, "r") as in_file:
        return yaml.safe_load(in_file)


def load_prompt_template(path: str):
    with open(path, "r") as in_file:
        return in_file.read()


def load_dataset(path: str) -> List[ConversationTurn]:
    turns = []
    with open(path) as in_file:
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

            turns.append(conversation_turn)

    return turns


@click.command()
@click.option("-d", "--dataset", "datasets", multiple=True, default=["nudged-questions", "treccast"],
              type=click.Choice(DATASETS), required=True)
@click.option("-m", "--model", "models", multiple=True, default=["LLama27BChat"], type=click.Choice(MODELS.keys()),
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
            for fold in range(NUM_FOLDS):
                llm_name = llm.name().split("/")[-1]

                path = data_conf[dataset]["formatted_path"].format(k=fold)
                turns = load_dataset(path)

                for run in range(1, NUM_REPETITIONS):
                    prompts = []
                    for turn in turns:
                        prompt = prompt_template.format(turn.system)
                        prompts.append(prompt)

                    responses = llm.generate_all(prompts)

                    for turn, prompt, response in zip(turns, prompts, responses):
                        questions = llm.parse_response(response)
                        if questions is not None:
                            turn.user_responses = questions
                        else:
                            turn.user_responses = []

                    file_name = f"corpus-{dataset.lower()}-{fold}-{llm_name}-run{run}.jsonl"
                    with (open(f"data/conversational-questions/{file_name}", "w+") as out_file):
                        for turn in turns:
                            out_file.write(json.dumps(dataclasses.asdict(turn)))
                            out_file.write("\n")

        del llm


if __name__ == '__main__':
    main()
