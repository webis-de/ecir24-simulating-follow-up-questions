from llm import *

DATASETS = {
    "inquisitive",
    "webis-nudged-questions23",
    "trec-cast22"
}

MODELS = {
    "Llama-2-7b-hf": LLama27B,
    "Llama-2-7b-hf-tuned-on-inquisitive": LLama27BInquisitive,
    "Llama-2-7b-tuned-on-webis-nudged-questions23": LLama27BNudgedQuestion,
    "Llama-2-7b-hf-tuned-on-trec-cast22": LLama27BTreccast,
    "Llama-2-13b-hf": LLama213B,
    "Llama-2-13b-hf-tuned-on-inquisitive": LLama213BInquisitive,
    "Llama-2-13b-tuned-on-webis-nudged-questions23": LLama213BNudgedQuestion,
    "Llama-2-13b-hf-tuned-on-trec-cast22": LLama213BTreccast,
    "alpaca-7b": Alpaca7B,
    "alpaca-7b-tuned-on-inquisitive": Alpaca7BInquisitive,
    "alpaca-7b-tuned-on-webis-nudged-questions23": Alpaca7BNudgedQuestions,
    "alpaca-7b-tuned-on-trec-cast22": Alpaca7BTreccast,
    "gpt-4": GPT4,
}

USER_TYPES = {"savvy": "elaborate", "naive": "simple"}
QUESTION_TYPES = ["reasons", "implications"]

USER_SIM_PROMPT = """### Instruction: Follow-up questions are the questions elicited from readers as they naturally read through text. You are a {} user. You ask {} questions about the {} of what was being said. Given the text below, write follow-up questions that you would ask if you were reading this text for the first time.

### Text: {}

### Follow-up questions:"""

NUM_REPETITIONS = 10

NUM_FOLDS = 3

DATASET_DIR = "data/corpus-webis-follow-up-questions-24"
