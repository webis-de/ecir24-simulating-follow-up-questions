import dataclasses
import json
import os.path

from corpora import InquisitiveCorpus, NudgedQuestionsCorpus
from generate_inquisitive_questions import load_config


def main():
    out_path = ("/mnt/ceph/storage/data-in-progress/data-research"
                "/conversational-search/ecir24-simulation-by-question-under-discussion")
    data_conf = load_config("datasets.yml")
    parser = {"inquisitive": InquisitiveCorpus, "nudged_questions": NudgedQuestionsCorpus}

    for dataset in data_conf:
        if "original_path" not in data_conf[dataset]:
            continue

        corpus_parser = parser[dataset](data_conf[dataset]["original_path"])

        with open(os.path.join(out_path, f"corpus-{dataset}.jsonl"), "w+") as out_file:
            while corpus_parser.has_next():
                turn = corpus_parser.next_turn()

                out_file.write(json.dumps(dataclasses.asdict(turn)))
                out_file.write("\n")


if __name__ == '__main__':
    main()
