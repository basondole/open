# This module is part of the core Basondole Tools
# This code creates dialog pop up windows
# This is forked from Tkinter dialog module
# AUTHOR: Paul S.I. Basondole

from Tkinter import *
import ttk
from PIL import Image, ImageTk

# variables for GUI icons
warning_icon = "C:\Users\u\Desktop\PACOM\icon\warning-icon.png"


class Dialog(Toplevel):

    '''Class to open dialogs.

    This class is intended as a base class for custom dialogs
    '''

    def __init__(self, parent, title=None, prompt=None, icon=None,
                 lbutton=None,rbutton=None, nobutton=None, resizable=True):

        '''Initialize a dialog.

        Arguments:

            parent -- a parent window (the application window)

            title -- the dialog title
        '''
        Toplevel.__init__(self, parent)

        if not resizable: self.resizable(width=False,height=False)

        self.withdraw() # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)
        if prompt:
            self.prompt = '\n'+prompt
        if lbutton:
            self.lb = lbutton
        else: self.lb = 'OK'
        if rbutton:
            self.rb = rbutton
        else: self.rb = 'Cancel'

        if nobutton:
           self.button = False
        else: self.button = True

        if icon: self.icon = icon
        else: self.icon = False

        self.ans = ''

        self.parent = parent

        self.result = None


        self.body1 = Frame(self)
        self.initial_focus = self.body(self.body1)
        self.body1.pack(padx=5, pady=5)

        self.buttonbox()


        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
           self.geometry("+%d+%d" % (self.location(self.parent)))

        self.deiconify() # become visibile now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self):
        '''Destroy the window'''
        self.initial_focus = None
        Toplevel.destroy(self)

    # construction hooks

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        pass

    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''

        box = Frame(self)
        butttonframe = Frame(self)

        if self.icon:
           self.load = Image.open(self.icon)
           self.render = ImageTk.PhotoImage(self.load)
           self.img = Label(box, image=self.render)
           self.img.image = self.render
           self.img.pack(side=LEFT, padx=10)

        l = Label(box, text=self.prompt)
        l.pack(side=LEFT,padx=10)

        if self.button:
           w = ttk.Button(butttonframe, text=self.lb, width=10, command=lambda: self.ok(), default=ACTIVE)
           w.pack(side=LEFT, padx=5, pady=5)
           w = ttk.Button(butttonframe, text=self.rb, width=10, command=lambda: self.cancel())
           w.pack(side=LEFT, padx=5, pady=5)

           self.bind("<Return>", self.ok)
           self.bind("<Escape>", self.cancel)



        butttonframe.pack(side=BOTTOM)
        box.pack()

    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    # command hooks

    def validate(self):
        '''validate the data

        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        '''

        return 1 # override

    def apply(self):
        '''process the data

        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        '''
        self.ans = 'ok'
        return


    def location(self,master,relx=0.24, rely=0.3):
        widget = self.body1
        if master.winfo_ismapped():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = master.winfo_screenwidth()
            m_height = master.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > master.winfo_screenwidth():
            x = master.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > master.winfo_screenheight():
            y = master.winfo_screenheight() - w_height
        elif y < 0:
            y = 0

        return x,y


def test():
   root = Tk()
   app = Dialog(root,prompt='\npaul\nis the developer of this\ncode which\nis so nice\n',icon=warning_icon,nobutton=True)


if __name__=='__main__':
   test()
