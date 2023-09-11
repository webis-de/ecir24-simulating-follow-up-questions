from nltk.translate import bleu_score
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class Bleu:
    def __init__(self):
        self.smoothing = bleu_score.SmoothingFunction()

    def similarity(self, reference: str, hypothesis: str):
        return bleu_score.sentence_bleu([reference.split()], hypothesis.split(),
                                        smoothing_function=self.smoothing.method4)


class SentenceTransformerScore:
    def __init__(self):
        self.transformer = SentenceTransformer("paraphrase-TinyBERT-L6-v2")

    def similarity(self, reference: str, hypothesis: str):
        embeddings = self.transformer.encode([reference, hypothesis], convert_to_tensor=True)

        return cos_sim(embeddings[0], embeddings[1])[0][0].item()
