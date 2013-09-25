"""Geocode address provided."""
import urllib
from lxml import etree


def geocode(address):
    """
    Take an address as a string for geocoding via Google's
    geocode api and return either the value or (0,0).
    https://developers.google.com/kml/articles/geocodingforkml
    """

    mapsurl = ('http://maps.googleapis.com/maps/api/geocode/xml?address=' +
               address.replace(' ', '+') + '&sensor=false')

    coords = urllib.urlopen(mapsurl).read()
    root = etree.fromstring(coords)
    coordstr = (0, 0)
    loc = root.find(".//location")
    if not loc is None:
        coordstr = (loc[1].text, loc[0].text)
    return coordstr
