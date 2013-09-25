""" Test suite for KML."""

import unittest as ut
import kml
from lxml import etree


class TestKML(ut.TestCase):

    """ Test the KML code for expected behaviour."""

    def test_placemark_method_makes_proper_kml_placemark(self):
        expected = "<Placemark><name>customer</name><description>" \
                   "910 Fake Address Way, West End, NC 28387</description>" \
                   "<Point><coordinates>0,0</coordinates></Point></Placemark>"
        result = kml.KML.placemark('customer',
                                   '910 Fake Address Way, West End, NC 28387',
                                   ('0', '0'))
        result_string = etree.tostring(result,
                                       method="xml",
                                       xml_declaration=False, pretty_print=False)
        self.assertEqual(result_string.strip(), expected.strip())

    def test_placemark_raises_exception_when_given_none_argument(self):
        self.assertRaises(TypeError, kml.KML.placemark, cname=None,
                          address=None, gcode=None)

    def test_serialize_method_makes_proper_kml(self):
        element = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        self.assertEqual(kml.KML.serialize(element),
                         etree.tostring(element, encoding="UTF-8",
                                        method="xml",
                                        xml_declaration=True,
                                        pretty_print=True))

    def test_serialize_raises_exception_when_given_none_argument(self):
        self.assertRaises(TypeError, kml.KML.serialize, root=None)


if __name__ == '__main__':
    ut.main()
