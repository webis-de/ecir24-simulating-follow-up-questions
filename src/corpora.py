import abc
import os.path
from zipfile import ZipFile


class Text:
    def __init__(self, _id: str, content: str):
        self._id = _id
        self.content = content
        self.questions = []

    def add_question(self, question: str):
        self.questions.append(question)

    def get_id(self):
        return self._id


class Corpus(metaclass=abc.ABCMeta):
    def __init__(self, base_path: str):
        self.base_path = base_path

    @abc.abstractmethod
    def has_next(self) -> bool:
        pass

    @abc.abstractmethod
    def next_text(self) -> Text:
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

        self.current_article = 1
        self.article = self.articles_zip.open("0001.txt", "r")
        self.article_line = None

    def has_next(self) -> bool:
        self.article_line = self.article.readline()
        if self.article_line:
            return True

        return False

    def next_text(self) -> Text:
        split = self.article_line.split(" ")
        _id = split[0]
        content = " ".join(split[1:])

        text = Text(_id, content)

        while True:
            if not self.question_line:
                break

            question_split = self.question_line.split("\t")

            if int(question_split[0]) != self.current_article:
                break

            if question_split[1] != text.get_id():
                break

            text.add_question(question_split[4])
            self.question_line = self.questions.readline()

        return text

    def close(self):
        self.article.close()
        self.articles_zip.close()
        self.questions.close()
