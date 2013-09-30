""" Model high-level logic for MVC pattern."""

import logging
from time import sleep
import xlrd
from geocode import geocode
from dao import MSSQLDAO as DAO
from kml import KML


class CtkModel(object):

    """MVC Model for program."""

    subscribers = []

    def addsub(self, sub):
        """Add subscriber - publisher/subscriber model"""
        self.subscribers.append(sub)

    def removesub(self, sub):
        """Remove subscriber - publisher/subscriber model"""
        self.subscribers.remove(sub)

    def notifysubswrite(self, data, extension, exten_desc):
        """Notify subscribers of write to file."""
        for sub in self.subscribers:
            sub.write(data, extension, exten_desc)

    @staticmethod
    def wait(seconds):
        """Avoid overflowing geocoder."""
        logging.info('Waiting to geocode next address (~' + str(seconds) +
                     's)..')
        sleep(seconds)

    @staticmethod
    def build_cust_addresses_dict(addr_component_dict):
        """Build a dict of customer keys and address values"""
        caddresses = {}
        for x in range(0, len(addr_component_dict['Name'])):
            address = (str(addr_component_dict['AddressLine1'][x])
                       + ', ' + str(addr_component_dict['City'][x])
                       + ', ' + str(addr_component_dict['StateProvince'][x])
                       + ' ' + str(addr_component_dict['PostalCode'][x])
                       + ', ' + str(addr_component_dict['CountryRegion'][x]))
            cname = addr_component_dict['Name'][x]
            caddresses[cname] = address

        return caddresses

    @staticmethod
    def xlsparse(xls, sheet_index=0, header_row_index=0):
        """
        Open a sheet of a book, read in the specific row as a header,
        and read in each column from that row down as data for that column.
        """
        data = {}
        with xlrd.open_workbook(xls) as book:
            sheet = book.sheet_by_index(sheet_index)
        for index, cvalue in enumerate(sheet.row_values(header_row_index)):
            data[cvalue] = sheet.col_values(index, header_row_index + 1)
        return data

    @staticmethod
    def dbimport(sname, dbname, uname, upass):
        """Import data from db using DAO"""
        dao = DAO(sname, dbname, uname, upass)
        if dao.connect():
            dao.query()
            dao.close()
        rdict = dao.get()
        return rdict

    def geocode_cust_addresses(self, caddresses):
        """Geocode all addresses from a customer dict."""
        kml = KML()
        xmlroot = kml.xmlroot
        # geocode addresses
        for key, value in caddresses.items():
            logging.info('Geocoding address..')
            gcaddr = geocode(value)
            logging.info('Appending row to kml..')
            xmlroot[0].append(kml.placemark(key, value, gcaddr))
            self.wait(10)

        self.notifysubswrite(
            kml.serialize(xmlroot), '*.kml', 'Google Earth KML')
