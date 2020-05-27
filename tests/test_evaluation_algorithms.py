import sys
import json
import os.path
import unittest

sys.path.append('../')
from evaluator.domain.algorithms.default import DefaultEvaluator
from evaluator.app.factory import ProfileFactory


class DefaultEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.default_profile = ProfileFactory.from_dict(def_input_dict['profiles'][0])
        self.scale_lower_bound = def_input_dict['scale_lower_bound']
        self.scale_higher_bound = def_input_dict['scale_higher_bound']

    def test_evaluation_function_default(self):
        expected_result = {
            "C++": 8.807970779778824,
            "Java": 5.4983399731247795
        }
        evaluator = DefaultEvaluator()
        skills_evaluated = evaluator.evaluate(self.default_profile,
                                              self.scale_lower_bound,
                                              self.scale_higher_bound)
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)

    def test_evaluation_function_scale_negative_difference(self):
        expected_result = {
            "C++": 0.5231883119115297,
            "Java": -0.8006640107500882
        }

        scale_lower_bound = self.scale_lower_bound
        scale_higher_bound = self.scale_higher_bound
        self.scale_lower_bound = 3
        self.scale_higher_bound = 1
        evaluator = DefaultEvaluator()
        skills_evaluated = evaluator.evaluate(self.default_profile,
                                              self.scale_lower_bound,
                                              self.scale_higher_bound)
        self.scale_lower_bound = scale_lower_bound
        self.scale_higher_bound = scale_higher_bound

        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)

    def test_evaluation_function_negative_skill_value(self):
        expected_result = {
            "C++": 2.6894142136999513,
            "Java": 2.6894142136999513
        }

        default_profile_skills = self.default_profile.skills.copy()
        self.default_profile.skills[0].value = -500000
        self.default_profile.skills[1].value = -500000
        evaluator = DefaultEvaluator()
        skills_evaluated = evaluator.evaluate(self.default_profile,
                                              self.scale_lower_bound,
                                              self.scale_higher_bound)
        self.default_profile.skills = default_profile_skills
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)
