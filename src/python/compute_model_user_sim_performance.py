def main():
    annotation_file = "./data/human-assessment.tsv"

    frequencies = {}

    with open(annotation_file) as in_file:
        header = in_file.readline().split()

        base_model_idx = header.index("base_model")
        tuning_idx = header.index("tuning")
        dataset_idx = header.index("dataset")
        user_exp_idx = header.index("user_experience")
        user_direction_idx = header.index("user_direction")

        naive_idx = header.index("naive")
        savvy_idx = header.index("savvy")
        implications_idx = header.index("implications")
        reasons_idx = header.index("reasons")

        for line in in_file:
            comp = line.strip().split("\t")

            base_model = comp[base_model_idx]
            dataset = comp[dataset_idx]

            user_exp = comp[user_exp_idx]
            user_direction = comp[user_direction_idx]

            tuning = comp[tuning_idx]
            if tuning == "none":
                tuning = ""

            user_cond = f"{user_exp} / {user_direction}"
            if user_cond not in frequencies:
                frequencies[user_cond] = {}

            if base_model not in frequencies[user_cond]:
                frequencies[user_cond][base_model] = {}

            if tuning not in frequencies[user_cond][base_model]:
                frequencies[user_cond][base_model][tuning] = {}

            if dataset not in frequencies[user_cond][base_model][tuning]:
                frequencies[user_cond][base_model][tuning][dataset] = {"naive": 0, "savvy": 0, "implications": 0,
                                                                       "reasons": 0, "total": 0}

            values = frequencies[user_cond][base_model][tuning][dataset]
            values["total"] += 1
            if comp[naive_idx] == "1":
                values["naive"] += 1

            if comp[savvy_idx] == "1":
                values["savvy"] += 1

            if comp[implications_idx] == "1":
                values["implications"] += 1

            if comp[reasons_idx] == "1":
                values["reasons"] += 1

    for user_cond in sorted(frequencies):
        print()
        print(user_cond)
        for base_model in sorted(frequencies[user_cond], key=str.casefold):
            for tuning in sorted(frequencies[user_cond][base_model]):
                values = frequencies[user_cond][base_model][tuning]
                print(f"{base_model:<40s} & {tuning:<20s} & "
                      f"{values['treccast']['naive'] / values['treccast']['total']:0.2f} & "
                      f"{values['nudged-questions']['naive'] / values['nudged-questions']['total']:0.2f} & "
                      f"{values['treccast']['savvy'] / values['treccast']['total']:0.2f} & "
                      f"{values['nudged-questions']['savvy'] / values['nudged-questions']['total']:0.2f} & "
                      f"{values['treccast']['implications'] / values['treccast']['total']:0.2f} & "
                      f"{values['nudged-questions']['implications'] / values['nudged-questions']['total']:0.2f} & "
                      f"{values['treccast']['reasons'] / values['treccast']['total']:0.2f} & "
                      f"{values['nudged-questions']['reasons'] / values['nudged-questions']['total']:0.2f}")


if __name__ == '__main__':
    main()
