"""Handle logic calls between the view and the model."""
import sys
import logging
from datetime import date
from tkgenview import TkGenView as view


class Controller(object):

    """Handle logic calls between the view and the model."""

    def __init__(self, newmodel):
        self.start_log()
        self.model = newmodel
        self.view = view('Customer To KML', self, self.model)
        self.view.link(self.import_database_data, self.import_excel_data)

    def display(self):
        """Display the GUI."""
        self.view.mainloop()

    @staticmethod
    def start_log():
        """
        Initialize the logging activity.
        """
        # begin logging program activity to file
        today = date.today()
        logging.basicConfig(filename='CustomerToKml '
                            + today.strftime('%m %d %y') +
                            '.log', level=logging.DEBUG)
        logging.info('Beginning run log for program..')

    def import_database_data(self):
        """Import data from database connection in model."""
        self.view.hide()
        data = self.model.dbimport(self.view.get_servername(),
                                   self.view.get_dbname(),
                                   self.view.get_username(),
                                   self.view.get_dbpassword())
        caddresses = self.model.build_cust_addresses_dict(data)
        self.model.geocode_cust_addresses(caddresses)
        self.end()

    def import_excel_data(self):
        """Import data from Excel."""
        self.view.hide()
        xls = self.view.get_xlsfile()
        data = self.model.xlsparse(xls)
        caddresses = self.model.build_cust_addresses_dict(data)
        self.model.geocode_cust_addresses(caddresses)
        self.end()

    @staticmethod
    def end():
        """End the program."""
        logging.info('..Done')
        logging.shutdown()
        sys.exit()

