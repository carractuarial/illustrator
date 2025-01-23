import unittest

from illustrator import functions

class Test_Functions(unittest.TestCase):

    def test_calculate_policy_year_month_1(self):
        self.assertEqual(functions.calculate_policy_year(1),1)

    def test_calculate_policy_year_month_12(self):
        self.assertEqual(functions.calculate_policy_year(12),1)
    
    def test_calculate_policy_year_month_13(self):
        self.assertEqual(functions.calculate_policy_year(13),2)

    def test_calculate_policy_year_month_1201(self):
        self.assertEqual(functions.calculate_policy_year(1201),101)

    def test_calculate_start_value(self):
        self.assertEqual(functions.calculate_start_value(1.2345),1.2345)

    def test_calculate_premium_month_1(self):
        self.assertEqual(functions.calculate_premium(1, 1234.56),1234.56)

    def test_calculate_premium_months_2to12(self):
        for i in range(2,13):
            self.assertEqual(functions.calculate_premium(i,1234.56),0)

    def test_calculate_premium_months_1to1440(self):
        for i in range(1440):
            if (i+1) % 12 == 1:
                self.assertEqual(functions.calculate_premium(i+1,1234.56),1234.56)
            else:
                self.assertEqual(functions.calculate_premium(i+1,1234.56),0)

    def test_calculate_premium_load_noprem(self):
        for r in [0, 0.1, 0.01, -1, 999]:
            self.assertEqual(functions.calculate_premium_load(0,r),0)

    def test_calculate_premium_load_0rate(self):
        for p in [0, 0.1, 0.01, -1, 999, 1234.56]:
            self.assertEqual(functions.calculate_premium_load(p, 0),0)

    def test_calculate_premium_load_5pct(self):
        p = [0, 0.1, 0.01, -1, 999, 1234.56]
        pl = [0, 0.005, 0.0005, -0.05, 49.95, 61.728]
        for i in range(len(p)):
            # self.assertEqual may fail
            self.assertAlmostEqual(functions.calculate_premium_load(p[i],0.05),pl[i])