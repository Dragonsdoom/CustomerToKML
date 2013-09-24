"""
Customer To KML
Assembled by FAV on 08 06 13
Connects to a data source containing addresses,
geocodes them with Google's geocode API, and stores them in KML format.
"""

import sys
import logging
import string as strmodule
from time import sleep
import xlrd
from geocode import geocode
from dao import MSSQLDAO as DAO
from kml import KML

class CtkModel(object):
    subscribers = []        
    def addsub(self, subs):
        self.subscribers.append(subs)

    def removesub(self):
        self.subscribers.remove(subs)

    def notifysubswrite(self, data, extension, exten_desc):
        for s in self.subscribers:
            s.write(data, extension, exten_desc)
        
    def wait(self,seconds):
        """Avoid overflowing geocoder."""
        logging.info('Waiting to geocode next address (~' + str(seconds) +
                         's)..')
        sleep(seconds)

    def build_cust_addresses_dict(self,addr_component_dict):
        caddresses = {}
        for x in range(0,len(addr_component_dict['Name'])):
            address = (str(addr_component_dict['AddressLine1'][x])
                   + ', ' + str(addr_component_dict['City'][x])
                   + ', ' + str(addr_component_dict['StateProvince'][x])
                   + ' ' + str(addr_component_dict['PostalCode'][x])
                   + ', ' + str(addr_component_dict['CountryRegion'][x]))
            cname = addr_component_dict['Name'][x]
            caddresses[cname] = address
            
        return caddresses

    def xlsparse(self,xls):
        book = xlrd.open_workbook(xls)
        print book

    def dbimport(self,sName,dbName,uName,uPass):      
        dao = DAO(sName,dbName,uName,uPass)
        if dao.connect():
            dao.query()
            dao.close()
        rdict = dao.get()
        
        self.geocode_cust_addresses(self.build_cust_addresses_dict(rdict))

    def geocode_cust_addresses(self,caddresses):
        kml = KML()
        xmlroot = kml.xmlroot
        #geocode addresses
        for k,v in caddresses.items():
            logging.info('Geocoding address..')
            gcaddr = geocode(v)
            logging.info('Appending row to kml..')
            xmlroot[0].append(kml.placemark(v, k, gcaddr))
            self.wait(10)

        self.notifysubswrite(kml.serialize(xmlroot),'*.kml','Google Earth KML')
