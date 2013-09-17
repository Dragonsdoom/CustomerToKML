"""
Customer To KML
Assembled by FAV on 08 06 13
Connects to a data source containing addresses,
geocodes them with Google's geocode API, and stores them in KML format.
"""
import pyodbc
import urllib
import sys
import logging
import Tkinter as Tk
import string as strModule
from tkFileDialog import asksaveasfile as tkAskSaveAsFile
from tkFileDialog import askopenfilename as tkAskOpenFileName
from lxml import etree
from time import sleep
from datetime import date


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

def sanitizeStr(dirtyStr, cleanChars):
    """
    This funct cleans the string provided and returns the cleaned string
    """
    cleanStr = ''
    for char in dirtyStr:
        if char in cleanChars:
           cleanStr += char
    return cleanStr

# incomplete!
def sanitizeCreds(creds):
    """
    This funct cleans the database credentials and returns the cleaned set.
    """
    dnsSanitary = strModule.ascii_letters + strModule.digits + '.' + '-'
    creds['Server Name'] = sanitizeStr(creds['Server Name'], dnsSanitary)
    dbSanitary = strModule.ascii_letters + strModule.digits + '_'
    creds['Database Name'] = sanitizeStr(creds['Database Name'], dbSanitary)
    creds['Database User Name'] = sanitizeStr(
        creds['Database User Name'],
        strModule.printable)
    creds['Database Password'] = sanitizeStr(
        creds['Database Password'],
        strModule.printable)
    return creds

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

class dao():
    def __init__(self):
        pass
    def prepare(self):
        pass
    def connect(self):
        pass
    def query(self):
        pass
    def get(self):
        pass
    def close(self):
        pass

class mssqldao(dao):
    connected = False
    connStr = ''
    statement = ''
    results = {}

    def __init__(self,server,database,uid,pwd):
        self.connStr = ('driver={SQL Server};server=' + server + ';database=' +
        database + ';uid=' + uid + ';pwd=' + pwd)
        self.statement = self.prepare()
    
    def prepare(self):
        return """SELECT Company.Name
        ,Company.Description
        ,AddressLine1
        ,AddressLine2
        ,City
        ,PostalCode
        ,CountryRegion.Name AS CountryRegion
        ,StateProvince.Name AS StateProvince
        FROM Titan.Titan.Address 
        INNER JOIN Titan.Titan.Company 
			ON Titan.Titan.Company.DefaultAddressId=Titan.Titan.Address.AddressId
		INNER JOIN Titan.Titan.StateProvince ON Address.StateProvinceId = StateProvince.StateProvinceId
		INNER JOIN Titan.Titan.CountryRegion ON Address.CountryRegionId = CountryRegion.CountryRegionId
        WHERE Titan.Titan.Company.CompanyId IN (
			SELECT Titan.Titan.Customer.CustomerId
			FROM Titan.Titan.Customer
			WHERE Titan.Titan.Customer.Active = 1)"""

    def connect(self):
        if self.connStr:
            # open database connection
            # https://code.google.com/p/pyodbc/wiki/GettingStarted
            logging.info('Opening connection to database..')
            try:
                self.connection = pyodbc.connect(self.connStr)
            except Exception, e:
                logging.warning("Error while connecting to database: " + str(e))
                sys.exit()
            self.cursor = self.connection.cursor()
            self.connected=True
            return True
        else:
            return False

    def query(self):
        if self.cursor and self.query:
            self.results = {}
            logging.info('Executing query..')
            try:
                self.cursor.execute(self.statement)
            except Exception, e:
                logging.warning("Error while querying database: " + str(e))
                sys.exit()
            rows = self.cursor.fetchall()
            cols = []
            #get cols from cursor
            for x in range(0,len(self.cursor.description)):
                cols.append(self.cursor.description[x][0])
            #set up lists in result dict
            for col in cols:    
                self.results[col] = []
            #add results to lists in dict by column
            for x in range(0,len(rows)):
                for y in range(0, len(cols)):
                    self.results[cols[y]].append(rows[x][y])
            return True
        else:
            return False

    def get(self):
        if self.results:
            return self.results
        else:
            raise ValueError
    
    def close(self):
        if self.connection:
            logging.info('Closing connection to database..')
            try:
                self.connection.close()
            except Exception, e:
                logging.warning("Error while writing to file: " + str(e))
                sys.exit()
            self.connected = False
            return True
        else:
            return False

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
    rootE = initKML()
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
        rootE[0].append(placemark(v, k, addressGCode))
        waitToAvoidOverflowingGeocoder(10)

    writeToFileWithGUIPrompt(serializeKML(rootE))
        
    # end program
    logging.info('..Done')
    sys.exit()

def initKML():
    # building root nodes
    # http://lxml.de/tutorial.html
    # https://developers.google.com/kml/documentation/kml_tut
    logging.info('Building kml in memory..')
    rootE = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    doc = etree.Element('Document')
    rootE.append(doc)
    return rootE

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
