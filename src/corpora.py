import abc
import dataclasses
import json
import os.path
from typing import List
from zipfile import ZipFile


@dataclasses.dataclass
class PastTurn:
    index: str
    id: str
    system: str
    user_responses: List[str]


@dataclasses.dataclass
class ConversationTurn:
    id: str
    conversation_id: str
    system: str
    user_responses: List[str]
    previous_turns: List[PastTurn]

    def to_past_turn(self) -> PastTurn:
        return PastTurn(str(len(self.previous_turns) + 1),
                        self.id,
                        self.system,
                        self.user_responses)


class Corpus(metaclass=abc.ABCMeta):
    def __init__(self, base_path: str):
        self.base_path = base_path

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass

    @abc.abstractmethod
    def next_turn(self) -> ConversationTurn:
        pass

    @abc.abstractmethod
    def close(self):
        pass


class InquisitiveCorpus(Corpus):
    def __init__(self, base_path: str):
        super().__init__(base_path)
        self.articles_zip = ZipFile(os.path.join(self.base_path, "INQUISITIVE-articles.zip"))

        self.questions = open(os.path.join(self.base_path, "questions.txt"))
        self.questions.readline()
        self.question_line = self.questions.readline()

        self.article_name_queue = [a for a in self.articles_zip.namelist() if a.endswith("txt")]
        current_article_name = self.article_name_queue.pop(0)
        self.current_article_id = (current_article_name
                                   .replace("article/", "")
                                   .replace(".txt", ""))
        self.current_article = self.articles_zip.open(current_article_name, "r")
        self.article_line = None
        self.turn = None

    def has_next(self) -> bool:
        self.article_line = self.current_article.readline()
        if self.article_line:
            self.article_line = self.article_line \
                .decode("utf-8") \
                .strip()
            return True
        elif len(self.article_name_queue) > 0:
            current_article_name = self.article_name_queue.pop(0)
            self.current_article_id = (current_article_name
                                       .replace("article/", "")
                                       .replace(".txt", ""))
            self.current_article = self.articles_zip.open(current_article_name, "r")

            return self.has_next()

        return False

    def next_turn(self) -> ConversationTurn:
        split = self.article_line.split(" ")
        turn_id = f"inquisitive-{split[0]}-{self.current_article_id}"
        system = " ".join(split[1:])
        conversation_id = str(int(self.current_article_id))

        if self.turn is None or self.turn.conversation_id != conversation_id:
            self.turn = ConversationTurn(turn_id, conversation_id, system, [], [])
        else:
            past_turn = self.turn.to_past_turn()
            self.turn.id = turn_id
            self.turn.system = system
            self.turn.conversation_id = conversation_id
            self.turn.user_responses = []
            self.turn.previous_turns.append(past_turn)

        while True:
            if not self.question_line:
                break

            question_split = self.question_line.split("\t")

            if int(question_split[0]) != int(self.current_article_id):
                break

            if question_split[1] != split[0]:
                break

            self.turn.user_responses.append(question_split[4])
            self.question_line = self.questions.readline()

        return self.turn

    def close(self):
        self.current_article.close()
        self.articles_zip.close()
        self.questions.close()


class NudgedQuestionsCorpus(Corpus):
    def __init__(self, base_path: str):
        super().__init__(base_path)
        data_zip = ZipFile(os.path.join(self.base_path, "study-data.zip"))
        data_file = data_zip.open("results/results-annotated.jsonl", "r")
        self.data = []

        for line in data_file:
            self.data.extend(json.loads(line)["tasks"])

        data_file.close()
        data_zip.close()

        self.data = list(sorted(self.data, key=lambda d: d["snippet"]))

    def has_next(self) -> bool:
        return len(self.data) > 0

    def next_turn(self) -> ConversationTurn:
        turn = None
        while True:
            if len(self.data) == 0:
                return turn

            task = self.data.pop(0)

            conversation_id = hex(hash(task["snippet"]))
            id = f"nudged-questions-{conversation_id}"
            if turn is None:
                turn = ConversationTurn(id, conversation_id, task["snippet"], [], [])

            if conversation_id != turn.conversation_id:
                self.data.insert(0, task)
                return turn

            turn.user_responses.append(task["question"])

    def close(self):
        pass
