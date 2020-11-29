from abc import ABC, abstractmethod

from py_fcm import functions

MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT = 30000
SRC_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(3 * MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT, 0.6)
DEFAULT_LAMBDA_VALUE = 0.01
MEAN_OF_BYTES_BY_LINE_OF_CODE = 47
GITLAB_BYTES_DIFFERENCE_RATIO = 25
STACK_EXC_MAX_REPUTATION_CONTRIBUTION = 6000
STACK_EXC_MAX_SCORE_CONTRIBUTION = 500
STACK_EXC_REPUTATION_LAMBDA = functions.Activation.sigmoid_hip_lambda(STACK_EXC_MAX_REPUTATION_CONTRIBUTION, 0.98)
STACK_EXC_SCORE_LAMBDA = functions.Activation.sigmoid_hip_lambda(STACK_EXC_MAX_REPUTATION_CONTRIBUTION, 0.98)


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, profile, infer_skills) -> list:
        pass


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, profile):
        pass
