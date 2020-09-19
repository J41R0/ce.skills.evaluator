from abc import ABC, abstractmethod

from py_fcm import functions

MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT = 30000
SRC_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(7 * MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT, 0.99)
DEFAULT_LAMBDA_VALUE = 0.01


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, profile) -> list:
        pass


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, profile):
        pass
