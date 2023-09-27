from llm import *

DATASETS = {
    "inquisitive",
    "nudged-questions",
    "treccast"
}

MODELS = {
    "LLama27B": LLama27B,
    "LLama27BInquisitve": LLama27BInquisitive,
    "LLama27BNudgedQuestions": LLama27BNudgedQuestion,
    "LLama27BTreccast": LLama27BTreccast,
    "LLama213B": LLama213B,
    "LLama213BInquisitive": LLama213BInquisitive,
    "LLama213BNudgedQuestions": LLama213BNudgedQuestion,
    "LLama213BTreccast": LLama213BTreccast,
    "LLama27BChat": LLama27BChat,
    "LLama27BChatInquisitive": LLama27BChatInquisitive,
    "LLama213BChat": LLama213BChat,
    "LLama213BChatInquisitive": LLama213BChatInquisitive,
    "GODEL": GODEL,
    "Alpaca": Alpaca
}

NUM_REPETITIONS = 10

NUM_FOLDS = 3
