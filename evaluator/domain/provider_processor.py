from abc import ABC, abstractmethod


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, profile) -> list:
        pass


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, profile):
        pass
