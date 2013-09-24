CustomerToKML
A database-to-KML file generator.

This generator connects to a database, queries for addresses, runs them through Googles geocoder, and saves them to a KML file.
This process is recorded in a seperate log file in the same directory.

Python 2.75
Libraries: pyodbc, urllib, sys, logging, Tkinter, ttk, string, tkFileDialog, lxml, time, datetime, xlrd