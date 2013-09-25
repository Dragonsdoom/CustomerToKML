import unittest as ut
import geocode


class TestGeocoder(ut.TestCase):
    def setUp(self):
        pass

    def test_geocode_raises_attribute_error_when_passed_none(self):
        self.assertRaises(AttributeError, geocode.geocode, None)

    def test_geocode_returns_zerozerotuple_when_passed_empty_string(self):
        self.assertEquals(geocode.geocode(''), (0, 0))

    def test_geocode_returns_something_when_passed_address(self):
        self.assertIsNotNone(geocode.geocode('496 Holly Grove School Road, '
                                             'West End, NC 27376'))

    def test_geocode_returns_tuple_when_passed_address(self):
        self.assertIs(type(geocode.geocode('496 Holly Grove School Road, '
                                      'West End, NC 27376')),
                      type(('0', '0')))

if __name__ == '__main__':
    ut.main()
