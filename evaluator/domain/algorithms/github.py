from evaluator.domain.profile_objects import Profile
from evaluator.domain.algorithms.git_based import GitBasedEvaluator, GitBasedPreprocessor


class GitHubEvaluator(GitBasedEvaluator):
    def evaluate(self, profile: Profile, infer_skills=True) -> list:
        """
        Evaluate a GitHub profile
        Args:
            profile: Profile to evaluate
            infer_skills: Infer skills if possible

        Returns: List of EvaluatedSkill

        """
        return self.git_evaluate(profile, infer_skills)


class GitHubPreprocessor(GitBasedPreprocessor):

    def preprocess(self, profile: Profile) -> Profile:
        """
        Preprocess a GitHub profile
        Args:
            profile: Profile to preprocess

        Returns: The same Profile object

        """
        projects_contribution = {}
        for repository in profile.repositories:
            if repository.total_additions != 0 and repository.user_additions != 0:
                projects_contribution[repository.id] = repository.user_additions / repository.total_additions
            else:
                projects_contribution[repository.id] = 1

        return self.git_preprocess(profile, projects_contribution)
