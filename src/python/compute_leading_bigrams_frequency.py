import json
import os.path

import click
import contractions
import spacy

from constants import DATASETS, MODELS, NUM_FOLDS, NUM_REPETITIONS
from generate_inquisitive_questions import load_config


@click.command()
@click.option("-d", "--dataset", "dataset", multiple=False, default=["nudged-questions", "treccast"],
              type=click.Choice(DATASETS), required=True)
@click.option("-m", "--model", "model", multiple=False, default=None, type=click.Choice(MODELS.keys()),
              required=False)
@click.option("-k", type=int, required=True, default=10)
def main(dataset, model, k):
    dataset_conf = load_config("datasets.yml")

    run_path = "/mnt/ceph/storage/data-in-progress/data-research/conversational-search/ecir24-simulation-by-question-under-discussion/kfolds/runs"

    files = []

    if model is not None:
        for fold in range(NUM_FOLDS):
            for i in range(NUM_REPETITIONS):
                files.append(os.path.join(run_path, f"corpus-{dataset}-{fold}-{model}-run{i}.jsonl"))
    else:
        files.append(dataset_conf[dataset]["formatted_path"])

    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    bi_gram_frequencies = {}
    total_responses = 0
    for file in files:
        with open(file, "r") as in_file:
            for line in in_file:
                data = json.loads(line)

                for response in data["user_responses"]:
                    response = contractions.fix(response)

                    doc = nlp(response)

                    if len(doc) < 3:
                        continue

                    leading_bi_gram = f"{doc[0]} [{doc[1].lemma_ if not doc[1].is_punct else doc[2].lemma_}]".lower()

                    if leading_bi_gram not in bi_gram_frequencies:
                        bi_gram_frequencies[leading_bi_gram] = 0

                    bi_gram_frequencies[leading_bi_gram] += 1
                    total_responses += 1

    bi_gram_items = list(sorted(bi_gram_frequencies.items(), key=lambda item: item[1], reverse=True))
    bi_gram_items = bi_gram_items[:k]
    for i, bi_gram in enumerate(bi_gram_items):
        print(f"{i + 1:2d}. {bi_gram[0]:>20s}   {bi_gram[1] / total_responses:0.2f}")


if __name__ == '__main__':
    main()
