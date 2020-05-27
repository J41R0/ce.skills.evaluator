from collections import defaultdict

from evaluator.app.factory import ProfileFactory


class SkillsEvaluation:
    def __init__(self):
        self.__skill_data = defaultdict(dict)

    def add_skill_evaluation(self, skill_name, provider, evaluation):
        if len(self.__skill_data[skill_name]) == 0:
            self.__skill_data[skill_name]['scores'] = {}
        self.__skill_data[skill_name]['scores'][provider] = evaluation
        self.__skill_data[skill_name]['name'] = skill_name

    def get_skills_data(self):
        return self.__skill_data.copy()


def evaluate_skills(profiles: list, scale_lower_bound: float, scale_higher_bound: float) -> SkillsEvaluation:
    evaluations = SkillsEvaluation()
    for profile in profiles:
        current_profile = ProfileFactory.from_dict(profile)
        evaluated_skills = current_profile.evaluate_skills(scale_lower_bound, scale_higher_bound)
        for skill in evaluated_skills:
            evaluations.add_skill_evaluation(skill.name, current_profile.provider_name, skill.value)
    return evaluations
