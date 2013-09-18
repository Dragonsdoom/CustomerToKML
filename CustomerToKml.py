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
#from lxml import etree
from time import sleep
from datetime import date
from geocode import geocode
from dao import mssqldao
from kml import kml

# builds a Tk label and entry; returns a tuple of both objects
def guiLabelEntryPair(master,displayText,mask='',s=Tk.TOP):
    """
    This func creates a label and entry combination and returns them as a tuple
    """
    pLabel = Tk.Label(text = displayText)
    pLabel.pack(side=s)
    pEntry = Tk.Entry(master,show=mask)
    pEntry.pack(side=s)
    return (pLabel, pEntry)

def createGUIMaster(title):
    """
    This func creates and initalizes the tkinter GUI master object,
    then returns it
    """
    master = Tk.Tk()
    master.title(title)
    #master.geometry(geometry)
    master.lift()
    return master

def getCreds(guiMaster):
    """
    This func queries the user for database and geocoding credentials
    and returns a list of credentials
    """

    uiPairs = {}
    uiPairs['Server Name'] = guiLabelEntryPair(guiMaster,
                                "Enter server name: ")
    uiPairs['Database Name'] = guiLabelEntryPair(guiMaster,
                                "Enter database name: ")
    uiPairs['Database User Name'] = guiLabelEntryPair(guiMaster,
                                "Enter database user name: ")
    uiPairs['Database Password'] = guiLabelEntryPair(guiMaster,
                                "Enter database password: ", '*')
    uiPairs['Server Name'][1].focus()

    credentials = {}
    def callback():
        for x in uiPairs.keys():
            credentials[x] = uiPairs[x][1].get()

    button = Tk.Button(guiMaster, text="Ok", command=callback)
    button.pack(side=Tk.BOTTOM)
    Tk.mainloop()
    return credentials

def initLogging():
    """
    This func initializes the logging activity
    """
    # begin logging program activity to file
    d = date.today()
    logging.basicConfig(filename='CustomerToKml ' + d.strftime('%m %d %y') +
                        '.log', level=logging.DEBUG)
    logging.info('Beginning run log for program..')

def writeToFileWithGUIPrompt(data):
    logging.info('Requesting save location from user..')
    root = Tk.Tk()
    root.withdraw() # hides the root window

    try:
        filename = tkAskSaveAsFile(parent=root,
                                   defaultextension='.kml',
                                   filetypes=[('Google Earth KML','*.kml')],
                                   title="Save the file as...")
        logging.info('Writing to file..')
        filename.write(data)
    except IOError, e:
        logging.warning("Error while writing to file: " + str(e))
        root.destroy()
        sys.exit()
    finally:
        logging.info('Closing file IO and destroying gui..')
        filename.close()
        root.destroy()

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

    writeToFileWithGUIPrompt(kml.serializeKML(rootE))
        
    # end program
    logging.info('..Done')
    sys.exit()

def main():
    initLogging()
    master = createGUIMaster('CustomerToKML')
    uiPairs = {}
    uiPairs['Server Name'] = guiLabelEntryPair(master,
                                "Enter server name: ")
    uiPairs['Database Name'] = guiLabelEntryPair(master,
                                "Enter database name: ")
    uiPairs['Database User Name'] = guiLabelEntryPair(master,
                                "Enter database user name: ")
    uiPairs['Database Password'] = guiLabelEntryPair(master,
                                "Enter database password: ", '*')
    uiPairs['Server Name'][1].focus()

    def impExCallback():
        importFromExcel(master)

    def impDBCallback():
        creds = {}
        for x in uiPairs.keys():
            creds[x] = uiPairs[x][1].get()
        importFromDatabase(master, creds['Server Name'],creds['Database Name'],creds['Database User Name'],creds['Database Password'])
    
    impButtonDB = Tk.Button(master,text="Import From Database", command=impDBCallback)
    impButtonDB.pack()
    impButtonXLS = Tk.Button(master,text="Import From Excel", command=impExCallback)
    impButtonXLS.pack()

    master.mainloop()

# run program
if __name__ == "__main__":
    main()
