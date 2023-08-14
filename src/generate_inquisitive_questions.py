import os.path

from llm import LLama27B, GODEL
from constants import PROMPT_TEMPLATE, DATASET
from corpora import InquisitiveCorpus, GeneratedText
import logging
import yaml
import json


def load_config(path: str):
    with open(path, "r") as in_file:
        return yaml.safe_load(in_file)


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    data_conf = load_config("datasets.yml")

    tested_models = [GODEL, LLama27B]

    if not os.path.exists("data"):
        os.mkdir("data")

    for model in tested_models:
        llm = model()

        file_name = f"{llm.name()}-{DATASET.lower()}.jsonl".split("/")[-1]
        with open(f"data/{file_name}", "w+") as out_file:
            corpus_parser = InquisitiveCorpus(data_conf[DATASET]["path"])

            while corpus_parser.has_next():
                text = corpus_parser.next_text()
                prompt = PROMPT_TEMPLATE.format(text.content)
                response = llm.generate(prompt)
                questions = llm.parse_response(response)
                gen_text = GeneratedText(text, prompt, response, questions)
                out_file.write(json.dumps(gen_text.__dict__))
                out_file.write("\n")

        del llm


if __name__ == '__main__':
    main()
