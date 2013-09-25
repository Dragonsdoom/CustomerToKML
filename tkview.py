"""Perform all tasks related to GUI."""
import sys
import logging
import Tkinter as tk
import ttk
from tkFileDialog import asksaveasfile, askopenfilename


class Tkview(object):

    """Perform all tasks related to GUI."""

    root = tk.Tk()

    def __init__(self, title, controller, model):
        self.controller = controller
        self.model = model
        model.addsub(self)

        self.root.resizable(0, 0)
        self.root.title(title)
        self.root.lift()

        self.servername_label = ttk.Label(self.root, text="Enter server name: ")
        self.servername_label.grid(row=0, column=0,
                                   sticky=tk.W + tk.E + tk.N + tk.S, padx=5)
        self.servername_entry = ttk.Entry(self.root)
        self.servername_entry.grid(row=1, column=0,
                                   sticky=tk.W + tk.E + tk.N + tk.S,
                                   padx=5, pady=3)
        self.servername_entry.focus()

        self.dbname_label = ttk.Label(self.root, text="Enter database name: ")
        self.dbname_label.grid(row=3, column=0,
                               sticky=tk.W + tk.E + tk.N + tk.S, padx=5)
        self.dbname_entry = ttk.Entry(self.root)
        self.dbname_entry.grid(row=4, column=0,
                               sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=3)

        self.username_label = ttk.Label(
            self.root, text="Enter database user name: ")
        self.username_label.grid(row=5, column=0,
                                 sticky=tk.W + tk.E + tk.N + tk.S, padx=5)
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(row=6, column=0,
                                 sticky=tk.W + tk.E + tk.N + tk.S,
                                 padx=5, pady=3)

        self.dbpw_label = ttk.Label(self.root, text="Enter database password: ")
        self.dbpw_label.grid(row=7, column=0,
                             sticky=tk.W + tk.E + tk.N + tk.S, padx=5)
        self.dbpw_entry = ttk.Entry(self.root, show='*')
        self.dbpw_entry.grid(row=8, column=0,
                             sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=3)

        self.dbimport_button = ttk.Button(self.root,
                                          text="Import From Database",
                                          command=None)
        self.dbimport_button.grid(row=9, column=0,
                                  sticky=tk.W + tk.E + tk.N + tk.S,
                                  padx=5, pady=3)
        self.xlsimport_button = ttk.Button(self.root,
                                           text="Import From Excel",
                                           command=None)
        self.xlsimport_button.grid(row=10, column=0,
                                   sticky=tk.W + tk.E + tk.N + tk.S,
                                   padx=5, pady=3)

    def link(self, import_dbcommand, import_xlscommand):
        """Link commands to buttons from controller."""
        self.dbimport_button.config(command=import_dbcommand)
        self.xlsimport_button.config(command=import_xlscommand)

    def hide(self):
        """Hide GUI window."""
        self.root.withdraw()

    def write(self, data, extension, exten_desc):
        """Write output to file."""
        logging.info('Requesting save location from user..')
        self.root.withdraw()  # hides the root window
        filename = None
        try:
            filename = asksaveasfile(parent=self.root,
                                     defaultextension=extension,
                                     filetypes=[(exten_desc, extension)],
                                     title="Save the file as...")
            logging.info('Writing to file..')
            filename.write(data)
        except IOError as err:
            logging.warning("Error while writing to file: " + str(err))
            self.root.destroy()
            sys.exit()
        finally:
            logging.info('Closing file IO and destroying gui..')
            filename.close()

    def get_servername(self):
        """Get attribute."""
        return self.servername_entry.get()

    def get_dbname(self):
        """Get attribute."""
        return self.dbname_entry.get()

    def get_username(self):
        """Get attribute."""
        return self.username_entry.get()

    def get_dbpassword(self):
        """Get attribute."""
        return self.dbpw_entry.get()

    def get_xlsfile(self):
        """Get file from operator."""
        xls = askopenfilename(parent=self.root,
                              defaultextension='*.xls',
                              filetypes=[('Excel XLS file', '*.xls')],
                              title="Open XLS file...")
        if xls:
            return xls
        else:
            raise TypeError

    def mainloop(self):
        """Draw the GUI while listening for events."""
        self.root.mainloop()
