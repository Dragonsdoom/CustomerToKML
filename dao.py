"""Data Access Object provides data access."""
import sys
import logging
import pyodbc


class DAO(object):

    """Extend class to implement functionality."""

    def __init__(self):
        pass

    def prepare(self):
        """Prepare access statement."""
        pass

    def connect(self):
        """Connect to data location."""
        pass

    def query(self):
        """Query data source."""
        pass

    def get(self):
        """Get data from DAO."""
        pass

    def close(self):
        """Close connection to data source."""
        pass


class MSSQLDAO(DAO):

    """Implement mssql DAO."""
    
    connected = False
    connection = None
    cursor = None
    connstr = ''
    statement = ''
    results = {}

    def __init__(self, server, database, uid, pwd):
        DAO.__init__(self)
        self.connstr = ('driver={SQL Server};server=' + server + ';database=' +
                        database + ';uid=' + uid + ';pwd=' + pwd)
        self.statement = self.prepare()

    def prepare(self):
        """Prepare access statement."""
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
        """Connect to data location."""
        if self.connstr:
            # open database connection
            # https://code.google.com/p/pyodbc/wiki/GettingStarted
            logging.info('Opening connection to database..')
            try:
                self.connection = pyodbc.connect(self.connstr)
            except Exception as err:
                logging.warning(
                    "Error while connecting to database: " + str(err))
                sys.exit()
            self.cursor = self.connection.cursor()
            self.connected = True
            return True
        else:
            return False

    def query(self):
        """Query data source."""
        if self.cursor and self.query:
            self.results = {}
            logging.info('Executing query..')
            try:
                self.cursor.execute(self.statement)
            except Exception as err:
                logging.warning("Error while querying database: " + str(err))
                sys.exit()
            rows = self.cursor.fetchall()
            cols = []
            # get cols from cursor
            for x in range(0, len(self.cursor.description)):
                cols.append(self.cursor.description[x][0])
            # set up lists in result dict
            for col in cols:
                self.results[col] = []
            # add results to lists in dict by column
            for x in range(0, len(rows)):
                for y in range(0, len(cols)):
                    self.results[cols[y]].append(rows[x][y])
            return True
        else:
            return False

    def get(self):
        """Get data from DAO."""
        if self.results:
            return self.results
        else:
            raise ValueError

    def close(self):
        """Close connection to data source."""
        if self.connection:
            logging.info('Closing connection to database..')
            try:
                self.connection.close()
            except Exception as err:
                logging.warning("Error while writing to file: " + str(err))
                sys.exit()
            self.connected = False
            return True
        else:
            return False
