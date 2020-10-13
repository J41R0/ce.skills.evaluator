from collections import defaultdict

from py_fcm import TYPE_SIMPLE, join_maps, functions

from evaluator.domain import knowledge_base
from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor
from evaluator.domain.provider_processor import SRC_LAMBDA_VALUE, GITLAB_BYTES_DIFFERENCE_RATIO


class GitLabEvaluator(Evaluator):
    def evaluate(self, profile: Profile, infer_skills=True) -> list:
        """
        Evaluate a GitLab profile
        Args:
            profile: Profile to evaluate
            infer_skills: Infer skills if possible

        Returns: List of EvaluatedSkill

        """
        evaluated_skill_list = []

        projects_fcm = []

        total_project_bytes = defaultdict(int)

        skills_relation = defaultdict(list)
        for skill in profile.skills:
            skills_relation[skill.repository_id].append(skill)
            total_project_bytes[skill.repository_id] += skill.value

        for repo_id in skills_relation:
            projects_fcm.append(knowledge_base.load_providers_fcm())
            for skill in skills_relation[repo_id]:
                projects_fcm[-1].add_concept(skill.name)
                skill_value = skill.contribution_factor * total_project_bytes[skill.repository_id]
                skill_value = skill_value / GITLAB_BYTES_DIFFERENCE_RATIO
                scaled_skill_value = functions.Activation.sigmoid_hip(skill_value, SRC_LAMBDA_VALUE)
                projects_fcm[-1].init_concept(skill.name, scaled_skill_value, required_presence=False)
            projects_fcm[-1].run_inference()

        final_fcm = join_maps(projects_fcm, ignore_zeros=True, value_strategy='highest')
        if infer_skills:
            result = final_fcm.get_final_state(concepts_type='any')
        else:
            result = final_fcm.get_final_state(concepts_type=TYPE_SIMPLE)
        for skill_name in result:
            if result[skill_name] > 0:
                evaluated_skill_list.append(EvaluatedSkill(skill_name, result[skill_name]))
        return evaluated_skill_list


class GitLabPreprocessor(Preprocessor):

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

        total_project_bytes = defaultdict(int)
        for skill in profile.skills:
            total_project_bytes[skill.repository_id] += skill.value

        for skill in profile.skills:
            skill.contribution_factor = ((skill.value * projects_contribution[skill.repository_id]) /
                                         total_project_bytes[skill.repository_id])

        return profile
