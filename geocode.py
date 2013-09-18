import urllib
from lxml import etree

# https://developers.google.com/kml/articles/geocodingforkml
def geocode(address):
    """
    This func takes an address as a string for geocoding via Google's
    geocode api and returns either the value or (0,0).
    """
    mapsUrl = ('http://maps.googleapis.com/maps/api/geocode/xml?address=' +
    address.replace(' ','+') + '&sensor=false')

    coords = urllib.urlopen(mapsUrl).read()
    root = etree.fromstring(coords)

    coordText = (0,0)
    try:
        coordText = (root.xpath('/GeocodeResponse/result/geometry/location/')[1], root.xpath('/GeocodeResponse/result/geometry/location/')[0])
        print coordText
    except Exception, e:
        logging.warning("Error while attempting to geocode address: " + str(e) +
                        "\nwith address: " + str(address) + "\nCoordinates: " +
                        str(coords))
    return coordText
