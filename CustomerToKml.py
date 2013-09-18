"""
Customer To KML
Assembled by FAV on 08 06 13
Connects to a data source containing addresses,
geocodes them with Google's geocode API, and stores them in KML format.
"""

import sys
import logging
import Tkinter as Tk
import string as strModule
from tkFileDialog import asksaveasfile as tkAskSaveAsFile
from tkFileDialog import askopenfilename as tkAskOpenFileName
from time import sleep
from geocode import geocode
from dao import mssqldao
from kml import kml
from tkview import tkview

class ctkModel():
    subscribers = []        
    def addSubscriber(self,subs):
        self.subscribers.append(subs)

    def removeSubscriber(self,subs):
        self.subscribers.remove(subs)

    def notifySubscribers(self):
        for s in self.subscribers:
            pass
        
    def waitToAvoidOverflowingGeocoder(self,seconds):
        logging.info('Waiting to geocode next address (~' + str(seconds) +
                         's)..')
        sleep(seconds) # Don't overflow geocoder

    def buildCustomerAddressesDict(self,addrComponentDict):
        custAddresses = {}
        for x in range(0,len(addrComponentDict['Name'])):
            address = (str(addrComponentDict['AddressLine1'][x])
                   + ', ' + str(addrComponentDict['City'][x])
                   + ', ' + str(addrComponentDict['StateProvince'][x])
                   + ' ' + str(addrComponentDict['PostalCode'][x])
                   + ', ' + str(addrComponentDict['CountryRegion'][x]))
            custName = addrComponentDict['Name'][x]
            custAddresses[custName] = address
            
        return custAddresses

    def importFromExcel(self,master):
        #tkAskOpenFileName()
        pass

    def importFromDatabase(self,sName,dbName,uName,uPass):      
        dao = mssqldao(sName,dbName,uName,uPass)
        if dao.connect():
            dao.query()
            dao.close()
        resultDict = dao.get()
        
        handleGeocodingLogic(buildAddressesByCustomer(resultDict))

    def handleGeocodingLogic(self,custAddr):
        rootE = kml.initKML()
        custAddresses = custAddr
        #geocode addresses
        for k,v in custAddresses.items():
            logging.info('Geocoding address..')
            try:
                addressGCode = geocode(v)
            except Exception, e:
                logging.warning("Error while geocoding address: " + str(e))
                sys.exit()
            logging.info('Appending row to kml..')
            rootE[0].append(kml.placemark(v, k, addressGCode))
            waitToAvoidOverflowingGeocoder(10)

        write(kml.serializeKML(rootE),'*.kml','Google Earth KML')
