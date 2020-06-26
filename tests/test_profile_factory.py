import sys
import json
import os.path
import unittest

sys.path.append('../')
from evaluator.domain.provider_processor import Evaluator, Preprocessor
from evaluator.app.factory import ProfileFactory, Profile, Repository, Skill, DefaultEvaluator, DefaultPreprocessor


class ProfileFactoryTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.default_profile = def_input_dict['profiles'][1]

    def test_profile_generation(self):
        profile_obj = ProfileFactory.from_dict(self.default_profile)

        self.assertTrue(isinstance(profile_obj, Profile))
        self.assertEqual("GITHUB", profile_obj.provider_name)
        self.assertEqual(dict, type(profile_obj.stats))
        self.assertEqual(list, type(profile_obj.repositories))
        self.assertEqual(list, type(profile_obj.skills))
        self.assertTrue(isinstance(profile_obj.preprocessor, Preprocessor))
        self.assertTrue(isinstance(profile_obj.evaluator, Evaluator))

    def test_repository_generation(self):
        repository_obj = ProfileFactory.from_dict(self.default_profile).repositories[0]

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
        skill_obj = ProfileFactory.from_dict(self.default_profile).skills[0]

        self.assertTrue(isinstance(skill_obj, Skill))
        self.assertEqual(0, skill_obj.repository_id)
        self.assertEqual("C++", skill_obj.name)
        self.assertEqual(1000000, skill_obj.value)

    def test_default_preprocessor_generation(self):
        temp_provider = self.default_profile['provider']
        self.default_profile['provider'] = "UnknownProvider"
        preprocessor_obj = ProfileFactory.from_dict(self.default_profile).preprocessor
        self.default_profile['provider'] = temp_provider

        self.assertTrue(isinstance(preprocessor_obj, DefaultPreprocessor))

    def test_default_evaluator_generation(self):
        temp_provider = self.default_profile['provider']
        self.default_profile['provider'] = "UnknownProvider"
        evaluator_obj = ProfileFactory.from_dict(self.default_profile).evaluator
        self.default_profile['provider'] = temp_provider

        self.assertTrue(isinstance(evaluator_obj, DefaultEvaluator))
