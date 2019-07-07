# This module is part of the core Basondole Tools
# This code provides a GUI to manage devices invetory in Basondole Tools
# AUTHOR: Paul S.I. Basondole

import Tkinter
from Tkinter import *
import ttk
from ClassDialog import Dialog


# variables for GUI icons
cancel_icon='C:\Users\u\Desktop\PACOM\icon\cancel-icon.png'

class Devices(Tkinter.Toplevel):


    def __init__(self,parent,ipDict,path=False):

        def close():
            if parent: parent.attributes('-disabled', False)
            self.destroy()


        Tkinter.Toplevel.__init__(self)
        Tkinter.Toplevel.title(self,'Devices')
        Tkinter.Toplevel.protocol(self,'WM_DELETE_WINDOW', lambda: close())
        Tkinter.Toplevel.geometry(self,"684x700+347+148")

        if parent: parent.attributes('-disabled', True)
        if path: self.path = path


        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()

        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])



        Tkinter.Toplevel.configure(self,background="#d9d9d9")
        Tkinter.Toplevel.configure(self,highlightbackground="#d9d9d9")
        Tkinter.Toplevel.configure(self,highlightcolor="black")
        Tkinter.Toplevel.resizable(self, width=False, height=False)

        self.font10 = "-family {Segoe UI} -size 12 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
        self.font11 = "-family {Segoe UI} -size 10 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
        self.font9 = "-family Calibri -size 15 -weight bold -slant roman "  \
             "-underline 0 -overstrike 0"


        TFrame1 = ttk.Frame(self)
        TFrame1.place(relx=0.292, rely=0.104, relheight=0.89, relwidth=0.694)
        TFrame1.configure(relief='groove')
        TFrame1.configure(borderwidth="2")
        TFrame1.configure(width=475)

        Scrolledtext1 = ScrolledText(TFrame1)
        Scrolledtext1.place(relx=0.01, rely=0.01, relheight=0.975
                , relwidth=0.980)
        Scrolledtext1.configure(background="white")
        Scrolledtext1.configure(font="Courier")
        Scrolledtext1.configure(foreground="black")
        Scrolledtext1.configure(highlightbackground="#d9d9d9")
        Scrolledtext1.configure(highlightcolor="black")
        Scrolledtext1.configure(insertbackground="black")
        Scrolledtext1.configure(insertborderwidth="3")
        Scrolledtext1.configure(selectbackground="#c4c4c4")
        Scrolledtext1.configure(selectforeground="black")
        Scrolledtext1.configure(width=10)
        Scrolledtext1.configure(wrap='none')
        Scrolledtext1.insert(END,createDb(ipDict,None))

        TLabel1 = ttk.Label(self)
        TLabel1.place(relx=0.015, rely=0.04, height=36, width=240, anchor = 'w')
        TLabel1.configure(foreground="#000000")
        TLabel1.configure(font=self.font9)
        TLabel1.configure(relief='flat')
        TLabel1.configure(text='''Device database''')
        TLabel1.configure(width=101)

        self.TFrame2 = ttk.Frame(self)
        self.TFrame2.place(relx=0.015, rely=0.104, relheight=0.186
                , relwidth=0.27)
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(borderwidth="2")
        self.TFrame2.configure(width=185)

        self.TButton1 = ttk.Button(self.TFrame2)
        self.TButton1.place(relx=0.179, rely=0.16, height=38, width=130)
        self.TButton1.configure(takefocus="")
        self._img1 = PhotoImage(file='')
        self.TButton1.configure(text='''Add new''',image=self._img1,compound='left')
        self.TButton1.image = self._img1
        self.TButton1.configure(command=lambda: self.editDevices('add',ipDict))

        tFr47_tBu50 = ttk.Button(self.TFrame2)
        tFr47_tBu50.place(relx=0.179, rely=0.56, height=38, width=130)
        tFr47_tBu50.configure(takefocus="")
        self._img50 = PhotoImage(file='')
        tFr47_tBu50.configure(text='''Remove  ''',image=self._img50, compound='left')
        tFr47_tBu50.image = self._img50
        tFr47_tBu50.configure(command=lambda: self.editDevices('remove',ipDict))


        TButton3 = ttk.Button(self)
        TButton3.place(relx=0.016, rely=0.928, height=43, width=183)
        TButton3.configure(takefocus="")
        TButton3.configure(text='''Close''', compound='left')
        TButton3.configure(command=lambda: close())


    def editDevices(self,action,ipDict):

        self.clear()

        self.TFrame3 = ttk.Frame(self)
        self.TFrame3.place(relx=0.015, rely=0.382, relheight=0.543
                , relwidth=0.27)
        self.TFrame3.configure(relief='groove')
        self.TFrame3.configure(borderwidth="2")
        self.TFrame3.configure(width=185)

        self.TLabel2_3 = ttk.Label(self)
        self.TLabel2_3.place(relx=0.017, rely=0.306, height=36, width=176)
        self.TLabel2_3.configure(foreground="#000000")
        self.TLabel2_3.configure(font=self.font9)
        self.TLabel2_3.configure(relief='flat')
        self.TLabel2_3.configure(text='''Input data''')

        self.TLabel3 = ttk.Label(self.TFrame3)
        self.TLabel3.place(relx=0.108, rely=0.038, height=29, width=105)
        self.TLabel3.configure(foreground="#000000")
        self.TLabel3.configure(font="TkDefaultFont")
        self.TLabel3.configure(relief='flat')
        self.TLabel3.configure(text='''IPv4 address''')

        self.ipaddr = ttk.Entry(self.TFrame3)
        self.ipaddr.place(relx=0.108, rely=0.115, relheight=0.075, relwidth=0.789)
        self.ipaddr.configure(width=146)
        self.ipaddr.configure(takefocus="")
        self.ipaddr.configure(cursor="ibeam")

        if action == 'remove':

            self.TButton3_4 = ttk.Button(self.TFrame3)
            self.TButton3_4.place(relx=0.108, rely=0.301, height=38, width=144)
            self.TButton3_4.configure(takefocus="")
            self.TButton3_4.configure(text='''Remove''')
            self.TButton3_4.configure(command=lambda: self.executeRemove(ipDict))

        if action == 'add':

            self.TLabel3_5 = ttk.Label(self.TFrame3)
            self.TLabel3_5.place(relx=0.108, rely=0.231, height=29, width=105)
            self.TLabel3_5.configure(foreground="#000000")
            self.TLabel3_5.configure(font="TkDefaultFont")
            self.TLabel3_5.configure(relief='flat')
            self.TLabel3_5.configure(text='''Hostname''')

            self.hostnameinput = StringVar(self.TFrame3)
            self.hostname = ttk.Entry(self.TFrame3)
            self.hostname.place(relx=0.108, rely=0.303, relheight=0.075
                    , relwidth=0.789)
            self.hostname.configure(takefocus="",textvar=self.hostnameinput)
            self.hostname.configure(cursor="ibeam")


            self.TLabel3_6 = ttk.Label(self.TFrame3)
            self.TLabel3_6.place(relx=0.135, rely=0.404, height=29, width=105)
            self.TLabel3_6.configure(foreground="#000000")
            self.TLabel3_6.configure(font="TkDefaultFont")
            self.TLabel3_6.configure(relief='flat')
            self.TLabel3_6.configure(text='''Vendor''')

            self.vendorselect = StringVar(self.TFrame3)
            self.vendorlist = ['Cisco','Juniper']
            self.vendor = ttk.Combobox(self.TFrame3)
            self.vendor.place(relx=0.108, rely=0.484, relheight=0.075
                    , relwidth=0.789)
            self.vendor.configure(textvar=self.vendorselect, values=self.vendorlist)
            self.vendor.configure(width=146)
            self.vendor.configure(foreground="#e0e0e0")
            self.vendor.configure(background="#e2e2e2")
            self.vendor.configure(takefocus="")


            self.TLabel3_7 = ttk.Label(self.TFrame3)
            self.TLabel3_7.place(relx=0.135, rely=0.585, height=29, width=125)
            self.TLabel3_7.configure(foreground="#000000")
            self.TLabel3_7.configure(font="TkDefaultFont")
            self.TLabel3_7.configure(relief='flat')
            self.TLabel3_7.configure(text='''Logical system''')


            self.Logical = ttk.Entry(self.TFrame3)
            self.Logical.place(relx=0.108, rely=0.669, relheight=0.075
                    , relwidth=0.789)
            self.Logical.configure(cursor="ibeam")
            self.Logical.configure(takefocus="")
            self.Logical.insert(0, "None")

            self.TButton3_4 = ttk.Button(self.TFrame3)
            self.TButton3_4.place(relx=0.108, rely=0.8, height=38, width=144)
            self.TButton3_4.configure(takefocus="")
            self.TButton3_4.configure(text='''Save''')
            self.TButton3_4.configure(command=lambda: self.executeAdd(ipDict))


    def executeAdd(self,ipDict):
        self.vendor = self.vendorselect.get()
        self.hostname = self.hostnameinput.get().replace(" ","_")
        ipaddr = self.ipaddr.get()
        ls = self.Logical.get()
        if not ipaddr:
            Dialog(self,title='Error',
                   prompt='No address entered\n',
                   icon=cancel_icon)
            return
        if not self.vendor or not self.hostname:
            Dialog(self,title='Error',
                   prompt='Enter hostname and vendor\n',
                   icon=cancel_icon)
            return

        ipaddr.split(".")
        if len(ipaddr.split('.'))>4:
            answer = Dialog(self,title='Error',prompt='Wrong IP address entered\n',
                            icon=cancel_icon)
            if answer.ans == 'ok': self.clear()
            return
        for octate in range(len(ipaddr.split('.'))):
           try:
               if int(ipaddr.split(".")[octate])>255:
                   answer = Dialog(self,title='Error',prompt='Wrong IP address entered\n',
                                   icon=cancel_icon)
                   if answer.ans == 'ok': self.clear()
                   return
           except ValueError:
               answer = Dialog(self,title='Error',prompt='Wrong IP address entered\n',
                               icon=cancel_icon)
               if answer.ans == 'ok': self.clear()
               return


        if ls and ls!='None':
            ipDict[ipaddr]=[self.vendor.lower(),self.hostname,ls]
        else: ipDict[ipaddr]=[self.vendor.lower(),self.hostname]

        keylist = ipDict.keys()
        keylist.sort()
        routers = open(self.path+"devices.bas","w")
        for key in keylist:
            try: routers.write('ipv4='+key.ljust(15)+ ' vendor='+ipDict[key][0].ljust(10)+\
                                   ' hostname='+ipDict[key][1].ljust(20)+' logicalsys='+ipDict[key][2])
            except IndexError: routers.write('ipv4='+key.ljust(15)+ ' vendor='+ipDict[key][0].ljust(10)+\
                                             ' hostname='+ipDict[key][1])
            routers.write('\n')
        routers.close()
        self.clear()

    def executeRemove(self,ipDict):
        try: ipDict.pop(self.ipaddr.get())
        except KeyError:
           answer = Dialog(self,title='Error',prompt='Device not found\n',
                           icon=cancel_icon)
           if answer.ans == 'ok':self.clear()
           return
        keylist = ipDict.keys()
        keylist.sort()
        routers = open(self.path+"devices.bas","w")
        for key in keylist:
          routers.write('ipv4='+key.ljust(15)+ ' vendor='+ipDict[key][0].ljust(10)+\
                    ' hostname='+ipDict[key][1]+'\n')
        routers.close()
        self.clear()

    def clear(self):
        try: self.TFrame3.destroy()
        except AttributeError: reason='widgets do not exist'


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

