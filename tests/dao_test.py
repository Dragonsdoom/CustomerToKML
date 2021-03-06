""" Test suite for DAO."""
import unittest as ut
from dao import MSSQLDAO


class TestDAO(ut.TestCase):

    """ Test the DAO code for expected behaviour."""

    def test_closing_dao_sets_variables_to_expected_values(self):
        tdao = MSSQLDAO('server', 'database', 'uid', 'pwd')
        tdao.connected = True
        tdao.close()
        self.assertFalse(tdao.connected)

if __name__ == '__main__':
    ut.main()
