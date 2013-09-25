"""Perform all tasks related to GUI."""
import sys
import logging
from tkFileDialog import asksaveasfile, askopenfilename
import tkgen.gengui


class TkGenView(object):

    """Perform all tasks related to GUI."""

    def __init__(self, title, controller, model):
        self.root = tkgen.gengui.TkJson('tkgui.json', title='tkjson')
        self.controller = controller
        self.model = model
        model.addsub(self)

        self.root.resizable(0, 0)
        self.root.title = title
        self.root.lift()

    def link(self, import_dbcommand, import_xlscommand):
        """Link commands to buttons from controller."""
        self.root.button('dbimport_button',import_dbcommand)
        self.root.button('xlsimport_button',import_xlscommand)

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
        return self.root.entry('sname_entry').get()

    def get_dbname(self):
        """Get attribute."""
        return self.root.entry('dbname_entry').get()

    def get_username(self):
        """Get attribute."""
        return self.root.entry('username_entry').get()

    def get_dbpassword(self):
        """Get attribute."""
        return self.root.entry('dbpw_entry').get()

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