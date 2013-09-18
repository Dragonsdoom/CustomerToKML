import sys
import logging
from lxml import etree

class kml():
    def initKML():
        # building root nodes
        # http://lxml.de/tutorial.html
        # https://developers.google.com/kml/documentation/kml_tut
        logging.info('Building kml in memory..')
        rootE = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        doc = etree.Element('Document')
        rootE.append(doc)
        return rootE

    # builds a kml placemark and returns the node
    def placemark(custName,address, addressGCode):
        """
        This func builds a placemark node structure for KML from params
        and returns the node.
        """
        pMark = etree.Element('Placemark')
        pMark.append(etree.Element('name'))
        pMark.append(etree.Element('description'))
        pMark.append(etree.Element('Point'))
        pMark[2].append(etree.Element('coordinates'))
        pMark[1].text = address
        pMark[0].text = custName
        pMark[2][0].text = (str(addressGCode[0]) + ',' + str(addressGCode[1]))
        return pMark

    def serializeKML(root):
        logging.info('Serializing KML in memory..')
        try:
            return etree.tostring(root,encoding="UTF-8",
                                          method="xml",
                                          xml_declaration=True,
                                          pretty_print=True)
        except Exception, e:
            logging.warning("Error while serializing addresses: " + str(e))
            sys.exit()
