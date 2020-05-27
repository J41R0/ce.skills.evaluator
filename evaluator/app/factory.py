from collections import defaultdict
from evaluator.domain.profile_objects import Profile, Repository, Skill
from evaluator.domain.algorithms.default import DefaultEvaluator, DefaultPreprocessor


class ProfileFactory:
    @staticmethod
    def from_dict(profile: dict) -> Profile:
        repositories = [ProfileFactory.__repository_from(repository) for repository in profile['repositories']]
        skills = [ProfileFactory.__skill_from(skill) for skill in profile['skills']]
        evaluators = ProfileFactory.__evaluators()
        preprocessors = ProfileFactory.__preprocessors()

        generated_profile = Profile(profile['provider'],
                                    profile['stats'],
                                    repositories,
                                    skills,
                                    preprocessors[profile['provider']],
                                    evaluators[profile['provider']])
        return generated_profile

    @staticmethod
    def __repository_from(repository: dict) -> Repository:
        return Repository(repository['id'], repository['isFork'], repository['contributors'],
                          repository['totalCommits'], repository['userCommits'], repository['forks'],
                          repository['stars'], repository['views'])

    @staticmethod
    def __skill_from(skill: dict) -> Skill:
        return Skill(skill['repositoryId'], skill['name'], skill['value'])

    @staticmethod
    def __evaluators() -> dict:
        evaluators = defaultdict(DefaultEvaluator)
        return evaluators

    @staticmethod
    def __preprocessors() -> dict:
        preprocessors = defaultdict(DefaultPreprocessor)
        return preprocessors
