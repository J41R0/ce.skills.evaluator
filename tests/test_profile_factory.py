import sys
import json
import os.path
import unittest

sys.path.append('../')
from evaluator.domain.provider_processor import Evaluator, Preprocessor
from evaluator.app.factory import (
    ProfileFactory,
    Profile,
    Repository,
    Skill,
    DefaultEvaluator,
    DefaultPreprocessor,
    GitHubEvaluator,
    GitHubPreprocessor,
    GitLabEvaluator,
    GitLabPreprocessor)


class ProfileFactoryTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.unknown_profile = def_input_dict['profiles'][0]
        self.github_profile = def_input_dict['profiles'][1]
        self.gitlab_profile = def_input_dict['profiles'][2]

    def test_github_profile_generation(self):
        profile_obj = ProfileFactory.from_dict(self.github_profile)

        self.assertTrue(isinstance(profile_obj, Profile))
        self.assertEqual("GITHUB", profile_obj.provider_name)
        self.assertEqual(dict, type(profile_obj.stats))
        self.assertEqual(list, type(profile_obj.repositories))
        self.assertEqual(list, type(profile_obj.skills))
        self.assertTrue(isinstance(profile_obj.preprocessor, GitHubPreprocessor))
        self.assertTrue(isinstance(profile_obj.evaluator, GitHubEvaluator))

    def test_gitlab_profile_generation(self):
        profile_obj = ProfileFactory.from_dict(self.gitlab_profile)

        self.assertTrue(isinstance(profile_obj, Profile))
        self.assertEqual("GITLAB", profile_obj.provider_name)
        self.assertEqual(dict, type(profile_obj.stats))
        self.assertEqual(list, type(profile_obj.repositories))
        self.assertEqual(list, type(profile_obj.skills))
        self.assertTrue(isinstance(profile_obj.preprocessor, GitLabPreprocessor))
        self.assertTrue(isinstance(profile_obj.evaluator, GitLabEvaluator))

    def test_unknown_profile_generation(self):
        profile_obj = ProfileFactory.from_dict(self.unknown_profile)

        self.assertTrue(isinstance(profile_obj, Profile))
        self.assertEqual("UNKNOWN", profile_obj.provider_name)
        self.assertEqual(dict, type(profile_obj.stats))
        self.assertEqual(list, type(profile_obj.repositories))
        self.assertEqual(list, type(profile_obj.skills))
        self.assertTrue(isinstance(profile_obj.preprocessor, DefaultPreprocessor))
        self.assertTrue(isinstance(profile_obj.evaluator, DefaultEvaluator))

    def test_non_smart_profile_generation(self):
        profile_obj = ProfileFactory.from_dict(self.unknown_profile, custom_evaluation=False)

        self.assertTrue(isinstance(profile_obj, Profile))
        self.assertEqual("UNKNOWN", profile_obj.provider_name)
        self.assertTrue(isinstance(profile_obj.preprocessor, DefaultPreprocessor))
        self.assertTrue(isinstance(profile_obj.evaluator, DefaultEvaluator))

        profile_obj = ProfileFactory.from_dict(self.github_profile, custom_evaluation=False)

        self.assertTrue(isinstance(profile_obj, Profile))
        self.assertEqual("GITHUB", profile_obj.provider_name)
        self.assertTrue(isinstance(profile_obj.preprocessor, DefaultPreprocessor))
        self.assertTrue(isinstance(profile_obj.evaluator, DefaultEvaluator))

        profile_obj = ProfileFactory.from_dict(self.gitlab_profile, custom_evaluation=False)

        self.assertTrue(isinstance(profile_obj, Profile))
        self.assertEqual("GITLAB", profile_obj.provider_name)
        self.assertTrue(isinstance(profile_obj.preprocessor, DefaultPreprocessor))
        self.assertTrue(isinstance(profile_obj.evaluator, DefaultEvaluator))

    def test_repository_generation(self):
        repository_obj = ProfileFactory.from_dict(self.github_profile).repositories[0]

        self.assertTrue(isinstance(repository_obj, Repository))
        self.assertEqual(0, repository_obj.id)
        self.assertEqual(False, repository_obj.is_fork)
        self.assertEqual(3, repository_obj.contributors)
        self.assertEqual(1, repository_obj.forks)
        self.assertEqual(2, repository_obj.stars)
        self.assertEqual(7, repository_obj.views)
        self.assertEqual(50, repository_obj.total_commits)
        self.assertEqual(15, repository_obj.user_commits)

    def test_skill_generation(self):
        skill_obj = ProfileFactory.from_dict(self.github_profile).skills[0]

        self.assertTrue(isinstance(skill_obj, Skill))
        self.assertEqual(0, skill_obj.repository_id)
        self.assertEqual("C++", skill_obj.name)
        self.assertEqual(1000000, skill_obj.value)
