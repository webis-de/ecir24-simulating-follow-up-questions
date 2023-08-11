from llm import LLama2
from constants import PROMPT_TEMPLATE, DATASET
import logging
import yaml


def load_config(path: str):
    with open(path, "r") as in_file:
        return yaml.safe_load(in_file)


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    data_conf = load_config("datasets.yml")

    # llm = LLama2()


if __name__ == '__main__':
    main()
