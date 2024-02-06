import json
import os.path

import click
import contractions
import spacy

from constants import DATASETS, NUM_FOLDS, NUM_REPETITIONS, DATASET_DIR
from generate_followup_questions import load_config


@click.command()
@click.option("-d", "--dataset", "datasets", multiple=True, default=["trec-cast22", "webis-nudged-questions23"],
              type=click.Choice(DATASETS), required=True)
@click.option("-k", type=int, required=True, default=10)
def main(datasets, k):
    dataset_conf = load_config("datasets.yml")
    run_path = os.path.join(DATASET_DIR, "simulations")

    models = ["Llama-2-7b-hf", "Llama-2-7b-hf-tuned-on-inquisitive", "Llama-2-13b-hf"]

    print(f"{'RANK':4} {'ORIGINAL':^28s}     {models[0]: ^28s}    {models[1]: ^28s}     {models[2]: ^28s}")

    for dataset in datasets:
        print(f"For \"{dataset}\"")
        files = [dataset_conf[dataset]["formatted_path"]]

        bigrams = {}

        for j in range(len(models) + 1):
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
            bi_gram_items = list(map(lambda x: (x[0], x[1] / total_responses), bi_gram_items))
            if j == 0:
                bigrams["original"] = bi_gram_items
            else:
                bigrams[models[j - 1]] = bi_gram_items

            if j < len(models):
                files = []
                for fold in range(NUM_FOLDS):
                    for i in range(NUM_REPETITIONS):
                        files.append(os.path.join(run_path,
                                                  f"simulations-for-{dataset}-fold{fold}-with-{models[j]}-run{i}.jsonl"))

        for i in range(k):
            print(f"{i + 1:4d} {bigrams['original'][i][0]:>20s}   {bigrams['original'][i][1]:0.2f}    "
                  f"{bigrams[models[0]][i][0]:>20s}   {bigrams[models[0]][i][1]:0.2f}    "
                  f"{bigrams[models[1]][i][0]:>20s}   {bigrams[models[1]][i][1]:0.2f}    "
                  f"{bigrams[models[2]][i][0]:>20s}   {bigrams[models[2]][i][1]:0.2f}")

        print()


if __name__ == '__main__':
    main()
