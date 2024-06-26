import json
import os.path
from typing import List

import dacite

from constants import DATASETS, NUM_FOLDS, NUM_REPETITIONS, MODELS, DATASET_DIR
from corpora import ConversationTurn
from generate_followup_questions import load_config
from similarities import Bleu, SentenceTransformerScore


def compute_sim(turn_orig: ConversationTurn, turn_gen: ConversationTurn,
                sim_function: Bleu | SentenceTransformerScore) -> List[float]:
    similarities = []
    for generated_question in turn_gen.user_responses:
        max_sim = 0.0

        for original_question in turn_orig.user_responses:
            original_question = original_question.lower()
            generated_question = generated_question.lower()

            similarity = sim_function.similarity(original_question, generated_question)
            if similarity > max_sim:
                max_sim = similarity

        similarities.append(max_sim)

    return similarities


def main():
    runs_path = os.path.join(DATASET_DIR, "simulations")
    data_conf = load_config("datasets.yml")

    bleu = Bleu()
    st = SentenceTransformerScore()

    printed_header = False
    model_names = list(MODELS.keys())

    for model in sorted(model_names, key=str.casefold):
        sims = {"bleu": {}, "sentence_bert": {}}
        for dataset in DATASETS:
            if dataset == "inquisitive":
                continue

            for fold in range(NUM_FOLDS):
                dataset_path = data_conf[dataset]["folds_path"].format(k=fold)
                dataset_file = open(dataset_path, "r")

                if not os.path.exists(dataset_path) or not os.path.isfile(dataset_path):
                    continue

                if dataset not in sims["bleu"]:
                    sims["bleu"][dataset] = []

                if dataset not in sims["sentence_bert"]:
                    sims["sentence_bert"][dataset] = []

                for run in range(NUM_REPETITIONS):
                    bleu_scores = []
                    st_scores = []
                    model_file = f"simulations-for-{dataset}-fold{fold}-with-{model}-run{run}.jsonl"
                    generated_path = os.path.join(runs_path, model_file)

                    if not os.path.exists(generated_path):
                        continue

                    with open(generated_path, "r") as generated_file:
                        dataset_file.seek(0)
                        for dataset_line, generated_line in zip(dataset_file, generated_file):
                            dataset_turn = dacite.from_dict(ConversationTurn, json.loads(dataset_line))
                            generated_turn = dacite.from_dict(ConversationTurn, json.loads(generated_line))

                            bleu_scores.extend(compute_sim(dataset_turn, generated_turn, bleu))
                            st_scores.extend(compute_sim(dataset_turn, generated_turn, st))

                    if len(bleu_scores) == 0:
                        continue

                    avg_bleu = sum(bleu_scores) / len(bleu_scores)
                    avg_st = sum(st_scores) / len(st_scores)
                    sims["bleu"][dataset].append(avg_bleu)
                    sims["sentence_bert"][dataset].append(avg_st)

        sorted_datasets = list(sorted(sims["bleu"].keys(), reverse=True))
        if not printed_header:
            print(f"{'Model':<100s}\t{'BLEU':^40s}\t{'Sentence-BERT':^40s}")
            print(
                f"{'':<100s}\t{sorted_datasets[0]:^20s} {sorted_datasets[1]:^20s}\t{sorted_datasets[0]:^20s} {sorted_datasets[1]:^20s}")
            print("".join(["-"] * 180))
            printed_header = True

        for dataset in sims["bleu"]:
            if len(sims["bleu"][dataset]) != NUM_REPETITIONS * NUM_FOLDS:
                continue
            sims["bleu"][dataset] = sum(sims["bleu"][dataset]) / len(sims["bleu"][dataset])
            sims["sentence_bert"][dataset] = sum(sims["sentence_bert"][dataset]) / len(sims["sentence_bert"][dataset])

        if isinstance(sims["bleu"]["trec-cast22"], list):
            continue

        print(
            f"{model:<100s}\t{sims['bleu'][sorted_datasets[0]]:^20.3f} {sims['bleu'][sorted_datasets[1]]:^20.3f}\t{sims['sentence_bert'][sorted_datasets[0]]:^20.3f} {sims['sentence_bert'][sorted_datasets[1]]:^20.3f}")


if __name__ == '__main__':
    main()
