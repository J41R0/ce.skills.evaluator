import sys
import json
import os.path
import unittest

sys.path.append('../')
from evaluator.app.factory import ProfileFactory
from evaluator.domain.algorithms.default import DefaultEvaluator, DefaultPreprocessor
from evaluator.domain.algorithms.github import GitHubEvaluator, GitHubPreprocessor
from evaluator.domain.algorithms.gitlab import GitLabEvaluator, GitLabPreprocessor


class DefaultEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.default_profile = ProfileFactory.from_dict(def_input_dict['profiles'][0])

    def test_evaluation_function_default(self):
        expected_result = {
            "FLUTTER": 0.5580522155596243,
            "REDHAT": 0.9961078780298288
        }
        evaluator = DefaultEvaluator()
        skills_evaluated = evaluator.evaluate(self.default_profile)
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)

    def test_evaluation_function_negative_skill_value(self):
        expected_result = {
            "FLUTTER": -0.5580522155596244,
            "REDHAT": -0.9867466055006741
        }

        default_profile_skills = self.default_profile.skills.copy()
        self.default_profile.skills[0].value = -126
        self.default_profile.skills[1].value = -501
        evaluator = DefaultEvaluator()
        skills_evaluated = evaluator.evaluate(self.default_profile)
        self.default_profile.skills = default_profile_skills
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)

    def test_default_preprocessor(self):
        preprocessor = DefaultPreprocessor()
        self.assertEqual(self.default_profile, preprocessor.preprocess(self.default_profile))

    def test_evaluation_function_git_based(self):
        expected_result = {
            "FLUTTER": 0.0007285323143711687,
            "REDHAT": 0.003607954539766182
        }
        evaluator = DefaultEvaluator()
        name_save = self.default_profile.provider_name
        self.default_profile.provider_name = "GITHUB"
        skills_evaluated = evaluator.evaluate(self.default_profile)
        self.default_profile.provider_name = name_save
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)


class GitHubEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.github_profile = ProfileFactory.from_dict(def_input_dict['profiles'][1])

    def test_preprocess_fuction(self):
        preprocessor = GitHubPreprocessor()
        preprocessor.preprocess(self.github_profile)
        self.assertEqual(0.1, self.github_profile.skills[0].contribution_factor)

    def test_evaluation_function(self):
        preprocessor = GitHubPreprocessor()
        preprocessor.preprocess(self.github_profile)
        evaluator = GitHubEvaluator()
        result = evaluator.evaluate(self.github_profile)
        for eval_sk in result:
            if eval_sk.name == "C++":
                self.assertEqual(0.5213561777638938, eval_sk.value)
            if eval_sk.name == "JAVA":
                self.assertEqual(0.5213561777638938, eval_sk.value)


class GitLabEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.gitlab_profile = ProfileFactory.from_dict(def_input_dict['profiles'][2])

    def test_preprocess_fuction(self):
        preprocessor = GitLabPreprocessor()
        preprocessor.preprocess(self.gitlab_profile)
        self.assertEqual(0.1, self.gitlab_profile.skills[0].contribution_factor)

    def test_evaluation_function(self):
        preprocessor = GitLabPreprocessor()
        preprocessor.preprocess(self.gitlab_profile)
        evaluator = GitLabEvaluator()
        result = evaluator.evaluate(self.gitlab_profile)
        for eval_sk in result:
            if eval_sk.name == "C++":
                self.assertEqual(0.26525633359279743, eval_sk.value)
            if eval_sk.name == "JAVA":
                self.assertEqual(0.5213561777638938, eval_sk.value)
