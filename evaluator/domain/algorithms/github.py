from collections import defaultdict

from py_fcm import join_maps, functions

from evaluator.domain import knowledge_base
from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor
from evaluator.domain.provider_processor import SRC_LAMBDA_VALUE


class GitHubEvaluator(Evaluator):
    def evaluate(self, profile: Profile, infer_skills=True) -> list:
        """
        Evaluate a GitHub profile
        Args:
            profile: Profile to evaluate
            infer_skills: Infer skills if possible

        Returns: List of EvaluatedSkill

        """
        evaluated_skill_list = []

        projects_fcm = []
        skills_relation = defaultdict(list)
        total_project_bytes = defaultdict(int)
        for skill in profile.skills:
            skills_relation[skill.repository_id].append(skill)
            total_project_bytes[skill.repository_id] += skill.value

        for repo_id in skills_relation:
            projects_fcm.append(knowledge_base.load_providers_fcm())
            for skill in skills_relation[repo_id]:
                skill_value = skill.contribution_factor * total_project_bytes[skill.repository_id]
                scaled_skill_value = functions.Activation.sigmoid_hip(skill_value, SRC_LAMBDA_VALUE)
                projects_fcm[-1].init_concept(skill.name, scaled_skill_value, required_presence=False)
            projects_fcm[-1].run_inference()

        final_fcm = join_maps(projects_fcm, ignore_zeros=True)
        final_fcm.set_map_decision_function("EXITED")
        if infer_skills:
            result = final_fcm.get_final_state(nodes_type='any')
        else:
            result = final_fcm.get_final_state(nodes_type="target")
        for skill_name in result:
            if result[skill_name] > 0:
                evaluated_skill_list.append(EvaluatedSkill(skill_name, result[skill_name]))
        return evaluated_skill_list


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
            if repository.total_additions != 0 and repository.user_additions != 0:
                projects_contribution[repository.id] = repository.user_additions / repository.total_additions
            else:
                projects_contribution[repository.id] = 1

        total_project_bytes = defaultdict(int)
        for skill in profile.skills:
            total_project_bytes[skill.repository_id] += skill.value

        for skill in profile.skills:
            skill.contribution_factor = ((skill.value * projects_contribution[skill.repository_id]) /
                                         total_project_bytes[skill.repository_id])

        return profile
