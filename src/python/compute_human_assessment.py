import os.path

from constants import DATASET_DIR


def main():
    annotation_file = os.path.join(DATASET_DIR, "simulation-annotations.tsv")
    frequencies = {}

    with open(annotation_file) as in_file:
        header = in_file.readline().split()

        base_model_idx = header.index("base_model")
        tuning_idx = header.index("tuning")
        dataset_idx = header.index("dataset")
        valid_idx = header.index("valid")
        related_idx = header.index("related")
        informative_idx = header.index("informative")
        specifc_idx = header.index("specific")

        user_exp_idx = header.index("user_experience")
        user_direction_idx = header.index("user_direction")

        total = 0
        for line in in_file:
            comp = line.strip().split("\t")

            if comp[user_exp_idx] != "none" and comp[user_direction_idx] != "none":
                continue

            total += 1
            base_model = comp[base_model_idx]
            tuning = comp[tuning_idx]
            if tuning == "none":
                tuning = ""
            dataset = comp[dataset_idx]

            if base_model not in frequencies:
                frequencies[base_model] = {}

            if tuning not in frequencies[base_model]:
                frequencies[base_model][tuning] = {}

            if dataset not in frequencies[base_model][tuning]:
                frequencies[base_model][tuning][dataset] = {"valid": 0, "related": 0, "informative": 0,
                                                            "specific": 0, "total": 0}

            values = frequencies[base_model][tuning][dataset]
            values["total"] += 1
            if comp[valid_idx] == "1":

                values["valid"] += 1

                if comp[related_idx] == "1":
                    values["related"] += 1

                    if comp[informative_idx] == "1":
                        values["informative"] += 1

                        if comp[specifc_idx] == "1":
                            values["specific"] += 1

    print("".join(["-"] * 125))
    print(f"{'MODEL':<59s}    {'VALID':^12s}    {'RELATED':^12s}    {'INFORMATIVE':^12s}    {'SPECIFIC':^12s}")
    print(
        f"{'Base':<30s}    {'Tuning':<25s}    {'cast':4s}    {'wnq':4s}    {'cast':4s}    {'wnq':4s}    {'cast':4s}    {'wnq':4s}    {'cast':4s}    {'wnq':4s}")
    print("".join(["-"] * 125))
    for base_model in sorted(frequencies, key=str.casefold):
        for tuning in sorted(frequencies[base_model]):
            values = frequencies[base_model][tuning]

            if base_model == "none":
                base_model = "original"
            print(f"{base_model:<30s}    {tuning:<25s}    "
                  f"{values['trec-cast22']['valid'] / values['trec-cast22']['total']:0.2f}    "
                  f"{values['webis-nudged-questions23']['valid'] / values['webis-nudged-questions23']['total']:0.2f}    "
                  f"{values['trec-cast22']['related'] / values['trec-cast22']['total']:0.2f}    "
                  f"{values['webis-nudged-questions23']['related'] / values['webis-nudged-questions23']['total']:0.2f}    "
                  f"{values['trec-cast22']['informative'] / values['trec-cast22']['total']:0.2f}    "
                  f"{values['webis-nudged-questions23']['informative'] / values['webis-nudged-questions23']['total']:0.2f}    "
                  f"{values['trec-cast22']['specific'] / values['trec-cast22']['total']:0.2f}    "
                  f"{values['webis-nudged-questions23']['specific'] / values['webis-nudged-questions23']['total']:0.2f}")

    print("".join(["-"] * 125))


if __name__ == '__main__':
    main()
