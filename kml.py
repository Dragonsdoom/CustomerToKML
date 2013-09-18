"""Generate KML files."""
import sys
import logging
from lxml import etree


class KML(object):
    """Generate KML files."""
    
    def __init__(self):
        # building root nodes
        # http://lxml.de/tutorial.html
        # https://developers.google.com/kml/documentation/kml_tut
        logging.info('Building kml in memory..')
        xmlroot = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        doc = etree.Element('Document')
        xmlroot.append(doc)
        self.xmlroot = xmlroot

    # builds a kml placemark and returns the node
    def placemark(self, cname, address, gcode):
        """
        This func builds a placemark node structure for KML from params
        and returns the node.
        """
        pmark = etree.Element('Placemark')
        pmark.append(etree.Element('name'))
        pmark.append(etree.Element('description'))
        pmark.append(etree.Element('Point'))
        pmark[2].append(etree.Element('coordinates'))
        pmark[1].text = address
        pmark[0].text = cname
        pmark[2][0].text = (str(gcode[0]) + ',' + str(gcode[1]))
        return pmark

    def serialize(self, root):
        """Serialize lxml into KML string."""
        logging.info('Serializing KML in memory..')
        try:
            return etree.tostring(root, encoding="UTF-8",
                                  method="xml",
                                  xml_declaration=True,
                                  pretty_print=True)
        except Exception as err:
            logging.warning("Error while serializing addresses: " + str(err))
            sys.exit()
