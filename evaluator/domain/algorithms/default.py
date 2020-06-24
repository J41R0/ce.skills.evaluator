from math import exp
from collections import defaultdict

from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor
from evaluator.domain.provider_processor import MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT


class DefaultEvaluator(Evaluator):

    def evaluate(self, profile: Profile) -> list:
        """
        Evaluate a profile assuming that scale_lower_bound < scale_higher_bound and scale_higher_bound > 0.
        Other values do not break the process buy may return unexpected evaluation values
        Args:
            profile: Profile to evaluate
            scale_lower_bound: Minimum scale value
            scale_higher_bound: Maximum scale value

        Returns: List of EvaluatedSkill

        """
        evaluated_skills = defaultdict(list)
        for skill in profile.skills:
            evaluation = DefaultEvaluator.__normalized_evaluation(profile.provider_name, skill.value)
            evaluated_skills[skill.name].append(evaluation)
        return DefaultEvaluator.__to_evaluated_skills(evaluated_skills)

    @staticmethod
    def __to_evaluated_skills(evaluated_skills: defaultdict):
        evaluated_skill_list = []
        for skill_name in evaluated_skills:
            evaluation = sum(evaluated_skills[skill_name]) / len(evaluated_skills[skill_name])
            evaluated_skill_list.append(EvaluatedSkill(skill_name, evaluation))
        return evaluated_skill_list

    @staticmethod
    def __normalized_evaluation(provider_name, value):
        if provider_name == "GITHUB" or provider_name == "GITLAB":
            relevance_indicator = value / MINIMUM_BYTES_OF_CODE_TO_CONSIDER_RELEVANT_PROJECT
            values_between_one_and_minus_one_exclusive = DefaultEvaluator.__sigmoid_hiperbolic(relevance_indicator)
        else:
            values_between_one_and_minus_one_exclusive = DefaultEvaluator.__sigmoid_hiperbolic(value)
        return values_between_one_and_minus_one_exclusive

    @staticmethod
    def __sigmoid_hiperbolic(val, lambda_val=0.1):
        return (1.0 - exp(-1 * lambda_val * val)) / (1.0 + exp(-1 * lambda_val * val))


class DefaultPreprocessor(Preprocessor):

    def preprocess(self, profile: Profile) -> Profile:
        """
        The default preprocessor do nothing
        Args:
            profile: Profile to preprocess

        Returns: The same Profile object

        """
        return profile
