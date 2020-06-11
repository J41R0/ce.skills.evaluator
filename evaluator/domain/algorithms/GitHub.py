from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor


class GitHubEvaluator(Evaluator):
    def evaluate(self, profile: Profile, scale_lower_bound: float, scale_higher_bound: float) -> list:
        """
        Evaluate a GitHub profile
        Args:
            profile: Profile to evaluate
            scale_lower_bound: Minimum scale value
            scale_higher_bound: Maximum scale value

        Returns: List of EvaluatedSkill

        """
        pass


class GitHubPreprocessor(Preprocessor):

    def preprocess(self, profile: Profile) -> Profile:
        """
        Preprocess a GitHub profile
        Args:
            profile: Profile to preprocess

        Returns: The same Profile object

        """
        pass
