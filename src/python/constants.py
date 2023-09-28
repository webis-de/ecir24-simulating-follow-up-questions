from llm import *

DATASETS = {
    "inquisitive",
    "nudged-questions",
    "treccast"
}

MODELS = {
    "Llama-2-7b-hf": LLama27B,
    "Llama-2-7b-hf-inquisitive": LLama27BInquisitive,
    "Llama-2-7b-hf-nudged-questions": LLama27BNudgedQuestion,
    "Llama-2-7b-hf-treccast": LLama27BTreccast,
    "Llama-2-13b-hf": LLama213B,
    "Llama-2-13b-hf-inquisitive": LLama213BInquisitive,
    "Llama-2-13b-hf-nudged-questions": LLama213BNudgedQuestion,
    "Llama-2-13b-hf-treccast": LLama213BTreccast,
    "GODEL": GODEL,
    "alpaca-7b": Alpaca7B,
    "alpaca-7b-inquisitive": Alpaca7BInquisitive,
    "alpaca-7b-nudged-questions": Alpaca7BNudgedQuestions,
    "alpaca-7b-treccast": Alpaca7BTreccast
}

NUM_REPETITIONS = 10

NUM_FOLDS = 3
