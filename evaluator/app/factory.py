from collections import defaultdict

from evaluator.domain.profile_objects import Profile, Repository, Skill
from evaluator.domain.algorithms.default import DefaultEvaluator, DefaultPreprocessor
from evaluator.domain.algorithms.github import GitHubEvaluator, GitHubPreprocessor
from evaluator.domain.algorithms.gitlab import GitLabEvaluator, GitLabPreprocessor


class ProfileFactory:
    @staticmethod
    def from_dict(profile: dict, custom_evaluation=True) -> Profile:
        repositories = [ProfileFactory.__repository_from(repository) for repository in profile['repositories']]
        skills = [ProfileFactory.__skill_from(skill) for skill in profile['skills']]
        evaluators = ProfileFactory.__evaluators()
        preprocessors = ProfileFactory.__preprocessors()
        if custom_evaluation:
            generated_profile = Profile(profile['provider'],
                                        profile['stats'],
                                        repositories,
                                        skills,
                                        preprocessors[str(profile['provider']).upper()],
                                        evaluators[str(profile['provider']).upper()])
        else:
            generated_profile = Profile(profile['provider'],
                                        profile['stats'],
                                        repositories,
                                        skills,
                                        DefaultPreprocessor(),
                                        DefaultEvaluator())
        return generated_profile

    @staticmethod
    def __repository_from(repository: dict) -> Repository:
        return Repository(repository['id'], repository['isFork'], repository['contributors'],
                          repository['totalCommits'], repository['userCommits'],
                          repository['forks'], repository['stars'], repository['views'],
                          repository['totalAdditions'], repository['userAdditions'])

    @staticmethod
    def __skill_from(skill: dict) -> Skill:
        return Skill(skill['repositoryId'], skill['name'], skill['value'])

    @staticmethod
    def __evaluators() -> dict:
        evaluators = defaultdict(DefaultEvaluator)
        evaluators["GITHUB"] = GitHubEvaluator()
        evaluators["GITLAB"] = GitLabEvaluator()
        return evaluators

    @staticmethod
    def __preprocessors() -> dict:
        preprocessors = defaultdict(DefaultPreprocessor)
        preprocessors["GITHUB"] = GitHubPreprocessor()
        preprocessors["GITLAB"] = GitLabPreprocessor()
        return preprocessors
