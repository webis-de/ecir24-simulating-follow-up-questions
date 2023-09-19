import json
import re

import click
import contractions
import spacy


@click.command()
@click.option("-f", "--file", "files", type=click.Path(exists=True, dir_okay=False), multiple=True, required=True)
@click.option("-k", type=int, required=True, default=10)
def main(files, k):
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    for file in files:
        bi_gram_frequencies = {}
        total_responses = 0

        with open(file, "r") as in_file:
            for line in in_file:
                data = json.loads(line)

                for response in data["user_responses"]:
                    response = re.sub(r"^[^a-zA-Z]+", "", response)
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
