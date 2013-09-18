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
from datetime import date
from geocode import geocode
from dao import mssqldao
from kml import kml
from tkview import tkview

def initLogging():
    """
    This func initializes the logging activity
    """
    # begin logging program activity to file
    d = date.today()
    logging.basicConfig(filename='CustomerToKml ' + d.strftime('%m %d %y') +
                        '.log', level=logging.DEBUG)
    logging.info('Beginning run log for program..')

def waitToAvoidOverflowingGeocoder(seconds):
    logging.info('Waiting to geocode next address (~' + str(seconds) +
                     's)..')
    sleep(seconds) # Don't overflow Google's geocoder

def buildAddressesByCustomer(rDict):
    custAddresses = {}
    for x in range(0,len(rDict['Name'])):
        address = (str(rDict['AddressLine1'][x])
               + ', ' + str(rDict['City'][x])
               + ', ' + str(rDict['StateProvince'][x])
               + ' ' + str(rDict['PostalCode'][x])
               + ', ' + str(rDict['CountryRegion'][x]))
        custName = rDict['Name'][x]
        custAddresses[custName] = address
        
    return custAddresses

def importFromExcel(master):
    tkAskOpenFileName()
    master.destroy()

def importFromDatabase(master,sName,dbName,uName,uPass):
    master.destroy()
    
    dao = mssqldao(sName,dbName,uName,uPass)
    if dao.connect():
        dao.query()
        dao.close()
    resultDict = dao.get()
    
    handleGeocodingLogic(buildAddressesByCustomer(resultDict))

def handleGeocodingLogic(custAddr):
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
        
    # end program
    logging.info('..Done')
    sys.exit()

def main():
    initLogging()
    gui = tkview('Customer To KML',None,None)

    def impExCallback():
        importFromExcel(master)

    def impDBCallback():
        creds = {}
        for x in uiPairs.keys():
            creds[x] = uiPairs[x][1].get()
        importFromDatabase(master, creds['Server Name'],creds['Database Name'],creds['Database User Name'],creds['Database Password'])

    gui.mainloop()

# run program
if __name__ == "__main__":
    main()
