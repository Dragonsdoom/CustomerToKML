import sys
import logging
import pyodbc

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
