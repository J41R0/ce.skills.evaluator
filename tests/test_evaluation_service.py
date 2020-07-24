import sys
import json
import os.path
import unittest

sys.path.append('../')
from evaluator.app.evaluation_service import evaluate_skills


class EvaluationServiceTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.default_profiles = def_input_dict['profiles']
        self.scale_lower_bound = def_input_dict['scaleLowerBound']
        self.scale_higher_bound = def_input_dict['scaleHigherBound']

    def test_evaluation_service_default(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_response_path = os.path.join(current_file_path, "resources/default_evaluation_response.json")
        with open(default_evaluation_response_path, 'r') as file:
            str_result = file.read()
        expected_result = json.loads(str_result)
        skills_evaluated = evaluate_skills(self.default_profiles,
                                           self.scale_lower_bound,
                                           self.scale_higher_bound)
        func_result = skills_evaluated.get_skills_data()
        final_result = []
        for key in func_result:
            final_result.append(func_result[key])
        for element in final_result:
            self.assertIn(element, expected_result)

    def test_evaluation_service_negative_to_positive_scale_range(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_response_path = os.path.join(current_file_path, "resources/default_evaluation_response.json")
        with open(default_evaluation_response_path, 'r') as file:
            str_result = file.read()
        expected_result = json.loads(str_result)
        skills_evaluated = evaluate_skills(self.default_profiles, -3, 7)
        func_result = skills_evaluated.get_skills_data()
        final_result = []
        for key in func_result:
            final_result.append(func_result[key])
        for element in expected_result:
            for provider in element["scores"]:
                element["scores"][provider] = element["scores"][provider] - 3
        for element in final_result:
            self.assertIn(element, expected_result)

    def test_evaluation_service_negative_scale_range(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_response_path = os.path.join(current_file_path, "resources/default_evaluation_response.json")
        with open(default_evaluation_response_path, 'r') as file:
            str_result = file.read()
        expected_result = json.loads(str_result)
        skills_evaluated = evaluate_skills(self.default_profiles, -10, 0)
        func_result = skills_evaluated.get_skills_data()
        final_result = []
        for key in func_result:
            final_result.append(func_result[key])
        for element in expected_result:
            for provider in element["scores"]:
                element["scores"][provider] = element["scores"][provider] - 10
        for element in final_result:
            self.assertIn(element, expected_result)
