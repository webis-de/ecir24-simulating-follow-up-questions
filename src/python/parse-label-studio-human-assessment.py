import sys, json

sys.stdout.write("dataset\tturn_id\tresponse_type\tbase_model\ttuning\tuser_experience\tuser_direction\tuser_response\tnot_generic\tvalid\trelated\tinformative\tnaive\tsavvy\treasons\tinformative\tcomment\n")
with open(sys.argv[1]) as assessment_file:
    for assessment in json.load(assessment_file):
        data = assessment["data"]
        turn_id = data["id"]
        dataset = data["dataset"]

        labels = {}
        comments = {}
        for result in assessment["annotations"][0]["result"]:
            target = str(int(result["to_name"][len("user-response"):]))
            if target not in labels:
                labels[target] = []

            if result["from_name"] == ("ratings" + target):
                labels[target].append(result["value"]["choices"])
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
            elif result["from_name"] == ("experience" + target):
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
            informative = "0"
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
                if "informative" in labels[target]:
                    informative = "1"
            comment = ""
            if target in comments:
                comment = comments[target]
            sys.stdout.write(f"{dataset}\t{turn_id}\t{response_type}\t{base_model}\t{tuning}\t{user_experience}\t{user_direction}\t{user_response}\t{not_generic}\t{valid}\t{related}\t{informative}\t{naive}\t{savvy}\t{reasons}\t{informative}\t{comment}\n")

