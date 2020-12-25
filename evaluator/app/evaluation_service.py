from collections import defaultdict

from py_fcm import join_maps, TYPE_SIMPLE

from evaluator.app.factory import ProfileFactory
from evaluator.domain import knowledge_base


class SkillsEvaluation:
    def __init__(self, scale_lower_bound: float, scale_higher_bound: float):
        self.__skill_data = defaultdict(dict)
        self.__scale_lower_bound = scale_lower_bound
        self.__scale_higher_bound = scale_higher_bound

    def __scale_value(self, value: float) -> float:
        """
        Scale evaluator result in input value to use only the [0,1] range of sigmoid hip function output
        Args:
            value: Evaluation result

        Returns: Scaled evaluation result to desired range

        """
        scaled_in_one_to_zero_range = 0
        if value > 0:
            scaled_in_one_to_zero_range = value

        values_range = self.__scale_higher_bound
        if self.__scale_higher_bound <= 0 and self.__scale_lower_bound < 0:
            values_range = abs(self.__scale_higher_bound - self.__scale_lower_bound)
        elif self.__scale_higher_bound > 0 and self.__scale_lower_bound > 0:
            values_range = self.__scale_higher_bound - self.__scale_lower_bound
        elif self.__scale_lower_bound < 0 < self.__scale_higher_bound:
            values_range = abs(self.__scale_higher_bound) + abs(self.__scale_lower_bound)

        pseudo_scaled_value = scaled_in_one_to_zero_range * values_range
        skill_evaluation_scaled = self.__scale_lower_bound + pseudo_scaled_value
        return skill_evaluation_scaled

    def add_skill_evaluation(self, skill_name: str, provider: str, evaluation: float):
        if len(self.__skill_data[skill_name]) == 0:
            self.__skill_data[skill_name]['scores'] = {}
        self.__skill_data[skill_name]['scores'][provider] = self.__scale_value(evaluation)
        self.__skill_data[skill_name]['name'] = skill_name

    def add_skill_final_evaluation(self, skill_name: str, evaluation: float):
        self.__skill_data[skill_name]['final_evaluation'] = self.__scale_value(evaluation)

    def get_skills_data(self):
        return self.__skill_data.copy()


def evaluate_providers_skills(profiles: list, scale_lower_bound: float, scale_higher_bound: float,
                              infer_skills=True, custom_evaluation=True) -> SkillsEvaluation:
    evaluations = SkillsEvaluation(scale_lower_bound, scale_higher_bound)
    evaluations_fcm_list = []
    for profile in profiles:
        current_profile = ProfileFactory.from_dict(profile, custom_evaluation)
        evaluated_skills = current_profile.evaluate_skills(infer_skills)
        evaluations_fcm_list.append(knowledge_base.load_skills_fcm())
        for skill in evaluated_skills:
            evaluations.add_skill_evaluation(skill.name, current_profile.provider_name, skill.value)
            evaluations_fcm_list[-1].add_concept(skill.name)
            evaluations_fcm_list[-1].init_concept(skill.name, skill.value)
        evaluations_fcm_list[-1].run_inference()

    final_evaluator_fcm = join_maps(evaluations_fcm_list, ignore_zeros=True, value_strategy='highest')
    final_evaluator_fcm.set_map_decision_function("EXITED")
    final_evaluator_fcm.run_inference()
    if infer_skills:
        final_evaluation = final_evaluator_fcm.get_final_state(concepts_type='any')
    else:
        final_evaluation = final_evaluator_fcm.get_final_state(concepts_type=TYPE_SIMPLE)
    for skill_name in final_evaluation:
        evaluations.add_skill_final_evaluation(skill_name, final_evaluation[skill_name])

    return evaluations
