from abc import ABC, abstractmethod

from py_fcm import functions

MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT = 30000
SRC_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(3 * MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT, 0.6)
DEFAULT_LAMBDA_VALUE = 0.01
MEAN_OF_RELEVANT_PROJECT_COMMITS = 125
COMMITS_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(MEAN_OF_RELEVANT_PROJECT_COMMITS, 0.5)
MEAN_OF_RELEVANT_PROJECT_FROKS = 10
FORKS_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(MEAN_OF_RELEVANT_PROJECT_FROKS, 0.5)
MEAN_OF_RELEVANT_PROJECT_VIEWS = 15
VIEWS_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(MEAN_OF_RELEVANT_PROJECT_VIEWS, 0.5)
MEAN_OF_RELEVANT_PROJECT_STARS = 20
STARS_LAMBDA_VALUE = functions.Activation.sigmoid_hip_lambda(MEAN_OF_RELEVANT_PROJECT_STARS, 0.5)

GITLAB_BYTES_DIFFERENCE_RATIO = 25

STACK_EXC_MAX_REPUTATION_CONTRIBUTION = 6000
STACK_EXC_MAX_SCORE_CONTRIBUTION = 750
STACK_EXC_REPUTATION_LAMBDA = functions.Activation.sigmoid_hip_lambda(STACK_EXC_MAX_REPUTATION_CONTRIBUTION, 0.98)
STACK_EXC_SCORE_LAMBDA = functions.Activation.sigmoid_hip_lambda(STACK_EXC_MAX_SCORE_CONTRIBUTION, 0.98)


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, profile, infer_skills) -> list:
        pass


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, profile):
        pass