def delEmptyLine(file):
   list = []
   list = file.split('\n')
   list.sort()
   cleanFile = ''
   for item in list:
     if item == '' : continue
     else: cleanFile+=item.strip()+'\n'
   return cleanFile.strip()

def createDb(ipDict,option):
   ipList = ipDict.keys()
   ipList.sort()
   ipFile=''
   cisco = ''
   juniper = ''
   others = ''
   for line in ipList:
       if 'juniper' in ipDict[line][0]:
           juniper+=line.ljust(15)+' ['+ipDict[line][1]+']\n'
       elif 'cisco' in ipDict[line][0]:
           cisco+=line.ljust(15)+' ['+ipDict[line][1]+']\n'
       else: others+=line.ljust(15)+' ['+ipDict[line][0].ljust(10)+' '+ipDict[line][1]+']\n'
   ipFile+='Cisco\n'+cisco+'\nJuniper\n'+juniper+'\nOthers\n'+others

   if option == 'juniper': return delEmptyLine(juniper)
   elif option == 'cisco' : return delEmptyLine(cisco)
   else: return ipFile

def testDevices():
    from initial import getIpFromFile
    ipDict = getIpFromFile(path='c:\users\u\Desktop\pacom\\')
    d = Devices(None,ipDict,path='c:\users\u\Desktop\pacom\\')
    d.mainloop()

if __name__ == '__main__':
   testDevices()

