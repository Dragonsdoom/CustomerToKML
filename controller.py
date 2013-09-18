import sys
import logging
from datetime import date
import customertokml as ctk
from tkview import tkview

class controller():
    def __init__(self,model):
        self.startLog()
        self.view = tkview('Customer To KML',self,None)

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

    def end(self):
        logging.info('..Done')
        logging.shutdown()
        sys.exit()
        
def main():
    ctr = controller(None)
    ctr.display()
    ctr.end()

# run program
if __name__ == "__main__":
    main()
