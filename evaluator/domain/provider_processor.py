from abc import ABC, abstractmethod

MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT = 50000


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, profile) -> list:
        pass


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, profile):
        pass
