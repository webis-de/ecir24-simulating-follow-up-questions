import abc
import logging
import os.path
import re
import sys
import time
from enum import Enum
from typing import List, Optional

import torch
import transformers
from chatnoir_api.chat import chat
from peft import PeftModel
from requests import HTTPError
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM

from logger import StdOutLogger

QUESTION_PATTERN = re.compile(r'(?:(?<=^)|(?<=[.!?]))([0-9]+\\.|-|[a-zA-Z]\)|\*)?[^.!?]*?\?', flags=re.MULTILINE)


class Param(Enum):
    SEVEN_B = "7b"
    THIRTEEN_B = "13b"
    SEVENTY_B = "70b"


class LLM(metaclass=abc.ABCMeta):
    TUNED_BASE_PATH = "/mnt/ceph/storage/data-in-progress/data-research/conversational-search/ecir24-simulation-by-question-under-discussion/kfolds/models"

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Loading model " + self.__class__.__name__)
        sys.stdout = StdOutLogger(self.logger.info)

    def __del__(self):
        sys.stdout = sys.__stdout__

    @abc.abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    def generate_all(self, prompts: List[str]) -> List[str]:
        return [self.generate(x) for x in prompts]

    @staticmethod
    @abc.abstractmethod
    def parse_response(response: str) -> Optional[List[str]]:
        pass

    @abc.abstractmethod
    def name(self) -> str:
        pass


class LLama2(LLM):

    def __init__(self, param: Param = Param.SEVEN_B, chat: bool = True, model_name: str = None, tuning: str = None):
        super().__init__()

        self.model_name = model_name
        if self.model_name is None:
            if chat:
                chat_str = "-chat"
            else:
                chat_str = ""

            self.model_name = f"meta-llama/Llama-2-{param.value}{chat_str}-hf"

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        if tuning is not None:
            weight_dir = f"{self.model_name.split('/')[-1]}-{tuning}"
            merged_model = PeftModel.from_pretrained(self.model, os.path.join(LLM.TUNED_BASE_PATH, weight_dir))
            merged_model = merged_model.merge_and_unload()
            self.model = merged_model

        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
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
            max_new_tokens=150
        )

        for seq in sequences:
            return seq["generated_text"]

    def generate_all(self, prompts: List[str]) -> List[str]:
        response = self.pipeline(
            prompts,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            max_new_tokens=150
        )

        results = []
        for sequence in response:
            for seq in sequence:
                results.append(seq["generated_text"])

        return results

    def name(self) -> str:
        return self.model_name

    @staticmethod
    def parse_response(response: str):
        questions = set()
        line_split = response.split("\n")
        for line in line_split:
            line = line.strip()
            matches = re.finditer(QUESTION_PATTERN, line)
            for match in matches:
                question = match.group(0).strip()
                if len(question) > 0:
                    question = re.sub(r"^Q[0-9:]+", "", question)
                    question = re.sub(r"^[^a-zA-Z]+", "", question)
                    questions.add(question.strip())

        if len(questions) > 0:
            return list(questions)

        return None


class LLama27B(LLama2):
    def __init__(self):
        super().__init__(Param.SEVEN_B, False)


class LLama27BChat(LLama2):
    def __init__(self):
        super().__init__(Param.SEVEN_B, True)


class LLama27BInquisitive(LLama2):
    def __init__(self):
        super().__init__(Param.SEVEN_B, False, tuning="inquisitive")


class LLama27BChatInquisitive(LLama2):
    def __init__(self):
        super().__init__(Param.SEVEN_B, True, tuning="inquisitive")


class LLama27BNudgedQuestion(LLama2):
    def __init__(self, folds: str):
        super().__init__(Param.SEVEN_B, False, tuning=f"nudged-questions{folds}")


class LLama27BChatNudgedQuestion(LLama2):
    def __init__(self, folds: str):
        super().__init__(Param.SEVEN_B, True, tuning=f"nudged-questions{folds}")


class LLama213BInquisitive(LLama2):
    def __init__(self):
        super().__init__(Param.THIRTEEN_B, False, tuning="inquisitive")


class LLama213BChatInquisitive(LLama2):
    def __init__(self):
        super().__init__(Param.THIRTEEN_B, True, tuning="inquisitive")


class LLama213B(LLama2):
    def __init__(self):
        super().__init__(Param.THIRTEEN_B, False)


class LLama213BChat(LLama2):
    def __init__(self):
        super().__init__(Param.THIRTEEN_B, True)


class LLama270BChat(LLama2):
    def __init__(self):
        super().__init__(Param.SEVENTY_B, True)


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


class ChatnoirModel(Enum):
    ALPACA_7B = "alpaca-en-7b"
    GPT2_BASE = "gpt2-base"
    GPT2_LARGE = "gpt2-large"
    GPT2_XL = "gpt2-xl"


class ChatnoirAPIModel(LLM):
    def __init__(self, model: ChatnoirModel):
        super().__init__()
        with open("chatnoir-token.txt") as in_file:
            self.api_key = in_file.read().strip()

        self.model_name = model.value

    def generate(self, prompt: str) -> str:
        try:
            return chat(api_key=self.api_key, input_sentence=prompt, model=self.model_name)
        except HTTPError as e:
            if e.response.status_code == 429:
                time.sleep(int(e.response.headers["Retry-After"]))
                return self.generate(prompt)
            else:
                raise e

    @staticmethod
    def parse_response(response: str) -> Optional[List[str]]:
        return LLama2.parse_response(response)

    def name(self) -> str:
        return self.model_name


class Alpaca(ChatnoirAPIModel):
    def __init__(self):
        super().__init__(ChatnoirModel.ALPACA_7B)
