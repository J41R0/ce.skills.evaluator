from abc import ABC, abstractmethod

from py_fcm import functions

MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT = 30000
SRC_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(3 * MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT, 0.6)
DEFAULT_LAMBDA_VALUE = 0.01
MEAN_OF_BYTES_BY_LINE_OF_CODE = 47
GITLAB_BYTES_DIFFERENCE_RATIO = 25


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, profile, infer_skills) -> list:
        pass


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, profile):
        pass
