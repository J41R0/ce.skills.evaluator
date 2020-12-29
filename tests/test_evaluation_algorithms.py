import sys
import json
import os.path
import unittest

sys.path.append('../')
from evaluator.app.factory import ProfileFactory
from evaluator.domain.algorithms.default import DefaultEvaluator, DefaultPreprocessor
from evaluator.domain.algorithms.github import GitHubEvaluator, GitHubPreprocessor
from evaluator.domain.algorithms.gitlab import GitLabEvaluator, GitLabPreprocessor
from evaluator.domain.algorithms.stackexchange import StackExchangeEvaluator, StackExchangePreprocessor


class DefaultEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        self.def_input_dict = json.loads(def_input)

    def test_evaluation_function_default(self):
        default_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][0])
        expected_result = {
            "FLUTTER": 0.5580522155596243,
            "REDHAT": 0.9961078780298288
        }
        evaluator = DefaultEvaluator()
        skills_evaluated = evaluator.evaluate(default_profile)
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)

    def test_evaluation_function_negative_skill_value(self):
        default_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][0])
        expected_result = {
            "FLUTTER": -0.5580522155596244,
            "REDHAT": -0.9867466055006741
        }

        default_profile_skills = default_profile.skills.copy()
        default_profile.skills[0].value = -126
        default_profile.skills[1].value = -501
        evaluator = DefaultEvaluator()
        skills_evaluated = evaluator.evaluate(default_profile)
        default_profile.skills = default_profile_skills
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)

    def test_default_preprocessor(self):
        default_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][0])
        preprocessor = DefaultPreprocessor()
        self.assertEqual(default_profile, preprocessor.preprocess(default_profile))

    def test_evaluation_function_git_based(self):
        default_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][0])
        expected_result = {
            "FLUTTER": 0.0009704057481774696,
            "REDHAT": 0.004805783453958215
        }
        evaluator = DefaultEvaluator()
        name_save = default_profile.provider_name
        default_profile.provider_name = "GITHUB"
        skills_evaluated = evaluator.evaluate(default_profile)
        default_profile.provider_name = name_save
        self.assertEqual(expected_result[skills_evaluated[0].name], skills_evaluated[0].value)
        self.assertEqual(expected_result[skills_evaluated[1].name], skills_evaluated[1].value)

    def test_evaluation_function_zero_skills_value(self):
        default_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][0])
        preprocessor = DefaultPreprocessor()
        for skill in default_profile.skills:
            skill.value = 0
        preprocessor.preprocess(default_profile)
        evaluator = DefaultEvaluator()
        result = evaluator.evaluate(default_profile)
        self.assertEqual(0, len(result))

    def test_evaluation_function_empty_skills(self):
        default_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][0])
        preprocessor = DefaultPreprocessor()
        default_profile.skills = []
        preprocessor.preprocess(default_profile)
        evaluator = DefaultEvaluator()
        result = evaluator.evaluate(default_profile)
        self.assertEqual(0, len(result))


class GitHubEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        self.def_input_dict = json.loads(def_input)

    def test_preprocess_fuction(self):
        github_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][1])
        preprocessor = GitHubPreprocessor()
        preprocessor.preprocess(github_profile)
        self.assertEqual(0.1, github_profile.skills[0].contribution_factor)

    def test_evaluation_function(self):
        github_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][1])
        preprocessor = GitHubPreprocessor()
        preprocessor.preprocess(github_profile)
        evaluator = GitHubEvaluator()
        result = evaluator.evaluate(github_profile)
        for eval_sk in result:
            if eval_sk.name == "C++":
                self.assertEqual(0.5484283430363441, eval_sk.value)
            if eval_sk.name == "JAVA":
                self.assertEqual(0.6470245324800256, eval_sk.value)

    def test_evaluation_function_zero_skills_value(self):
        github_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][1])
        preprocessor = GitHubPreprocessor()
        for skill in github_profile.skills:
            skill.value = 0
        preprocessor.preprocess(github_profile)
        evaluator = GitHubEvaluator()
        result = evaluator.evaluate(github_profile)
        self.assertEqual(0, len(result))

    def test_evaluation_function_empty_skills(self):
        github_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][1])
        preprocessor = GitHubPreprocessor()
        github_profile.skills = []
        preprocessor.preprocess(github_profile)
        evaluator = GitHubEvaluator()
        result = evaluator.evaluate(github_profile)
        self.assertEqual(0, len(result))


class GitLabEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        self.def_input_dict = json.loads(def_input)

    def test_preprocess_fuction(self):
        gitlab_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][2])
        preprocessor = GitLabPreprocessor()
        preprocessor.preprocess(gitlab_profile)
        self.assertEqual(0.1, gitlab_profile.skills[0].contribution_factor)

    def test_evaluation_function(self):
        gitlab_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][2])
        preprocessor = GitLabPreprocessor()
        preprocessor.preprocess(gitlab_profile)
        evaluator = GitLabEvaluator()
        result = evaluator.evaluate(gitlab_profile)
        for eval_sk in result:
            if eval_sk.name == "C++":
                self.assertEqual(0.024640244562941203, eval_sk.value)
            if eval_sk.name == "JAVA":
                self.assertEqual(0.030796799479009186, eval_sk.value)

    def test_evaluation_function_zero_skills_value(self):
        gitlab_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][2])
        preprocessor = GitLabPreprocessor()
        for skill in gitlab_profile.skills:
            skill.value = 0
        preprocessor.preprocess(gitlab_profile)
        evaluator = GitLabEvaluator()
        result = evaluator.evaluate(gitlab_profile)
        self.assertEqual(0, len(result))

    def test_evaluation_function_empty_skills(self):
        gitlab_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][2])
        preprocessor = GitLabPreprocessor()
        gitlab_profile.skills = []
        preprocessor.preprocess(gitlab_profile)
        evaluator = GitLabEvaluator()
        result = evaluator.evaluate(gitlab_profile)
        self.assertEqual(0, len(result))


class StackExchangeEvaluatorTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        self.def_input_dict = json.loads(def_input)

    def test_preprocess_fuction(self):
        stack_exchange_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][3])
        preprocessor = StackExchangePreprocessor()
        preprocessor.preprocess(stack_exchange_profile)
        self.assertEqual(0.29710501384080074, stack_exchange_profile.skills[0].value)

    def test_evaluation_function(self):
        stack_exchange_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][3])
        preprocessor = StackExchangePreprocessor()
        preprocessor.preprocess(stack_exchange_profile)
        evaluator = StackExchangeEvaluator()
        result = evaluator.evaluate(stack_exchange_profile)
        for eval_sk in result:
            if eval_sk.name == "JAVA":
                self.assertEqual(0.24215496714015378, eval_sk.value)
            if eval_sk.name == "DEPENDENCY-INJECTION":
                self.assertEqual(0.30475980581088286, eval_sk.value)
            if eval_sk.name == "EJB":
                self.assertEqual(0.34606189253643604, eval_sk.value)
            if eval_sk.name == "INVERSION-OF-CONTROL":
                self.assertEqual(0.010718195620673304, eval_sk.value)
            if eval_sk.name == "SPRING":
                self.assertEqual(0.06884650863233735, eval_sk.value)

    def test_evaluation_function_zero_skills_value(self):
        stack_exchange_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][3])
        preprocessor = StackExchangePreprocessor()
        for skill in stack_exchange_profile.skills:
            skill.value = 0
        preprocessor.preprocess(stack_exchange_profile)
        evaluator = StackExchangeEvaluator()
        result = evaluator.evaluate(stack_exchange_profile)
        self.assertEqual(0, len(result))

    def test_evaluation_function_empty_skills(self):
        stack_exchange_profile = ProfileFactory.from_dict(self.def_input_dict['profiles'][3])
        preprocessor = StackExchangePreprocessor()
        stack_exchange_profile.skills = []
        preprocessor.preprocess(stack_exchange_profile)
        evaluator = StackExchangeEvaluator()
        result = evaluator.evaluate(stack_exchange_profile)
        self.assertEqual(0, len(result))
