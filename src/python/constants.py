from llm import *

DATASETS = {
    "inquisitive",
    "nudged-questions",
    "treccast"
}

MODELS = {
    "LLama27B": LLama27B,
    "LLama27BChat": LLama27BChat,
    "LLama27BInquisitve": LLama27BInquisitive,
    "LLama27BChatInquisitive": LLama27BChatInquisitive,
    "LLama213B": LLama213B,
    "LLama213BChat": LLama213BChat,
    "LLama213BInquisitive": LLama213BInquisitive,
    "LLama213BChatInquisitive": LLama213BChatInquisitive,
    "GODEL": GODEL,
    "Alpaca": Alpaca
}

NUM_REPETITIONS = 10

NUM_FOLDS = 3
