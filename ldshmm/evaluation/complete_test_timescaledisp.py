from unittest import TestCase
from ldshmm.evaluation.evaluate_mm import MM_Evaluation


class Timescaledisp_Test(TestCase):
    def setUp(self):
        self.evaluate = MM_Evaluation()

    def test_run_all_tests(self):
        self.evaluate.test_run_all_tests_timescaledisp()