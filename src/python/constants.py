from llm import *

DATASETS = {
    "inquisitive",
    "nudged_questions",
    "treccast"
}

MODELS = {
    "LLama27B": LLama27B,
    "LLama27BChat": LLama27BChat,
    "LLama27BQUD": LLama27BQUD,
    "LLama27BChatQUD": LLama27BChatQUD,
    "LLama213B": LLama213B,
    "LLama213BChat": LLama213BChat,
    "LLama213BQUD": LLama213BQUD,
    "LLama213BChatQUD": LLama213BChatQUD,
    "GODEL": GODEL,
    "Alpaca": Alpaca
}
