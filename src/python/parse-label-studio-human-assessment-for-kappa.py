import sys, json

sys.stdout.write("turn_id\tmodel\tvalue\tannotator35\tannotator49\tannotator65\n")

combined_labels = {}
with open(sys.argv[1]) as assessment_file:
    for assessment in json.load(assessment_file):
        if len(assessment["annotations"]) > 1:
            data = assessment["data"]
            turn_id = data["id"]
            dataset = data["dataset"]

            for annotation in assessment["annotations"]:
                annotator = str(annotation["completed_by"])
                labels = {}
                comments = {}
                for result in annotation["result"]:
                    target = str(int(result["to_name"][len("user-response"):]))
                    if target not in labels:
                        labels[target] = []

                    if result["from_name"] == ("ratings" + target):
                        for label in result["value"]["choices"]:
                            labels[target].append(label)
                    elif result["from_name"] == ("direction" + target):
                        if result["value"]["number"] == -1:
                            labels[target].append("reasons")
                        elif result["value"]["number"] == 1:
                            labels[target].append("implications")
                        elif result["value"]["number"] == 0:
                            pass
                        else:
                            sys.stderr.write("Unknown value for " + turn_id + " direction" + target + ": " + str(result["value"]["number"]) + "\n")
                            exit(1)
                    elif result["from_name"] == ("expertise" + target):
                        if result["value"]["number"] == -1:
                            labels[target].append("naive")
                        elif result["value"]["number"] == 1:
                            labels[target].append("savvy")
                        elif result["value"]["number"] == 0:
                            pass
                        else:
                            sys.stderr.write("Unknown value for " + turn_id + " experience" + target + ": " + str(result["value"]["number"]) + "\n")
                            exit(1)
                    elif result["from_name"] == ("comments" + target):
                        comments[target] = result["value"]["text"][0]

                had_gpt_none_none_none = False
                for t in range(0, 32):
                    target = str(t)
                    user_response = data["user_response_" + target]
                    response_type = data["user_response_" + target + "_type"]
                    base_model = "none"
                    tuning = "none"
                    user_experience = "none"
                    user_direction = "none"
                    if response_type == "generated":
                        base_model = data["user_response_" + target + "_base_model"]
                        tuning = data["user_response_" + target + "_tuning"]
                        if tuning == "":
                            tuning = "none"
                        user_experience = data["user_response_" + target + "_user_experience"]
                        if user_experience == "":
                            user_experience = "none"
                        user_direction = data["user_response_" + target + "_user_direction"]
                        if user_direction == "":
                            user_direction = "none"
                    not_generic = "1"
                    valid = "0"
                    related = "0"
                    informative = "0"
                    naive = "0"
                    savvy = "0"
                    reasons = "0"
                    implications = "0"
                    if target in labels:
                        if "generic" in labels[target]:
                            not_generic = "0"
                        if "valid" in labels[target]:
                            valid = "1"
                        if "related" in labels[target]:
                            related = "1"
                        if "informative" in labels[target]:
                            informative = "1"
                        if "naive" in labels[target]:
                            naive = "1"
                        if "savvy" in labels[target]:
                            savvy = "1"
                        if "reasons" in labels[target]:
                            reasons = "1"
                        if "implications" in labels[target]:
                            implications = "1"
                    comment = ""
                    if target in comments:
                        comment = comments[target]

                    skip = False
                    if base_model == "gpt-4" and user_experience == "none":
                        if had_gpt_none_none_none:
                            skip = True
                        else:
                            had_gpt_none_none_none = True
                    if not skip:
                        key = f"{response_type}-{base_model}-{tuning}-{user_experience}-{user_direction}"
                        if turn_id not in combined_labels:
                            combined_labels[turn_id] = {}
                        if key not in combined_labels[turn_id]:
                            combined_labels[turn_id][key] = {
                                  "not_generic": {},
                                  "valid": {},
                                  "related": {},
                                  "informative": {},
                                  "naive": {},
                                  "savvy": {},
                                  "reasons": {},
                                  "implications": {}
                                }
                        combined_labels[turn_id][key]["not_generic"][annotator] = not_generic
                        combined_labels[turn_id][key]["valid"][annotator] = valid
                        combined_labels[turn_id][key]["related"][annotator] = related
                        combined_labels[turn_id][key]["informative"][annotator] = informative
                        combined_labels[turn_id][key]["naive"][annotator] = naive
                        combined_labels[turn_id][key]["savvy"][annotator] = savvy
                        combined_labels[turn_id][key]["reasons"][annotator] = reasons
                        combined_labels[turn_id][key]["implications"][annotator] = implications

for turn_id in combined_labels:
    for key in combined_labels[turn_id]:
        for value in combined_labels[turn_id][key]:
            sys.stdout.write(f"{turn_id}\t{key}\t{value}")
            for annotator in [ "35", "49", "65" ]:
                label = combined_labels[turn_id][key][value][annotator]
                sys.stdout.write(f"\t{label}")
            sys.stdout.write(f"\n")


