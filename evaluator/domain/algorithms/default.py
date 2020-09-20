from collections import defaultdict

from py_fcm.functions import Activation

from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor, DEFAULT_LAMBDA_VALUE


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
            evaluation = DefaultEvaluator.__normalized_evaluation(skill.value)
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
    def __normalized_evaluation(value):
        values_between_one_and_minus_one_exclusive = Activation.sigmoid_hip(value, lambda_val=DEFAULT_LAMBDA_VALUE)
        return values_between_one_and_minus_one_exclusive


class DefaultPreprocessor(Preprocessor):

    def preprocess(self, profile: Profile) -> Profile:
        """
        The default preprocessor do nothing
        Args:
            profile: Profile to preprocess

        Returns: The same Profile object

        """
        return profile
