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

def createGUIMaster(title,geometry):
    """
    This func creates and initalizes the tkinter GUI master object,
    then returns it
    """
    master = Tk.Tk()
    master.title(title)
    master.geometry(geometry)
    master.lift()
    return master

def getCreds():
    """
    This func queries the user for database and geocoding credentials
    and returns a list of credentials
    """
    master = createGUIMaster('CustomerToKML','200x200')

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

    credentials = {}
    def callback():
        for x in uiPairs.keys():
            credentials[x] = uiPairs[x][1].get()
        master.destroy()

    button = Tk.Button(master, text="Ok", command=callback)
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

def connectToMSSQL(server,database,uid,pwd):
    """
    This func connects to MSSQL using the arguments provided and returns the
    connection object
    """
    try:
        connStr = ('driver={SQL Server};server=' + server + ';database=' +
        database + ';uid=' + uid + ';pwd=' + pwd)
        connection = pyodbc.connect(connStr)
    except Exception, e:
        logging.warning("Error while connecting to database: " + str(e))
        sys.exit()
    return connection

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

def buildQuery():
    # get active customers with addresses
    raise RuntimeError, "Database query removed to preserve proprietary business information. Please replace this with your own query."

def connectToSQLServer():
    # get credentials for database and geocoding
    logging.info('Requesting credentials..')
    creds = sanitizeCreds(getCreds())

    # open database connection
    # https://code.google.com/p/pyodbc/wiki/GettingStarted
    logging.info('Opening connection to database..')
    connection = connectToMSSQL(creds['Server Name'],
                                creds['Database Name'],
                                creds['Database User Name'],
                                creds['Database Password'])
    cursor = connection.cursor()
    return cursor

def executeSQLQuery(cursor, qStatement):
    logging.info('Executing query..')
    try:
        cursor.execute(qStatement)
    except Exception, e:
        logging.warning("Error while querying database: " + str(e))
        sys.exit()
    return cursor

def main():
    initLogging()
       
    cursor = connectToSQLServer()
    logging.info('Building query..')
    qStatement = buildQuery()
    cursor = executeSQLQuery(cursor, qStatement)

    # building root nodes
    # http://lxml.de/tutorial.html
    # https://developers.google.com/kml/documentation/kml_tut
    logging.info('Building kml in memory..')
    root = etree.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    doc = etree.Element('Document')
    root.append(doc)

    # read data from query and generate XML tree
    address = ''
    for row in cursor.fetchall():
        logging.info('Fetching row from cursor..')
        address = (str(row.AddressLine1) +
        ', ' + str(row.City) +
        ', ' + str(row.StateProvince) +
        ' ' + str(row.PostalCode) +
        ', ' + str(row.CountryRegion))
        
        custName = str(row.Name)
        logging.info('Geocoding address..')
        try:
            addressGCode = geocode(address)
        except Exception, e:
            logging.warning("Error while geocoding address: " + str(e))
            sys.exit()
        logging.info('Appending row to kml..')
        doc.append(placemark(custName, address, addressGCode))

        waitSecs = 10
        logging.info('Waiting to geocode next address (~' + str(waitSecs) +
                     's)..')
        sleep(waitSecs) # Don't overflow Google's geocoder

    # serialize XML
    logging.info('Serializing KML in memory..')
    try:
        serialOutput = etree.tostring(root,encoding="UTF-8",
                                      method="xml",
                                      xml_declaration=True,
                                      pretty_print=True)
    except Exception, e:
        logging.warning("Error while serializing addresses: " + str(e))
        sys.exit()

    # begin write to file
    logging.info('Requesting save location from user..')
    root = Tk.Tk()
    root.withdraw() # hides the root window

    try:
        filename = tkAskSaveAsFile(parent=root,
                                   defaultextension='.kml',
                                   filetypes=[('Google Earth KML','*.kml')],
                                   title="Save the file as...")
        logging.info('Writing to file..')
        filename.write(serialOutput)
    except IOError, e:
        logging.warning("Error while writing to file: " + str(e))
        root.destroy()
        sys.exit()

    logging.info('Closing file IO and destroying gui..')
    filename.close()
    root.destroy()

    # close connection to DB
    logging.info('Closing connection to database..')
    try:
        connection.close()
    except Exception, e:
        logging.warning("Error while writing to file: " + str(e))
        sys.exit()

    # end program
    logging.info('..Done')
    sys.exit()

# run program
if __name__ == "__main__":
    main()
