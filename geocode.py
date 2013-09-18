"""Geocode address provided."""
import logging
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
    try:
        coordstr = (
            root.xpath('/GeocodeResponse/result/geometry/location/')[1],
            root.xpath('/GeocodeResponse/result/geometry/location/')[0])
        print coordstr
    except IndexError as err:
        logging.warning("Error while attempting to geocode address: " +
                        str(err) + "\nwith address: " + str(address) +
                        "\nCoordinates: " +
                        str(coords))
    return coordstr
