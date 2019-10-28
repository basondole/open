# This module is part of the core Basondole Tools
# This code  provides a window to display output of various functions
# The output of a function is passed to this code to be displayed in a window
# AUTHOR: Paul S.I. Basondole

import Tkinter
from Tkinter import *
import ttk

# variable for GUI icons
program_icon ='C:\Users\u\Desktop\PACOM\icon\paul-icon1.ico'


class outputWin():


    def TB2(self,title,output,window,frame):


        def close():
            window.attributes('-disabled', False)
            win2.destroy()

        win2 = Tkinter.Tk()
        win2.title(title)
        win2.protocol('WM_DELETE_WINDOW', lambda: close())

        window.attributes('-disabled', True)

        textFrame = Tkinter.Frame(win2, width=600,height=560)
        textFrame.pack(fill='both',expand=True)
        textFrame.grid_propagate(False)
        textFrame.grid_rowconfigure(0, weight=1)
        textFrame.grid_columnconfigure(0, weight=2)


        closebutton = ttk.Button(win2)
        closebutton.configure(text='Close')
        closebutton.configure(command=lambda: close())
        closebutton.pack()

        Scrolledtext1 = ScrolledText(textFrame)
        Scrolledtext1.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        Scrolledtext1.configure(background="white")
        Scrolledtext1.configure(font="Courier")
        Scrolledtext1.configure(foreground="black")
        Scrolledtext1.configure(highlightbackground="#d9d9d9")
        Scrolledtext1.configure(highlightcolor="black")
        Scrolledtext1.configure(insertbackground="black")
        Scrolledtext1.configure(insertborderwidth="3")
        Scrolledtext1.configure(selectbackground="#c4c4c4")
        Scrolledtext1.configure(selectforeground="black")
        Scrolledtext1.configure(width=643)
        Scrolledtext1.configure(wrap='none')
        Scrolledtext1.insert(END,output)



    def Error(self):

        win2 = Tkinter.Tk()
        win2.title('Error')
        win2.iconbitmap(self,default=program_icon)
        win2.title('Big Paul Tools')
        win2.geometry("460x241+636+175")
        label=Tkinter.Label(win2, text="Error\nDevice database not found")
        label.pack()
        win2.mainloop()


#Scroll bar functionality
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        py3 = False
        if py3:
            methods = Tkinter.Pack.__dict__.keys() | Tkinter.Grid.__dict__.keys() \
                  | Tkinter.Place.__dict__.keys()
        else:
            methods = Tkinter.Pack.__dict__.keys() + Tkinter.Grid.__dict__.keys() \
                  + Tkinter.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, Tkinter.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Tkinter.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledEntry(AutoScroll, Tkinter.Entry):
    '''A standard Tkinter Entry widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Tkinter.Entry.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
#EOF Scrollbar Functionality
