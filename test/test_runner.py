import unittest
import pandas as pd
# from OTAR_result_parser.OTAR_result_parser import OTAR_result_parser
from OTAR_result_parser.OTAR_result_parser import run_analysis


# Test block:
class Test_analysis_runner(unittest.TestCase):

    ExpectedKeys = ["queryTerm", "target-disease-pairs", "score_max", "score_min", "score_mean", "score_std"]

    wrongTerm = 'cica'
    goodTarget = 'ENSG00000197386'
    goodDisease = 'Orphanet_399'

    # Test a query that returns no association:
    def test_empty_target_search(self):
        response_data = run_analysis('target', self.wrongTerm)

        # Test if data is a dictionary:
        self.assertIsInstance(response_data, dict)

        # Test if all the keys are there:
        for key in self.ExpectedKeys:
            self.assertIn(key, response_data)

            if key == "queryTerm":
                # Test if the queryTerm is properly stored:
                self.assertEqual(self.wrongTerm, response_data[key])

            else:
                # Test if the values are None:
                self.assertIsNone(response_data[key])

    # Test a good target response:
    def test_good_target(self):
        response_data = run_analysis('target', self.goodTarget)

        for key in self.ExpectedKeys:
            self.assertIn(key, response_data)
            
            if key == "queryTerm":
                # Test if the queryTerm is properly stored:
                self.assertEqual(self.goodTarget, response_data[key])

            elif key == 'target-disease-pairs':
                # Test if the target/disease pair is a pandas dataframe:
                self.assertIsInstance(response_data[key], pd.DataFrame)

            else:
                self.assertIsInstance(response_data[key], float)

    # Test a good disease response:
    def test_goog_disase(self):
        response_data = run_analysis('disease', self.goodDisease)

        # Test dataframe that indicates the query was successful:
        self.assertIsInstance(response_data['target-disease-pairs'], pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
