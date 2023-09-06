from llm import *

PROMPT_TEMPLATE = \
    ("Inquisitive questions are the questions elicited from readers as they naturally read through text. "
     "Given the text below, write an inquisitive question that you would ask if you were reading "
     "this text for the first time.\n\n"
     "### Text: {}\n"
     "### Question:")

DATASETS = {
    "inquisitive",
    "nudged_questions",
    "treccast"
}

MODELS = {
    "LLama27B": LLama27B,
    "LLama27BChat": LLama27BChat,
    "LLama213B": LLama213B,
    "LLama213BChat": LLama213BChat,
    "GODEL": GODEL,
    "Alpaca": Alpaca
}
