"""Handle logic calls between the view and the model."""
import sys
import logging
from datetime import date
from .customertokml import ctkModel
from .tkview import tkview as view


class Controller(object):

    """Handle logic calls between the view and the model."""

    def __init__(self, model):
        self.start_log()
        self.model = model
        self.view = view('Customer To KML', self, self.model)
        self.view.link(self.import_database_data, self.import_excel_data)

    def display(self):
        """Display the GUI."""
        self.view.mainloop()

    def start_log(self):
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
        self.model.importFromDatabase(self.view.getServerName(),
                                      self.view.getDBName(),
                                      self.view.getUserName(),
                                      self.view.getDBPassword())

    def import_excel_data(self):
        """Import data from Excel."""
        self.view.hide()
        self.model.importFromExcel()

    def end(self):
        """End the program."""
        logging.info('..Done')
        logging.shutdown()
        sys.exit()


def main():
    """Enter the program"""
    ctr = Controller(ctkModel())
    ctr.display()
    ctr.end()

if __name__ == "__main__":
    main()
