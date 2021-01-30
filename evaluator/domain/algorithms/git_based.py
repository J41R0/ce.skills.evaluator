from collections import defaultdict

from py_fcm import TYPE_SIMPLE, join_maps, functions

from evaluator.domain import knowledge_base
from evaluator.domain.provider_processor import SRC_LAMBDA_VALUE, COMMITS_LAMBDA_VALUE, FORKS_LAMBDA_VALUE, \
    STARS_LAMBDA_VALUE, VIEWS_LAMBDA_VALUE
from evaluator.domain.profile_objects import Profile, EvaluatedSkill
from evaluator.domain.provider_processor import Evaluator, Preprocessor


class GitBasedEvaluator(Evaluator):
    def git_evaluate(self, profile: Profile, infer_skills=True, reduction_factor=1) -> list:
        evaluated_skill_list = []

        projects_fcm = []
        skills_relation = defaultdict(list)
        total_project_bytes = defaultdict(int)
        commits_contribution = defaultdict(float)
        fork_star_vew_contribution = defaultdict(float)
        for repo in profile.repositories:
            if repo.user_commits > 0:
                commits_contribution[repo.id] = functions.Activation.sigmoid_hip(repo.user_commits,
                                                                                 COMMITS_LAMBDA_VALUE)
            else:
                commits_contribution[repo.id] = 0
            forks_eval = functions.Activation.sigmoid_hip(repo.forks,
                                                          COMMITS_LAMBDA_VALUE)
            views_eval = functions.Activation.sigmoid_hip(repo.views,
                                                          VIEWS_LAMBDA_VALUE)
            stars_eval = functions.Activation.sigmoid_hip(repo.stars,
                                                          STARS_LAMBDA_VALUE)
            # weighted sum
            fork_star_vew_contribution[repo.id] = 0.4 * forks_eval + 0.4 * views_eval + 0.2 * stars_eval

        for skill in profile.skills:
            skills_relation[skill.repository_id].append(skill)
            total_project_bytes[skill.repository_id] += skill.value

        for repo_id in skills_relation:
            projects_fcm.append(knowledge_base.load_skills_fcm())
            for skill in skills_relation[repo_id]:
                projects_fcm[-1].add_concept(skill.name)

                skill_value = total_project_bytes[skill.repository_id] / reduction_factor
                skill_value = skill_value * skill.contribution_factor
                scaled_skill_value = functions.Activation.sigmoid_hip(skill_value, SRC_LAMBDA_VALUE)
                scaled_skill_value = scaled_skill_value * commits_contribution[skill.repository_id]

                if scaled_skill_value > 0.000001:
                    scaled_skill_value = scaled_skill_value + 0.1 * fork_star_vew_contribution[skill.repository_id]
                if scaled_skill_value > 1.0:
                    scaled_skill_value = 1.0

                projects_fcm[-1].init_concept(skill.name, scaled_skill_value, required_presence=False)
            projects_fcm[-1].run_inference()

        if len(projects_fcm) > 0:
            final_fcm = join_maps(projects_fcm, ignore_zeros=True, value_strategy='highest')
            final_fcm.set_map_decision_function("EXITED")
            if infer_skills:
                result = final_fcm.get_final_state(concepts_type='any')
            else:
                result = final_fcm.get_final_state(concepts_type=TYPE_SIMPLE)
            for skill_name in result:
                if result[skill_name] > 0:
                    evaluated_skill_list.append(EvaluatedSkill(skill_name, result[skill_name]))
        return evaluated_skill_list


class GitBasedPreprocessor(Preprocessor):

    def git_preprocess(self, profile: Profile, projects_contribution: dict) -> Profile:
        """
        Define a Git-based profile contribution factor
        Args:
            profile: Profile to preprocess

        Returns: The same Profile object

        """
        total_project_bytes = defaultdict(int)
        for skill in profile.skills:
            total_project_bytes[skill.repository_id] += skill.value

        for skill in profile.skills:
            if total_project_bytes[skill.repository_id] > 0:
                skill.contribution_factor = ((skill.value * projects_contribution[skill.repository_id]) /
                                             total_project_bytes[skill.repository_id])
            else:
                skill.contribution_factor = 1
        return profile
