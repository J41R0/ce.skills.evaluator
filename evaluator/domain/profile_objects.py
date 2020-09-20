from evaluator.domain.provider_processor import Preprocessor, Evaluator


class Profile:
    def __init__(self, provider_name: str, stats: dict, repositories: list, skills: list, preprocessor: Preprocessor,
                 evaluator: Evaluator):
        self.provider_name = provider_name
        self.stats = stats
        self.repositories = repositories
        self.skills = skills
        self.preprocessor = preprocessor
        self.evaluator = evaluator

    def evaluate_skills(self) -> list:
        self.preprocessor.preprocess(self)
        return self.evaluator.evaluate(self)


class Repository:
    def __init__(self, repository_id: int, is_fork: bool, contributors: int, total_commits: int, user_commits: int,
                 forks: int, stars: int, views: int, total_additions: int, user_additions: int):
        self.id = repository_id
        self.is_fork = is_fork
        self.contributors = contributors
        self.total_commits = total_commits
        self.user_commits = user_commits
        self.forks = forks
        self.stars = stars
        self.views = views
        self.user_additions = user_additions
        self.total_additions = total_additions


class Skill:
    def __init__(self, repository_id: int, name: str, value: int):
        self.repository_id = repository_id
        self.name = self.__skill_name_preprocessor(name)
        self.value = value
        self.contribution_factor = 1

    def __skill_name_preprocessor(self, skill_name: str) -> str:
        return skill_name.upper()


class EvaluatedSkill:
    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value
