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
        projects_contribution = {}
        for repository in profile.repositories:
            if repository.total_additions != 0:
                projects_contribution[repository.id] = repository.user_additions / repository.total_additions
            else:
                projects_contribution[repository.id] = 1

        for skill in profile.skills:
            skill.value = skill.value * projects_contribution[skill.repository_id]
        return profile
