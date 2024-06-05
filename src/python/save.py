from constants import MODELS

name = "Llama-2-13b-hf-tuned-on-inquisitive"
llm = MODELS[name]()
llm.model.save_pretrained(name)
llm.tokenizer.save_pretrained(name)

