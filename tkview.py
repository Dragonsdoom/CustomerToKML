import sys
import logging
import Tkinter as tk
import ttk

class tkview():
    root = tk.Tk()

    def __init__(self,title,controller,model):
        self.controller = controller
        self.model = model
        #model.addSubscriber(self)

        self.root.resizable(0,0)
        self.root.title(title)
        self.root.lift()

        serverNameLabel = ttk.Label(self.root,text="Enter server name: ")
        serverNameLabel.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5)
        serverNameEntry = ttk.Entry(self.root)
        serverNameEntry.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=3)
        serverNameEntry.focus()
        
        dbNameLabel = ttk.Label(self.root,text="Enter database name: ")
        dbNameLabel.grid(row=3, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5)
        dbNameEntry = ttk.Entry(self.root)
        dbNameEntry.grid(row=4, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=3)

        userNameLabel = ttk.Label(self.root,text="Enter database user name: ")
        userNameLabel.grid(row=5, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5)
        userNameEntry = ttk.Entry(self.root)
        userNameEntry.grid(row=6, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=3)

        dbpwLabel = ttk.Label(self.root,text="Enter database password: ")
        dbpwLabel.grid(row=7, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5)
        dbpwEntry = ttk.Entry(self.root,show='*')
        dbpwEntry.grid(row=8, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=3)

        importButtonDB = ttk.Button(self.root,text="Import From Database", command=None)
        importButtonDB.grid(row=9, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=3)
        importButtonXLS = ttk.Button(self.root,text="Import From Excel", command=None)
        importButtonXLS.grid(row=10, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=3)

    def write(self,data,extension,extDescription):
        logging.info('Requesting save location from user..')
        self.root.withdraw() # hides the root window

        try:
            filename = tkAskSaveAsFile(parent=self.root,
                                       defaultextension=extension,
                                       filetypes=[(extDescription,extension)],
                                       title="Save the file as...")
            logging.info('Writing to file..')
            filename.write(data)
        except IOError, e:
            logging.warning("Error while writing to file: " + str(e))
            self.root.destroy()
            sys.exit()
        finally:
            logging.info('Closing file IO and destroying gui..')
            filename.close()
            
    def mainloop(self):
        tk.mainloop()
