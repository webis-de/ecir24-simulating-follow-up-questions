from llm import *

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
