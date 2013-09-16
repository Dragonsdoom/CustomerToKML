import unittest as ut
from sys import path
path.append('C:\\Users\\fvoelker\\Documents\\Customer To KML\\CustomerToKML\\')
import CustomerToKml as ctk

class TestBuildQuery(ut.TestCase):
    def setUp(self):
        pass
    def test_param_is_string(self):
        self.assertIs(type(ctk.buildQuery()),type("string"))
    def test_param_contains_sql_text(self):
        self.assertTrue('SELECT'.lower() in ctk.buildQuery().lower())

if __name__ == '__main__':
    ut.main()
