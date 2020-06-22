from collections import defaultdict

from Py_FCM import join_maps

from evaluator.domain import knowledge_base
from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor


class GitHubEvaluator(Evaluator):
    def evaluate(self, profile: Profile, scale_lower_bound: float, scale_higher_bound: float) -> list:
        """
        Evaluate a GitHub profile
        Args:
            profile: Profile to evaluate
            scale_lower_bound: Minimum scale value
            scale_higher_bound: Maximum scale value

        Returns: List of EvaluatedSkill

        """
        evaluated_skill_list = []

        projects_fcm = []
        skills_relation = defaultdict(list)
        for skill in profile.skills:
            skills_relation[skill.repository_id].append(skill)
        for repo_id in skills_relation:
            projects_fcm.append(knowledge_base.load_providers_fcm())
            for skill in skills_relation[repo_id]:
                projects_fcm[-1].init_concept(skill.name, skill.contribution_factor, required_presence=False)
            projects_fcm[-1].run_inference()

        final_fcm = join_maps(projects_fcm)
        result = final_fcm.get_final_state(nodes_type='any')
        for skill_name in result:
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
            if repository.total_additions != 0:
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
