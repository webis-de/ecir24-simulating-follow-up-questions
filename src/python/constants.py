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
    "alpaca-7b-treccast": Alpaca7BTreccast,
    "GPT4": GPT4,
}

USER_TYPES = ["savvy", "naive"]
QUESTION_TYPES = {
    "background": "You ask questions that involve definitions, causes, background information, and details.",
    "effect": "You ask questions that involve elaborations, predictions, effects, or concretizations and exemplifications."}

USER_SIM_PROMPT = """### Instruction: Follow-up questions are the questions elicited from readers as they naturally read through text. You are a {} user. {} Given the text below, write follow-up questions that you would ask if you were reading this text for the first time.

### Text: {}

### Follow-up questions:"""

NUM_REPETITIONS = 10

NUM_FOLDS = 3
