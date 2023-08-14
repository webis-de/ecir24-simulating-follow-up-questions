import abc
import re
from enum import Enum
from typing import List, Optional

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import transformers
import torch
import logging
import sys

from logger import StdOutLogger


class Param(Enum):
    SEVEN_B = "7b"
    THIRTEEN_B = "13b"


class LLM(metaclass=abc.ABCMeta):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Loading model " + self.__class__.__name__)
        sys.stdout = StdOutLogger(self.logger.info)

    def __del__(self):
        sys.stdout = sys.__stdout__

    @abc.abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def parse_response(response: str) -> Optional[List[str]]:
        pass

    @abc.abstractmethod
    def name(self) -> str:
        pass


class LLama2(LLM):

    def __init__(self, param: Param = Param.SEVEN_B):
        super().__init__()
        self.model_name = f"meta-llama/Llama-2-{param.value}-chat-hf"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )

    def generate(self, prompt: str) -> str:
        sequences = self.pipeline(
            prompt,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=500
        )

        for seq in sequences:
            return seq["generated_text"]

    def name(self) -> str:
        return self.model_name

    @staticmethod
    def parse_response(response: str):
        questions = []
        line_split = response.split("\n")
        for line in line_split:
            line = line.strip()
            if re.match("^[0-9].*", line):
                questions.append(re.sub("^[0-9]+\\.\\s", "", line))

        if len(questions) > 0:
            return questions

        return None


class LLama27B(LLama2):
    def __init__(self):
        super().__init__()


class GODEL(LLM):

    def __init__(self):
        super().__init__()
        self.model_name = "microsoft/GODEL-v1_1-large-seq2seq"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def generate(self, prompt: str) -> str:
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        outputs = self.model.generate(
            input_ids,
            do_sample=True,
            top_p=0.9,
            max_length=500
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def name(self) -> str:
        return self.model_name

    @staticmethod
    def parse_response(response: str) -> Optional[List[str]]:
        questions = []
        for line in response.split("\n"):
            questions.append(line)

        if len(questions) > 0:
            return questions

        return None
