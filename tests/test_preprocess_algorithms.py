import sys
import json
import os.path
import unittest

sys.path.append('../')
from evaluator.domain.algorithms.default import DefaultPreprocessor
from evaluator.app.factory import ProfileFactory


class PreprocessAlgorithmsTests(unittest.TestCase):
    def setUp(self):
        current_file_path = os.path.abspath(os.path.dirname(__file__))
        default_evaluation_input_path = os.path.join(current_file_path, "resources/default_evaluation_input.json")
        with open(default_evaluation_input_path, 'r') as file:
            def_input = file.read()

        def_input_dict = json.loads(def_input)
        self.default_profile = ProfileFactory.from_dict(def_input_dict['profiles'][0])

    def test_default_preprocessor(self):
        my_preprocessor = DefaultPreprocessor()
        result = my_preprocessor.preprocess(self.default_profile)
        self.assertEqual(self.default_profile, result)
