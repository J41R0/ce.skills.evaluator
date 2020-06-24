from collections import defaultdict

from evaluator.app.factory import ProfileFactory


class SkillsEvaluation:
    def __init__(self, scale_lower_bound: float, scale_higher_bound: float):
        self.__skill_data = defaultdict(dict)
        self.__scale_lower_bound = scale_lower_bound
        self.__scale_higher_bound = scale_higher_bound

    def __scale_value(self, value: float) -> float:
        max_positive_scale = self.__scale_higher_bound + abs(self.__scale_lower_bound)
        scaled_in_one_to_zero_range = (value + 1) / 2
        skill_evaluation_scaled = (scaled_in_one_to_zero_range * max_positive_scale) - abs(self.__scale_lower_bound)
        return skill_evaluation_scaled

    def add_skill_evaluation(self, skill_name, provider, evaluation: float):
        if len(self.__skill_data[skill_name]) == 0:
            self.__skill_data[skill_name]['scores'] = {}
        self.__skill_data[skill_name]['scores'][provider] = self.__scale_value(evaluation)
        self.__skill_data[skill_name]['name'] = skill_name

    def get_skills_data(self):
        return self.__skill_data.copy()


def evaluate_skills(profiles: list, scale_lower_bound: float, scale_higher_bound: float) -> SkillsEvaluation:
    evaluations = SkillsEvaluation(scale_lower_bound, scale_higher_bound)
    for profile in profiles:
        current_profile = ProfileFactory.from_dict(profile)
        evaluated_skills = current_profile.evaluate_skills(scale_lower_bound, scale_higher_bound)
        for skill in evaluated_skills:
            evaluations.add_skill_evaluation(skill.name, current_profile.provider_name, skill.value)
    return evaluations
