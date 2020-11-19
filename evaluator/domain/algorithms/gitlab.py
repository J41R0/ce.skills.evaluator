from evaluator.domain.profile_objects import Profile
from evaluator.domain.provider_processor import GITLAB_BYTES_DIFFERENCE_RATIO
from evaluator.domain.algorithms.git_based import GitBasedEvaluator, GitBasedPreprocessor


class GitLabEvaluator(GitBasedEvaluator):
    def evaluate(self, profile: Profile, infer_skills=True) -> list:
        """
        Evaluate a GitLab profile
        Args:
            profile: Profile to evaluate
            infer_skills: Infer skills if possible

        Returns: List of EvaluatedSkill

        """
        return self.git_evaluate(profile, infer_skills, GITLAB_BYTES_DIFFERENCE_RATIO)


class GitLabPreprocessor(GitBasedPreprocessor):

    def preprocess(self, profile: Profile) -> Profile:
        """
        Preprocess a GitLab profile
        Args:
            profile: Profile to preprocess

        Returns: The same Profile object updated

        """
        projects_contribution = {}
        for repository in profile.repositories:
            if repository.total_additions != 0 and repository.user_additions != 0:
                projects_contribution[repository.id] = repository.user_additions / repository.total_additions
            elif repository.total_commits != 0 and repository.user_commits != 0:
                projects_contribution[repository.id] = repository.user_commits / repository.total_commits
            else:
                projects_contribution[repository.id] = 1

        return self.git_preprocess(profile, projects_contribution)
