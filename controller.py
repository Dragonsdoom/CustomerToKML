import sys
import logging
from datetime import date
from customertokml import ctkModel as model
from tkview import tkview as view

class controller():
    def __init__(self,model):
        self.startLog()
        self.model = model
        self.view = view('Customer To KML',self,self.model)
        self.view.link(self.importDatabaseData,self.importExcelData)

    def display(self):
        self.view.mainloop()
        
    def startLog(self):
        """
        This func initializes the logging activity
        """
        # begin logging program activity to file
        d = date.today()
        logging.basicConfig(filename='CustomerToKml ' + d.strftime('%m %d %y') +
                            '.log', level=logging.DEBUG)
        logging.info('Beginning run log for program..')

    def importDatabaseData(self):
        self.view.hide()
        self.model.importFromDatabase(self.view.getServerName(),
                                 self.view.getDBName(),
                                 self.view.getUserName(),
                                 self.view.getDBPassword())
        
    def importExcelData(self):
        self.view.hide()
        self.model.importFromExcel()           

    def end(self):
        logging.info('..Done')
        logging.shutdown()
        sys.exit()

# starting function
def main():
    ctr = controller(model())
    ctr.display()
    ctr.end()

# entry point
if __name__ == "__main__":
    main()
