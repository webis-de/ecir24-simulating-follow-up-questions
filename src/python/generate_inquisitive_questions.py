import dataclasses
import json
import os.path
from datetime import datetime

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
                conversation_turn = ConversationTurn(turn.id, turn.conversation_id, turn.system, [],
                                                     turn.previous_turns)
                conversation_turn.previous_turns.append(past_turn)

            turns.append(conversation_turn)

    return turns


@click.command()
@click.option("-d", "--dataset", "datasets", multiple=True, default=["nudged-questions", "treccast"],
              type=click.Choice(DATASETS), required=True)
@click.option("-m", "--model", "models", multiple=True, default=None, type=click.Choice(MODELS.keys()),
              required=False)
@click.option("-u", "--simulate-user", "simulate_user", default=False)
@click.option("-c", "--config", type=click.Path(exists=True, dir_okay=False), required=False, default=None)
def main(datasets, models, simulate_user, config):
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    data_conf = load_config("datasets.yml")

    if config is not None:
        run_config = load_config(config)
        datasets = run_config["datasets"]
        models = run_config["models"]
        simulate_user = run_config["simulate_user"]

    if not os.path.exists("data/conversational-questions"):
        os.makedirs("data/conversational-questions", exist_ok=True)

    user_conditions = []
    if simulate_user:
        for user in USER_TYPES:
            for question_type in QUESTION_TYPES:
                user_conditions.append((user, question_type))

        prompt_template = USER_SIM_PROMPT
    else:
        user_conditions.append((None, None))
        prompt_template = load_prompt_template("prompt-template.txt")

    start_timestamp = datetime.now().isoformat()
    runtime_log_file = open(f"data/runtime-log-{start_timestamp}.jsonl", "w")
    inference_log_file = open(f"data/inference-log-{start_timestamp}.jsonl", "w")

    for user_condition in user_conditions:
        for model in models:
            llm = MODELS[model]()

            for dataset in datasets:
                for fold in range(NUM_FOLDS):
                    if isinstance(llm, CrossValModel):
                        llm.set_test_fold(fold, NUM_FOLDS)

                    llm_name = llm.name().split("/")[-1]

                    path = data_conf[dataset]["folds_path"].format(k=fold)
                    turns = load_dataset(path)

                    for run in range(0, NUM_REPETITIONS):
                        start_timestamp = datetime.now().isoformat()
                        run_start = time.time()
                        prompts = []
                        for turn in turns:
                            if simulate_user:
                                prompt = prompt_template.format(user_condition[0], QUESTION_TYPES[user_condition[1]],
                                                                turn.system)
                            else:
                                prompt = prompt_template.format(turn.system)

                            prompts.append(prompt)

                        responses = llm.generate_all(prompts)

                        inferences = []

                        for turn, prompt, response in zip(turns, prompts, responses):
                            questions = LLM.parse_response(response)

                            inferences.append({"id": turn.id, "model": llm_name, "prompt": prompt, "response": response,
                                               "parsed": questions})
                            if questions is not None:
                                turn.user_responses = questions
                            else:
                                for _ in range(5):
                                    new_response = llm.generate(prompt)
                                    new_questions = llm.parse_response(new_response)

                                    inferences.append(
                                        {"id": turn.id, "model": llm_name, "prompt": prompt, "response": response,
                                         "parsed": questions})

                                    if new_questions is not None:
                                        turn.user_responses = new_questions
                                        break

                                if turn.user_responses is None:
                                    turn.user_responses = []

                        run_duration = time.time() - run_start

                        if isinstance(llm, CrossValModel):
                            llm_name = re.sub(r'[0-9]+$', '', llm_name)

                        if simulate_user:
                            file_name = f"corpus-{dataset.lower()}-{fold}-{llm_name}-{user_condition[0]}-{user_condition[1]}-run{run}.jsonl"
                        else:
                            file_name = f"corpus-{dataset.lower()}-{fold}-{llm_name}-run{run}.jsonl"
                        with (open(f"data/conversational-questions/{file_name}", "w+") as out_file):
                            for turn in turns:
                                out_file.write(json.dumps(dataclasses.asdict(turn)))
                                out_file.write("\n")

                        log_entry = {"start_time": start_timestamp, "dataset": dataset.lower(), "fold": fold,
                                     "model": llm_name, "run": run,
                                     "runtime": run_duration, "prompt": prompt_template}
                        runtime_log_file.write(json.dumps(log_entry))
                        runtime_log_file.write("\n")
                        runtime_log_file.flush()

                        for inference in inferences:
                            inference_log_file.write(json.dumps(inference))
                            inference_log_file.write("\n")
                            inference_log_file.flush()

            del llm

    runtime_log_file.close()


if __name__ == '__main__':
    main()
