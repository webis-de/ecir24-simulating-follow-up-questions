import dataclasses
import json
import os.path

from corpora import InquisitiveCorpus
from generate_inquisitive_questions import load_config


def main():
    out_path = ("/mnt/ceph/storage/data-in-progress/data-research"
                "/conversational-search/ecir24-simulation-by-question-under-discussion")
    data_conf = load_config("datasets.yml")
    for dataset in data_conf:
        corpus_parser = InquisitiveCorpus(data_conf[dataset]["path"])

        with open(os.path.join(out_path, f"corpus-{dataset}.jsonl"), "w+") as out_file:
            while corpus_parser.has_next():
                turn = corpus_parser.next_turn()

                out_file.write(json.dumps(dataclasses.asdict(turn)))
                out_file.write("\n")


if __name__ == '__main__':
    main()
