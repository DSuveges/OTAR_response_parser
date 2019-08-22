import unittest
import pandas as pd
from OTAR_result_parser.OTAR_result_parser import OTAR_result_parser


# Building a test object:
class test_OT_response_object(object):
    test_dataframe = pd.DataFrame({'association_score.overall' : [1,2,3,4,5]})

    def to_dataframe(self):
        return(self.test_dataframe)


test_data = test_OT_response_object()

# Test block:
class Test_OTAR_result_parser(unittest.TestCase):
    test_dataFrame = test_data.to_dataframe()

    def test_init(self):
        parser = OTAR_result_parser(test_data)
        self.assertEqual(len(parser), len(self.test_dataFrame))

    def test_get_association_score_mean(self):
        parser = OTAR_result_parser(test_data)
        self.assertEqual(parser.get_association_score_mean(), self.test_dataFrame['association_score.overall'].mean())

    def test_get_association_score_min(self):
        parser = OTAR_result_parser(test_data)
        self.assertEqual(parser.get_association_score_min(), self.test_dataFrame['association_score.overall'].min())

    def test_get_association_score_max(self):
        parser = OTAR_result_parser(test_data)
        self.assertEqual(parser.get_association_score_max(), self.test_dataFrame['association_score.overall'].max())

    def test_get_association_score_std(self):
        parser = OTAR_result_parser(test_data)
        self.assertEqual(parser.get_association_score_std(), self.test_dataFrame['association_score.overall'].std())


if __name__ == '__main__':
    unittest.main()
