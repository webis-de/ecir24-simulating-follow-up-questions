import json
import os.path
import re
from typing import List

import dacite

from constants import DATASETS
from corpora import ConversationTurn
from similarities import Bleu, SentenceTransformerScore


def compute_sim(turn_orig: ConversationTurn, turn_gen: ConversationTurn,
                sim_function: Bleu | SentenceTransformerScore) -> List[float]:
    similarities = []
    for generated_question in turn_gen.user_responses:
        max_sim = 0.0

        for original_question in turn_orig.user_responses:
            original_question = original_question.lower()
            generated_question = re.sub(r"^[^a-zA-Z]+", "", generated_question).lower()
            similarity = sim_function.similarity(original_question, generated_question)
            if similarity > max_sim:
                max_sim = similarity

        similarities.append(max_sim)

    return similarities


def main():
    base_path = ("/mnt/ceph/storage/data-in-progress/data-research/conversational-search/"
                 "ecir24-simulation-by-question-under-discussion/")
    bleu = Bleu()
    st = SentenceTransformerScore()

    for dataset in DATASETS:
        dataset_path = os.path.join(base_path, f"corpus-{dataset}.jsonl")

        if not os.path.exists(dataset_path) or not os.path.isfile(dataset_path):
            continue

        model_files = [file for file in os.listdir(base_path) if file.startswith(f"corpus-{dataset}-")]

        for model_file in model_files:
            bleu_scores = []
            st_scores = []
            generated_path = os.path.join(base_path, model_file)
            with open(dataset_path, "r") as dataset_file:
                with open(generated_path, "r") as generated_file:
                    for dataset_line, generated_line in zip(dataset_file, generated_file):
                        dataset_turn = dacite.from_dict(ConversationTurn, json.loads(dataset_line))
                        generated_turn = dacite.from_dict(ConversationTurn, json.loads(generated_line))

                        bleu_scores.extend(compute_sim(dataset_turn, generated_turn, bleu))
                        st_scores.extend(compute_sim(dataset_turn, generated_turn, st))

            if len(bleu_scores) == 0:
                continue
            avg_bleu = sum(bleu_scores) / len(bleu_scores)
            avg_st = sum(st_scores) / len(st_scores)
            print(f"{model_file:<100s}\t{dataset:<20s}\t{avg_bleu:0.3f}\t{avg_st:0.3f}")


if __name__ == '__main__':
    main()
