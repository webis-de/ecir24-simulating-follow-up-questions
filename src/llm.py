import abc
from enum import Enum
from mlc_chat import ChatModule
import logging
import sys

from logger import StdOutLogger


class Param(Enum):
    SEVEN_B = "7b"
    THIRTEEN_B = "13b"


class LLM(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class LLama2(LLM):
    def __init__(self, param: Param = Param.SEVEN_B):
        self.logger = logging.getLogger(LLama2.__name__)
        self.logger.debug("Loading LLama2 model")
        sys.stdout = StdOutLogger(self.logger.debug)
        self.chat_mod = ChatModule(model=f"Llama-2-{param.value}-chat-hf-q4f16_1")
        sys.stdout = sys.__stdout__
        self.logger.debug("Done")

    def generate(self, prompt: str) -> str:
        gen = self.chat_mod.generate(prompt=prompt)
        self.chat_mod.reset_chat()

        return gen
