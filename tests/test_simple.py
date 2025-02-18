import unittest

from illustrator import simple

class Test_Simple(unittest.TestCase):

    def test_as_issue_projection(self):
        gender = 'M'
        risk_class = 'NS'
        issue_age = 35
        face_amount = 100000
        annual_premium = 1255.03

        self.assertAlmostEqual(simple.at_issue_projection(gender, risk_class, issue_age, face_amount, annual_premium), 132184.0427, places=4)