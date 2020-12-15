from py_fcm import TYPE_SIMPLE, join_maps, functions

from evaluator.domain import knowledge_base

from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor, STACK_EXC_REPUTATION_LAMBDA, \
    STACK_EXC_SCORE_LAMBDA


class StackExchangeEvaluator(Evaluator):

    def evaluate(self, profile: Profile, infer_skills=False) -> list:
        """
        Evaluate a profile assuming that scale_lower_bound < scale_higher_bound and scale_higher_bound > 0.
        Other values do not break the process buy may return unexpected evaluation values
        Args:
            profile: Profile to evaluate
            infer_skills: Infer skills if possible, not used in this evaluator

        Returns: List of EvaluatedSkill

        """
        evaluated_skill_list = []
        try:
            profile_reputation = int(float(profile.stats['reputation']))
        except Exception as err:
            raise Exception("Cannot load StackExchange reputation due: '" + str(err) + "'")
        reputation_contribution = functions.Activation.sigmoid_hip(profile_reputation, STACK_EXC_REPUTATION_LAMBDA)
        fcm_evaluator = knowledge_base.load_skills_fcm()
        for skill in profile.skills:
            # if the concept is already in the knowledge base there is no change when is added
            fcm_evaluator.add_concept(skill.name)
            fcm_evaluator.init_concept(skill.name, skill.value, required_presence=False)
        fcm_evaluator.run_inference()

        if infer_skills:
            result = fcm_evaluator.get_final_state(concepts_type='any')
        else:
            result = fcm_evaluator.get_final_state(concepts_type=TYPE_SIMPLE)

        for skill_name in result:
            if 0 < result[skill_name]:
                final_evaluation = result[skill_name] + (0.2 * reputation_contribution)
                if final_evaluation > 1:
                    final_evaluation = 1
                evaluated_skill_list.append(EvaluatedSkill(skill_name, final_evaluation))
        return evaluated_skill_list


class StackExchangePreprocessor(Preprocessor):

    def preprocess(self, profile: Profile) -> Profile:
        """
        The StackExchange preprocessor do nothing
        Args:
            profile: Profile to preprocess

        Returns: The same Profile object

        """
        for skill in profile.skills:
            skill.value = functions.Activation.sigmoid_hip(skill.value, STACK_EXC_SCORE_LAMBDA)
        return profile
