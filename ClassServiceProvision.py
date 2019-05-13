# This module is part of the core Basondole Tools
# This code provides GUI for user to provison IP service and Martini layer 2 circuits
# Can work with most shell with ssh support but it is further optimized for JunOS, Cisco IOS and IOS XE and Debian
# AUTHOR: Paul S.I. Basondole

import Tkinter
import ttk
from Tkinter import *

import ipaddr
from IPy import IP as validIP

from ClassLoading import loading
from vFinderUnNC import vlanFinder
from vFinderDeuxNC import vlanFinderDualPes
from ClassDialog import Dialog
from ClassSendCommand import ClassSendCommand


# Variables for GUI icons
error_icon = "C:\Users\u\Desktop\PACOM\icon\error-icon.png"
warning_icon = "C:\Users\u\Desktop\PACOM\icon\warning-icon.png"


class ServiceProvision(Tkinter.Toplevel):

    def __init__(self,username,password,ipDict,intDict,policerDict):

        Tkinter.Toplevel.__init__(self)

        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family Calibri -size 15 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        self.style = ttk.Style()
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        self.user = username
        self.key = password

        Tkinter.Toplevel.geometry(self,"600x660+322+128")
        Tkinter.Toplevel.title(self,"Service Provision")
        Tkinter.Toplevel.configure(self,background="#d9d9d9")
        Tkinter.Toplevel.configure(self,highlightbackground="#d9d9d9")
        Tkinter.Toplevel.configure(self,highlightcolor="black")

        self.Label3 = Tkinter.Label(self)
        self.Label3.place(relx=0.017, rely=0.015, height=55, width=295)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font11)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Service Provision''')

        self.Frame3 = Tkinter.Frame(self)
        self.Frame3.place(relx=0.017, rely=0.106, relheight=0.809
                , relwidth=0.975)
        self.Frame3.configure(relief='groove')
        self.Frame3.configure(background="#d9d9d9")
        self.Frame3.configure(highlightbackground="#d9d9d9")
        self.Frame3.configure(highlightcolor="black")
        self.Frame3.configure(width=585)

        self.TFrame1 = Tkinter.Frame(self.Frame3)
        self.TFrame1.place(relx=0.034, rely=0.009, relheight=0.626
                , relwidth=0.419)
        self.TFrame1.configure(relief='groove')
        self.TFrame1.configure(borderwidth="2")
        self.TFrame1.configure(width=245)


        self.TFrame1_6 = Tkinter.Frame(self.Frame3)
        self.TFrame1_6.place(relx=0.479, rely=0.009, relheight=0.626
                , relwidth=0.419)
        self.TFrame1_6.configure(relief='groove')
        self.TFrame1_6.configure(borderwidth="2")
        self.TFrame1_6.configure(width=245)

        self.TLabel1_8 = ttk.Label(self.TFrame1)
        self.TLabel1_8.place(relx=0.041, rely=0.025, height=32, width=97)
        self.TLabel1_8.configure(background="#d9d9d9")
        self.TLabel1_8.configure(foreground="#000000")
        self.TLabel1_8.configure(font="TkDefaultFont")
        self.TLabel1_8.configure(relief='flat')
        self.TLabel1_8.configure(text='''Service''')

        self.TFrame2 = ttk.Frame(self.Frame3)
        self.TFrame2.place(relx=0.034, rely=0.729, relheight=0.103
                , relwidth=0.863)
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(borderwidth="2")
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(width=505)

        def rebuild(choice):
            self.TFrame1.destroy()
            self.TFrame1_6.destroy()
            self.TFrame2.place_forget()
            self.Frame3.place_forget()
            self.TFrame1 = Tkinter.Frame(self.Frame3,relief='groove',borderwidth ='2')
            self.TFrame1_6 = Tkinter.Frame(self.Frame3,relief='groove',borderwidth ='2')
            self.TLabel1_8 = ttk.Label(self.TFrame1)
            self.TLabel1_8.place(relx=0.041, rely=0.025, height=32, width=97)
            self.TLabel1_8.configure(background="#d9d9d9")
            self.TLabel1_8.configure(foreground="#000000")
            self.TLabel1_8.configure(font="TkDefaultFont")
            self.TLabel1_8.configure(relief='flat')
            self.TLabel1_8.configure(text='''Service''')
            self.servselect = StringVar(self.TFrame1_6)
            self.TCombobox1_8 = ttk.Combobox(self.TFrame1_6)
            self.TCombobox1_8.configure(takefocus="")
            self.TCombobox1_8.configure(textvar=self.servselect, values=['Internet','L2mpls'])
            self.TCombobox1_8.bind("<<ComboboxSelected>>", service)
            self.TCombobox1_8.set(choice)

        def service(*args):
            choice = self.TCombobox1_8.get()
            rebuild(choice)
            self.TEntry1.delete(0,END)
            if choice == 'Internet':
                Tkinter.Toplevel.geometry(self,"600x660")
                internet(ipDict,intDict,policerDict,self,self.Frame3,self.TFrame1,self.TFrame1_6,self.TFrame2)
            elif choice == 'L2mpls':
                Tkinter.Toplevel.geometry(self,"600x760")
                l2mpls(ipDict,intDict,policerDict,self,self.Frame3,self.TFrame1,self.TFrame1_6,self.TFrame2)

        self.servselect = StringVar(self.TFrame1_6)
        self.TCombobox1_8 = ttk.Combobox(self.TFrame1_6)
        self.TCombobox1_8.place(relx=0.041, rely=0.03, relheight=0.093
                , relwidth=0.906)
        self.TCombobox1_8.configure(takefocus="")
        self.TCombobox1_8.configure(textvar=self.servselect, values=['Internet','L2mpls'])
        self.TCombobox1_8.bind("<<ComboboxSelected>>", service)
        self.TCombobox1_8.set('Internet')
        # default selected value is internet, thus we need to call the internet method here
        internet(ipDict,intDict,policerDict,self,self.Frame3,self.TFrame1,self.TFrame1_6,self.TFrame2)


        self.TLabel1_4 = ttk.Label(self.TFrame2)
        self.TLabel1_4.place(relx=0.02, rely=0.182, height=29, width=107)
        self.TLabel1_4.configure(background="#d9d9d9")
        self.TLabel1_4.configure(foreground="#000000")
        self.TLabel1_4.configure(font="TkDefaultFont")
        self.TLabel1_4.configure(relief='flat')
        self.TLabel1_4.configure(text='''Description''')

        self.TEntry1 = ttk.Entry(self.TFrame2)
        self.TEntry1.place(relx=0.218, rely=0.182, relheight=0.564
                , relwidth=0.764)
        self.TEntry1.configure(width=386)
        self.TEntry1.configure(takefocus="")
        self.TEntry1.configure(cursor="ibeam")

        self.Button2 = Tkinter.Button(self.Frame3)
        self.Button2.place(relx=0.034, rely=0.860, height=42, width=188)
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Configure''')
        self.Button2.configure(command= lambda: conf(self,ipDict,intDict,policerDict,self.TCombobox1_8.get()))

        self.Button2_14 = Tkinter.Button(self.Frame3)
        self.Button2_14.place(relx=0.564, rely=0.860, height=42, width=188)
        self.Button2_14.configure(pady="0")
        self.Button2_14.configure(text='''Clear''')
        self.Button2_14.configure(command= lambda: service())




class internet():

    def __init__(self,ipDict,intDict,policerDict,parent,mainframe,labelframe,entryframe,descframe):


        mainframe.place(relx=0.017, rely=0.106, relheight=0.809
                , relwidth=0.975)

        entryframe.place(relx=0.479, rely=0.009, relheight=0.626
                , relwidth=0.419)

        labelframe.place(relx=0.034, rely=0.009, relheight=0.626
                , relwidth=0.419)

        #description frame
        descframe.place(relx=0.034, rely=0.700, relheight=0.103
                , relwidth=0.863)

        #service type label
        parent.TLabel1_8.place(relx=0.041, rely=0.025, height=32, width=97)

        # for GUI elements position adjustment in window
        self.y, self.d = 0.142, 0.116

        parent.TLabel1_7 = ttk.Label(labelframe)
        parent.TLabel1_7.place(relx=0.041, rely=self.y, height=32, width=207)
        parent.TLabel1_7.configure(background="#d9d9d9")
        parent.TLabel1_7.configure(foreground="#000000")
        parent.TLabel1_7.configure(font="TkDefaultFont")
        parent.TLabel1_7.configure(relief='flat')
        parent.TLabel1_7.configure(text='''Edge router''')

        parent.TLabel1_3 = ttk.Label(labelframe)
        parent.TLabel1_3.place(relx=0.041, rely=self.y+self.d, height=32, width=207)
        parent.TLabel1_3.configure(background="#d9d9d9")
        parent.TLabel1_3.configure(foreground="#000000")
        parent.TLabel1_3.configure(font="TkDefaultFont")
        parent.TLabel1_3.configure(relief='flat')
        parent.TLabel1_3.configure(text='''Logical system (optional)''')

        parent.TLabel1_4 = ttk.Label(labelframe)
        parent.TLabel1_4.place(relx=0.041, rely=self.y+2*self.d, height=32, width=207)
        parent.TLabel1_4.configure(background="#d9d9d9")
        parent.TLabel1_4.configure(foreground="#000000")
        parent.TLabel1_4.configure(font="TkDefaultFont")
        parent.TLabel1_4.configure(relief='flat')
        parent.TLabel1_4.configure(text='''Interface''')

        parent.TLabel1_4 = ttk.Label(labelframe)
        parent.TLabel1_4.place(relx=0.041, rely=self.y+3*self.d, height=32, width=207)
        parent.TLabel1_4.configure(background="#d9d9d9")
        parent.TLabel1_4.configure(foreground="#000000")
        parent.TLabel1_4.configure(font="TkDefaultFont")
        parent.TLabel1_4.configure(relief='flat')
        parent.TLabel1_4.configure(text='''VLAN''')

        parent.TLabel1_4 = ttk.Label(labelframe)
        parent.TLabel1_4.place(relx=0.041, rely=self.y+4*self.d, height=32, width=207)
        parent.TLabel1_4.configure(background="#d9d9d9")
        parent.TLabel1_4.configure(foreground="#000000")
        parent.TLabel1_4.configure(font="TkDefaultFont")
        parent.TLabel1_4.configure(relief='flat')
        parent.TLabel1_4.configure(text='''IPv4 address''')

        parent.TLabel1_5 = ttk.Label(labelframe)
        parent.TLabel1_5.place(relx=0.041, rely=self.y+5*self.d, height=32, width=207)
        parent.TLabel1_5.configure(background="#d9d9d9")
        parent.TLabel1_5.configure(foreground="#000000")
        parent.TLabel1_5.configure(font="TkDefaultFont")
        parent.TLabel1_5.configure(relief='flat')
        parent.TLabel1_5.configure(text='''IPv6 address (optional)''')

        parent.TLabel1_6 = ttk.Label(labelframe)
        parent.TLabel1_6.place(relx=0.041, rely=self.y+6*self.d, height=32, width=207)
        parent.TLabel1_6.configure(background="#d9d9d9")
        parent.TLabel1_6.configure(foreground="#000000")
        parent.TLabel1_6.configure(font="TkDefaultFont")
        parent.TLabel1_6.configure(relief='flat')
        parent.TLabel1_6.configure(text='''Bandwidth''')


        # Servie type entry
        parent.TCombobox1_8.place(relx=0.041, rely=0.03, relheight=0.093
                    , relwidth=0.906)

        keylist = ipDict.keys()
        keylist.sort()
        ipList = []
        for ip in keylist: ipList.append(ip)

        def updateint(*args):
            self.freevlans = []
            parent.TCombobox1_11.configure(textvar=parent.vlanselect, values=self.freevlans)
            parent.TCombobox1_10.configure(textvar=parent.intselect, values=intDict[parent.devselect.get()])
            parent.TCombobox1_10.set('Select interface')
            if not 'Unlimited' in policerDict[parent.devselect.get()]:
                policerDict[parent.devselect.get()].insert(0,'Unlimited')
            parent.TCombobox1_14.configure(textvar=parent.polselect, values=policerDict[parent.devselect.get()])
            parent.TCombobox1_14.set('Unlimited')
            try: parent.TCombobox1_9.set(ipDict[parent.devselect.get()][2])
            except IndexError: parent.TCombobox1_9.set('None')

        parent.devselect = StringVar(entryframe)
        parent.TCombobox1 = ttk.Combobox(entryframe)
        parent.TCombobox1.place(relx=0.041, rely=0.149, relheight=0.093
                , relwidth=0.906)
        parent.TCombobox1.configure(width=222)
        parent.TCombobox1.configure(takefocus="")
        parent.TCombobox1.configure(textvar=parent.devselect, values=ipList)
        parent.TCombobox1.bind("<<ComboboxSelected>>", updateint)
        parent.TCombobox1.set('Select router')


        parent.TCombobox1_9 = ttk.Combobox(entryframe)
        parent.TCombobox1_9.place(relx=0.041, rely=0.269, relheight=0.093
                , relwidth=0.906)
        parent.TCombobox1_9.configure(takefocus="")
        parent.TCombobox1_9.set('None')


        def updatevlan(*args):
            if parent.TCombobox1_10.get() == 'Null':
                self.freevlans = []
                parent.TCombobox1_11.configure(textvar=parent.vlanselect, values=self.freevlans)
                return
            parent.loading = loading(entryframe,parent,pbar=[0.041,0.507,0.093,0.906],words='Loading vlans')
            parent.update_idletasks()
            self.freevlans = vlanFinder(parent.TCombobox1.get(),ipDict,parent.TCombobox1_10.get(),parent.user,parent.key)
            self.freevlans.insert(0,0)
            parent.TCombobox1_11.configure(textvar=parent.vlanselect, values=self.freevlans)
            parent.TCombobox1_11.set('Select')
            parent.config(cursor='')
            parent.update()
            parent.loading.stop(parent)

        parent.intselect = StringVar(entryframe)
        parent.TCombobox1_10 = ttk.Combobox(entryframe)
        parent.TCombobox1_10.place(relx=0.041, rely=0.388, relheight=0.093
                , relwidth=0.906)
        parent.TCombobox1_10.configure(takefocus="")
        parent.TCombobox1_10.set('Select interface')
        parent.TCombobox1_10.bind("<<ComboboxSelected>>", updatevlan)


        parent.vlanselect = StringVar(entryframe)
        parent.TCombobox1_11 = ttk.Combobox(entryframe)
        parent.TCombobox1_11.place(relx=0.041, rely=0.507, relheight=0.093
                , relwidth=0.906)
        parent.TCombobox1_11.configure(takefocus="")

        parent.TCombobox1_12 = ttk.Combobox(entryframe)
        parent.TCombobox1_12.place(relx=0.041, rely=0.627, relheight=0.093
                , relwidth=0.906)
        parent.TCombobox1_12.configure(takefocus="")

        parent.TCombobox1_13 = ttk.Combobox(entryframe)
        parent.TCombobox1_13.place(relx=0.041, rely=0.746, relheight=0.093
                , relwidth=0.906)
        parent.TCombobox1_13.configure(takefocus="")


        parent.polselect = StringVar(entryframe)
        parent.TCombobox1_14 = ttk.Combobox(entryframe)
        parent.TCombobox1_14.place(relx=0.041, rely=0.866, relheight=0.093
                , relwidth=0.906)
        parent.TCombobox1_14.configure(takefocus="")



class l2mpls():

    def __init__(self,ipDict,intDict,policerDict,parent,mainframe,labelframe,entryframe,descframe):


        mainframe.place(relx=0.017, rely=0.106, relheight=0.909
                , relwidth=0.975)

        entryframe.place(relx=0.479, rely=0.009, relheight=0.701
                , relwidth=0.419)

        labelframe.place(relx=0.034, rely=0.009, relheight=0.701
                , relwidth=0.419)


        #description frame
        descframe.place(relx=0.034, rely=0.729, relheight=0.103
                , relwidth=0.863)

        #service type label
        parent.TLabel1_8.place(relx=0.041, rely=0.025, height=32, width=97)

        self.y,self.d = 0.100,0.074

        parent.TLabel2_7 = ttk.Label(labelframe)
        parent.TLabel2_7.place(relx=0.041, rely=self.y, height=32, width=207)
        parent.TLabel2_7.configure(background="#d9d9d9")
        parent.TLabel2_7.configure(foreground="#000000")
        parent.TLabel2_7.configure(font="TkDefaultFont")
        parent.TLabel2_7.configure(relief='flat')
        parent.TLabel2_7.configure(text='''Edge router''')

        parent.TLabel2_3 = ttk.Label(labelframe)
        parent.TLabel2_3.place(relx=0.041, rely=self.y+self.d, height=32, width=207)
        parent.TLabel2_3.configure(background="#d9d9d9")
        parent.TLabel2_3.configure(foreground="#000000")
        parent.TLabel2_3.configure(font="TkDefaultFont")
        parent.TLabel2_3.configure(relief='flat')
        parent.TLabel2_3.configure(text='''Logical system (optional)''')

        parent.TLabel2_4 = ttk.Label(labelframe)
        parent.TLabel2_4.place(relx=0.041, rely=self.y+2*self.d, height=32, width=207)
        parent.TLabel2_4.configure(background="#d9d9d9")
        parent.TLabel2_4.configure(foreground="#000000")
        parent.TLabel2_4.configure(font="TkDefaultFont")
        parent.TLabel2_4.configure(relief='flat')
        parent.TLabel2_4.configure(text='''Interface''')


        parent.TLabel2_11 = ttk.Label(labelframe)
        parent.TLabel2_11.place(relx=0.041, rely=self.y+3*self.d, height=32, width=207)
        parent.TLabel2_11.configure(background="#d9d9d9")
        parent.TLabel2_11.configure(foreground="#000000")
        parent.TLabel2_11.configure(font="TkDefaultFont")
        parent.TLabel2_11.configure(relief='flat')
        parent.TLabel2_11.configure(text='''Bandwidth''')

        parent.TLabel2_4 = ttk.Label(labelframe)
        parent.TLabel2_4.place(relx=0.041, rely=self.y+4*self.d, height=32, width=207)
        parent.TLabel2_4.configure(background="#d9d9d9")
        parent.TLabel2_4.configure(foreground="#000000")
        parent.TLabel2_4.configure(font="TkDefaultFont")
        parent.TLabel2_4.configure(relief='flat')
        parent.TLabel2_4.configure(text='''Edge router''')

        parent.TLabel2_4 = ttk.Label(labelframe)
        parent.TLabel2_4.place(relx=0.041, rely=self.y+5*self.d, height=32, width=207)
        parent.TLabel2_4.configure(background="#d9d9d9")
        parent.TLabel2_4.configure(foreground="#000000")
        parent.TLabel2_4.configure(font="TkDefaultFont")
        parent.TLabel2_4.configure(relief='flat')
        parent.TLabel2_4.configure(text='''Logical system (optional)''')

        parent.TLabel2_5 = ttk.Label(labelframe)
        parent.TLabel2_5.place(relx=0.041, rely=self.y+6*self.d, height=32, width=207)
        parent.TLabel2_5.configure(background="#d9d9d9")
        parent.TLabel2_5.configure(foreground="#000000")
        parent.TLabel2_5.configure(font="TkDefaultFont")
        parent.TLabel2_5.configure(relief='flat')
        parent.TLabel2_5.configure(text='''Interface''')


        parent.TLabel2_10 = ttk.Label(labelframe)
        parent.TLabel2_10.place(relx=0.041, rely=self.y+7*self.d, height=32, width=207)
        parent.TLabel2_10.configure(background="#d9d9d9")
        parent.TLabel2_10.configure(foreground="#000000")
        parent.TLabel2_10.configure(font="TkDefaultFont")
        parent.TLabel2_10.configure(relief='flat')
        parent.TLabel2_10.configure(text='''Bandwidth''')

        parent.TLabel2_6 = ttk.Label(labelframe)
        parent.TLabel2_6.place(relx=0.041, rely=self.y+8*self.d, height=32, width=207)
        parent.TLabel2_6.configure(background="#d9d9d9")
        parent.TLabel2_6.configure(foreground="#000000")
        parent.TLabel2_6.configure(font="TkDefaultFont")
        parent.TLabel2_6.configure(relief='flat')
        parent.TLabel2_6.configure(text='''VLAN''')

        parent.TLabel2_8 = ttk.Label(labelframe)
        parent.TLabel2_8.place(relx=0.041, rely=self.y+9*self.d, height=32, width=207)
        parent.TLabel2_8.configure(background="#d9d9d9")
        parent.TLabel2_8.configure(foreground="#000000")
        parent.TLabel2_8.configure(font="TkDefaultFont")
        parent.TLabel2_8.configure(relief='flat')
        parent.TLabel2_8.configure(text='''Virtual circuit (VCID)''')

        parent.TLabel2_9 = ttk.Label(labelframe)
        parent.TLabel2_9.place(relx=0.041, rely=self.y+10*self.d, height=32, width=207)
        parent.TLabel2_9.configure(background="#d9d9d9")
        parent.TLabel2_9.configure(foreground="#000000")
        parent.TLabel2_9.configure(font="TkDefaultFont")
        parent.TLabel2_9.configure(relief='flat')
        parent.TLabel2_9.configure(text='''MTU''')

        parent.TLabel2_11 = ttk.Label(labelframe)
        parent.TLabel2_11.place(relx=0.041, rely=self.y+11*self.d, height=32, width=207)
        parent.TLabel2_11.configure(background="#d9d9d9")
        parent.TLabel2_11.configure(foreground="#000000")
        parent.TLabel2_11.configure(font="TkDefaultFont")
        parent.TLabel2_11.configure(relief='flat')
        parent.TLabel2_11.configure(text='''Control word''')


        #service type entry
        parent.TCombobox1_8.place(relx=0.041, rely=0.025, relheight=0.07
                    , relwidth=0.906)

        keylist = ipDict.keys()
        keylist.sort()
        ipList = []
        for ip in keylist: ipList.append(ip)

        def updateint1(*args):
            self.freevlans = []
            parent.TCombobox2_13.configure(textvar=parent.vlanselect, values=self.freevlans)
            parent.TCombobox2_10.configure(textvar=parent.intselect1, values=intDict[parent.devselect1.get()])
            parent.TCombobox2_10.set('Select interface')
            if not 'Unlimited' in policerDict[parent.devselect1.get()]:
                policerDict[parent.devselect1.get()].insert(0,'Unlimited')
            parent.TCombobox2_18.configure(textvar=parent.polselect1, values=policerDict[parent.devselect1.get()])
            parent.TCombobox2_18.set('Unlimited')
            try: parent.TCombobox2_9.set(ipDict[parent.devselect1.get()][2])
            except IndexError: parent.TCombobox2_9.set('None')

        parent.devselect1 = StringVar(entryframe)
        parent.TCombobox2_1 = ttk.Combobox(entryframe)
        parent.TCombobox2_1.place(relx=0.041, rely=self.y, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_1.configure(width=222)
        parent.TCombobox2_1.configure(takefocus="")
        parent.TCombobox2_1.configure(textvar=parent.devselect1, values=ipList)
        parent.TCombobox2_1.bind("<<ComboboxSelected>>", updateint1)
        parent.TCombobox2_1.set('Select router')


        parent.TCombobox2_9 = ttk.Combobox(entryframe)
        parent.TCombobox2_9.place(relx=0.041, rely=self.y+self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_9.configure(takefocus="")
        parent.TCombobox2_9.set('None')


        def updatevlan(*args):
            if 'Null' in (parent.TCombobox2_10.get(),parent.TCombobox2_15.get()):
                self.freevlans = []
                parent.TCombobox2_13.configure(textvar=parent.vlanselect, values=self.freevlans)
                return
            if 'Select interface' in (parent.TCombobox2_10.get(),parent.TCombobox2_15.get()):
                self.freevlans = []
                parent.TCombobox2_13.configure(textvar=parent.vlanselect, values=self.freevlans)
                return
            parent.loading = loading(entryframe,parent,pbar=[0.041,self.y+8*self.d,0.07,0.906],words='Loading vlans')
            parent.update_idletasks()

            self.freevlans = vlanFinderDualPes(parent.user, parent.key,
                      parent.TCombobox2_1.get(), parent.TCombobox2_10.get(),
                      parent.TCombobox2_11.get(), parent.TCombobox2_15.get(),
                      ipDict,'list',None,None)
            self.freevlans.insert(0,0)
            parent.TCombobox2_13.configure(textvar=parent.vlanselect, values=self.freevlans)
            parent.TCombobox2_13.set('Select')
            parent.config(cursor='')
            parent.update()
            parent.loading.stop(parent)

        parent.intselect1 = StringVar(entryframe)
        parent.TCombobox2_10 = ttk.Combobox(entryframe)
        parent.TCombobox2_10.place(relx=0.041, rely=self.y+2*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_10.configure(takefocus="")
        parent.TCombobox2_10.set('Select interface')
        parent.TCombobox2_10.bind("<<ComboboxSelected>>", updatevlan)


        parent.polselect1 = StringVar(entryframe)
        parent.TCombobox2_18 = ttk.Combobox(entryframe)
        parent.TCombobox2_18.place(relx=0.041, rely=self.y+3*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_18.configure(takefocus="")

        def updateint2(*args):
            self.freevlans = []
            parent.TCombobox2_13.configure(textvar=parent.vlanselect, values=self.freevlans)
            parent.TCombobox2_15.configure(textvar=parent.intselect2, values=intDict[parent.devselect2.get()])
            parent.TCombobox2_15.set('Select interface')
            if not 'Unlimited' in policerDict[parent.devselect2.get()]:
                policerDict[parent.devselect2.get()].insert(0,'Unlimited')
            parent.TCombobox2_17.configure(textvar=parent.polselect12, values=policerDict[parent.devselect2.get()])
            parent.TCombobox2_17.set('Unlimited')
            try: parent.TCombobox2_12.set(ipDict[parent.devselect2.get()][2])
            except IndexError: parent.TCombobox2_12.set('None')

        parent.devselect2 = StringVar(entryframe)
        parent.TCombobox2_11 = ttk.Combobox(entryframe)
        parent.TCombobox2_11.place(relx=0.041, rely=self.y+4*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_11.configure(takefocus="")
        parent.TCombobox2_11.configure(textvar=parent.devselect2, values=ipList)
        parent.TCombobox2_11.bind("<<ComboboxSelected>>", updateint2)
        parent.TCombobox2_11.set('Select router')

        parent.TCombobox2_12 = ttk.Combobox(entryframe)
        parent.TCombobox2_12.place(relx=0.041, rely=self.y+5*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_12.configure(takefocus="")
        parent.TCombobox2_12.set('None')

        parent.intselect2 = StringVar(entryframe)
        parent.TCombobox2_15 = ttk.Combobox(entryframe)
        parent.TCombobox2_15.place(relx=0.041, rely=self.y+6*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_15.configure(takefocus="")
        parent.TCombobox2_15.set('Select interface')
        parent.TCombobox2_15.bind("<<ComboboxSelected>>", updatevlan)


        parent.polselect12 = StringVar(entryframe)
        parent.TCombobox2_17 = ttk.Combobox(entryframe)
        parent.TCombobox2_17.place(relx=0.041, rely=self.y+7*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_17.configure(takefocus="")

        def updatevcid(*args):
            parent.TCombobox2_14.set(parent.TCombobox2_13.get())
            parent.TCombobox2_16.set(1500)

        parent.vlanselect = StringVar(entryframe)
        parent.TCombobox2_13 = ttk.Combobox(entryframe)
        parent.TCombobox2_13.place(relx=0.041, rely=self.y+8*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_13.configure(takefocus="")
        parent.TCombobox2_13.bind("<<ComboboxSelected>>", updatevcid)

        parent.TCombobox2_14 = ttk.Combobox(entryframe)
        parent.TCombobox2_14.place(relx=0.041, rely=self.y+9*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_14.configure(takefocus="")

        parent.TCombobox2_16 = ttk.Combobox(entryframe)
        parent.TCombobox2_16.place(relx=0.041, rely=self.y+10*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_16.configure(takefocus="")

        parent.TCombobox2_19 = ttk.Combobox(entryframe)
        parent.TCombobox2_19.place(relx=0.041, rely=self.y+11*self.d, relheight=0.07
                , relwidth=0.906)
        parent.TCombobox2_19.configure(takefocus="")



class conf():
    def __init__(self,parent,ipDict,intDict,policerDict,service):

        confDict = {}
        self.error = error_icon
        self.warning = warning_icon
        user,key = parent.user, parent.key

        if service == 'Internet':

            pe = parent.TCombobox1.get()
            if not pe in ipDict.keys():
                Dialog(parent,prompt="Edge router unknown\n",icon=self.error)
                return

            ls = parent.TCombobox1_9.get()
            if ls == 'None': ls=False

            iface = parent.TCombobox1_10.get()
            if not iface in intDict[pe] or iface=='Null':
                Dialog(parent,prompt="Interface unknown\n",icon=self.error)
                return

            vlan = parent.TCombobox1_11.get()
            try:
                if int(vlan) not in range(0,4095):
                    Dialog(parent,prompt="VLAN not in correct range\n",icon=self.error)
                    return
            except ValueError:
                Dialog(parent,prompt="VLAN not in correct range\n",icon=self.error)
                return

            ipaddr4 = parent.TCombobox1_12.get()
            ipaddr6 = parent.TCombobox1_13.get()


            if not ipaddr4 and not ipaddr6:
                Dialog(parent,prompt="Please fill the address\n",icon=self.error)
                return

            if ipaddr4:
                try: int(ipaddr4.split('/')[1]) in range(33)
                except ValueError:
                    Dialog(parent,prompt="Specify subnet ipv4 mask\n",icon=self.error)
                    return
                except IndexError:
                    Dialog(parent,prompt="Specify subnet ipv4 mask\n",icon=self.error)
                    return
                try: ipaddr4 = str(validIP(ipaddr4.split('/')[0]))+'/'+ipaddr4.split('/')[1]
                except ValueError:
                    Dialog(parent,prompt="Wrong ipv4 address\n",icon=self.error)
                    return


            if ipaddr6:
                try: int(ipaddr6.split('/')[1]) in range(129)
                except ValueError:
                    Dialog(parent,prompt="Specify subnet ipv6 mask\n",icon=self.error)
                    return
                except IndexError:
                    Dialog(parent,prompt="Specify subnet ipv6 mask\n",icon=self.error)
                    return
                try: ipaddr6 = str(validIP(ipaddr6.split('/')[0]))+'/'+ipaddr6.split('/')[1]
                except ValueError:
                    Dialog(parent,prompt="Wrong ipv6 address\n",icon=self.error)
                    return
            bw = parent.TCombobox1_14.get()
            if not bw in policerDict[pe]:
                Dialog(parent,prompt="Bandwidth is not defined\n",icon=self.error)
                return
            ds = parent.TEntry1.get()
            if not ds:
                Dialog(parent,prompt="Description is not defined\n",icon=self.error)
                return

            d = internetService()

            if ipDict[pe][0] == 'juniper':
                commandList = d.junos(pe,ls,iface,vlan,ipaddr4,ipaddr6,bw,ds)


            elif ipDict[pe][0] == 'cisco':
                commandList = d.cisco(pe,ls,iface,vlan,ipaddr4,ipaddr6,bw,ds)

            confDict[pe] = [ipDict[pe][0],ipDict[pe][1],commandList]

            self.c = ClassSendCommand()
            error = False
            error = self.c.execute(parent,confDict,user,key)
            if error:
                Dialog(parent,prompt='There was an error in configuration of '+pe+
                       ' \nPlease configure the device manually\n', icon = self.warning)

            '''clear the input data '''
            internet(ipDict,intDict,policerDict,parent,parent.Frame3,parent.TFrame1,parent.TFrame1_6,parent.TFrame2) # default selected value is internet
            parent.TEntry1.delete(0,END)

            return

        if service == 'L2mpls':

            pe1 = parent.TCombobox2_1.get()
            if not pe1 in ipDict.keys():
                Dialog(parent,prompt="Edge router unknown\n",icon=self.error)
                return

            ls1 = parent.TCombobox2_9.get()
            if ls1 == 'None': ls1=False

            iface1 = parent.TCombobox2_10.get()
            if not iface1 in intDict[pe1] or iface1=='Null':
                Dialog(parent,prompt="Interface unknown\n",icon=self.error)
                return

            pe2 = parent.TCombobox2_11.get()
            if not pe2 in ipDict.keys():
                Dialog(parent,prompt="Edge router unknown\n",icon=self.error)
                return

            ls2 = parent.TCombobox2_12.get()
            if ls2 == 'None': ls2=False

            iface2 = parent.TCombobox2_15.get()
            if not iface2 in intDict[pe2] or iface2=='Null':
                Dialog(parent,prompt="Interface unknown\n",icon=self.error)
                return

            vlan = parent.TCombobox2_13.get()
            try:
                if not int(vlan) in range(1,4095):
                    Dialog(parent,prompt="VLAN not in correct range\n",icon=self.error)
                    return
            except ValueError:
                Dialog(parent,prompt="VLAN not in correct range\n",icon=self.error)
                return

            vc = parent.TCombobox2_14.get()
            if not vc:
                Dialog(parent,prompt="VCID is not defined\n",icon=self.error)
                return

            mtu = parent.TCombobox2_16.get()
            try:
                if not int(mtu) in range(1,9193):
                    Dialog(parent,prompt="Invalid MTU\n",icon=self.error)
                    return
            except ValueError:
                Dialog(parent,prompt="Invalid MTU\n",icon=self.error)
                return


            bw1 =  parent.TCombobox2_18.get()
            if not bw1 in policerDict[pe1]:
                Dialog(parent,prompt="Bandwidth is not defined\n",icon=self.error)
                return

            bw2 =  parent.TCombobox2_17.get()
            if not bw2 in policerDict[pe2]:
                Dialog(parent,prompt="Bandwidth is not defined\n",icon=self.error)
                return

            ds = parent.TEntry1.get()
            if not ds:
                Dialog(parent,prompt="Description is not defined\n",icon=self.error)
                return

            ncw = False
            d = l2mplsService()

            l2dict = {}
            l2dict[pe1] = [ls1,iface1,vlan,bw1,ds,pe2,vc,mtu,ncw]
            l2dict[pe2] = [ls2,iface2,vlan,bw2,ds,pe1,vc,mtu,ncw]

            for pe in l2dict.keys():
                if ipDict[pe][0] == 'juniper' :
                    commandList = d.junos(pe,l2dict[pe][0],l2dict[pe][1],l2dict[pe][2],l2dict[pe][3],
                                          l2dict[pe][4],l2dict[pe][5],l2dict[pe][6],l2dict[pe][7],l2dict[pe][8])
                    confDict[pe] = [ipDict[pe][0],ipDict[pe][1],commandList]
                elif ipDict[pe1][0] == 'cisco':
                    commandList = d.cisco(pe,l2dict[pe][0],l2dict[pe][1],l2dict[pe][2],l2dict[pe][3],
                                          l2dict[pe][4],l2dict[pe][5],l2dict[pe][6],l2dict[pe][7],l2dict[pe][8])
                    confDict[pe] = [ipDict[pe][0],ipDict[pe][1],commandList]


            self.c = ClassSendCommand()
            error = False
            error = self.c.execute(parent,confDict,user,key)
            if error:
                Dialog(parent,prompt='There was an error in configuration of '+pe+
                       ' \nPlease configure the device manually\n', icon = self.warning)

            '''clear the input data '''
            l2mpls(ipDict,intDict,policerDict,parent,parent.Frame3,parent.TFrame1,parent.TFrame1_6,parent.TFrame2)
            parent.TEntry1.delete(0,END)

            return



class internetService():

    def junos(self,pe,ls,iface,vlan,ipaddr4,ipaddr6,bw,ds):
        commandList = []
        if ls: commandList.append('show configuration logical-systems '+ls+' interface '+iface+'.'+vlan)
        else: commandList.append('show configuration interface '+iface+'.'+vlan)
        commandList.append('configure private')
        if ls: commandList.append('edit logical-systems '+ls)
        commandList.append('edit interface '+iface+'.'+vlan)
        if int(vlan) != 0:
            commandList.append('set vlan-id '+vlan)
        if ipaddr4:
            commandList.append('set family inet address '+ipaddr4)
            if bw != 'Unlimited':
                commandList.append('set family inet policer input '+bw)
                commandList.append('set family inet policer output '+bw)
        if ipaddr6:
            commandList.append('set family inet6 address '+ipaddr6)
            if bw != 'Unlimited':
                commandList.append('set family inet6 policer input '+bw)
                commandList.append('set family inet6 policer output '+bw)
        commandList.append('set description "'+ds+'"')
        commandList.append('top')
        commandList.append('show | compare')
        commandList.append('commit and-quit')
        if ls: commandList.append('show configuration logical-systems '+ls+' interface '+iface+'.'+vlan)
        else: commandList.append('show configuration interface '+iface+'.'+vlan)
        if ipaddr4:
            if ls:
                commandList.append('ping rapid '+ipaddr4.split('/')[0]+' logical-system '+ls)
                commandList.append('ping rapid 8.8.8.8 source '+ipaddr4.split('/')[0]+' logical-system '+ls)
            else:
                commandList.append('ping rapid '+ipaddr4.split('/')[0])
                commandList.append('ping rapid 8.8.8.8 source '+ipaddr4.split('/')[0])
        if ipaddr6:
            if ls:
                commandList.append('ping rapid '+ipaddr6.split('/')[0]+' logical-system '+ls)
                commandList.append('ping rapid 2001:4860:4860::8888 source '+ipaddr6.split('/')[0]+' logical-system '+ls)
            else:
                commandList.append('ping rapid '+ipaddr6.split('/')[0])
                commandList.append('ping rapid 2001:4860:4860::8888 source '+ipaddr6.split('/')[0])
        return commandList


    def cisco(self,pe,ls,iface,vlan,ipaddr4,ipaddr6,bw,ds):
        ipaddr4 = (ipaddr.IPv4Network(ipaddr4).with_netmask).replace('/',' ')
        commandList = []
        ls = False
        if int(vlan) !=0:
            commandList.append('show running-config interface '+iface+'.'+vlan)
        else: commandList.append('show running-config interface '+iface)
        commandList.append('configure terminal')
        if int(vlan) !=0:
            commandList.append('interface '+iface+'.'+vlan)
            commandList.append('encapsulation dot1q '+vlan)
        else: commandList.append('interface '+iface)
        if ipaddr4:
            commandList.append('ip address '+ipaddr4)
            if bw != 'Unlimited':
                commandList.append('service-policy input '+bw)
                commandList.append('service-policy output '+bw)
        if ipaddr6:
            commandList.append('ipv6 address '+ipaddr6)
            if bw != 'Unlimited':
                commandList.append('service-policy input '+bw)
                commandList.append('service-policy output '+bw)
        commandList.append('description '+ds)
        commandList.append('end')
        commandList.append('write memory')
        if int(vlan) !=0:
            commandList.append('show running-config interface '+iface+'.'+vlan)
        else: commandList.append('show running-config interface '+iface)
        if ipaddr4:
            commandList.append('ping '+ipaddr4.split()[0]+' timeout 0')
            commandList.append('ping 8.8.8.8 source '+ipaddr4.split()[0]+' timeout 0')
        if ipaddr6:
            commandList.append('ping '+ipaddr6.split('/')[0]+' timeout 0')
            commandList.append('ping 2001:4860:4860::8888 source '+ipaddr6.split('/')[0]+' timeout 0')
        return commandList


class l2mplsService():

    def junos(self,pe,ls,iface,vlan,bw,ds,neighbor,vc,mtu,ncw):
        commandList = []
        if ls: commandList.append('show configuration logical-systems '+ls+' interface '+iface+'.'+vlan)
        else: commandList.append('show configuration interface '+iface+'.'+vlan)
        commandList.append('configure private')
        if ls: commandList.append('edit logical-systems '+ls)
        commandList.append('edit interface '+iface+'.'+vlan)
        if int(vlan) != 0:
            commandList.append('set vlan-id '+vlan)
        commandList.append('set encapsulation vlan-ccc')
        if bw != 'Unlimited':
            commandList.append('set family ccc policer input '+bw)
            commandList.append('set family ccc policer output '+bw)
        commandList.append('set description "'+ds+'"')
        commandList.append('exit')
        commandList.append('edit protocols l2circuit')
        commandList.append('edit neighbor '+neighbor)
        commandList.append('edit interface '+iface+'.'+vlan)
        commandList.append('set description "'+ds+'"')
        commandList.append('set virtual-circuit-id '+vlan)
        if mtu: commandList.append('set mtu '+mtu)
        if ncw: commandList.append('set no-control-word')

        commandList.append('top')
        commandList.append('show | compare')
        commandList.append('commit and-quit')

        if ls: commandList.append('show configuration logical-systems '+ls+' interface '+iface+'.'+vlan)
        else:  commandList.append('show configuration interface '+iface+'.'+vlan)

        if ls: commandList.append('show configuration logical-systems '+ls+' protocols l2circuit neighbor '
                                   +neighbor+' interface '+iface+'.'+vlan)
        else:  commandList.append('show configuration protocols l2circuit neighbor '
                                   +neighbor+' interface '+iface+'.'+vlan)

        if ls: commandList.append('show l2circuit connections interface '
                                   +iface+'.'+vlan+' neighbor '+neighbor+' summary  logical-system '+ls)
        else:  commandList.append('show l2circuit connections interface '
                                   +iface+'.'+vlan+' neighbor '+neighbor+' summary')

        if ls: commandList.append('ping mpls l2circuit interface '+iface+'.'+vlan+
                          ' logical-system '+ls+' reply-mode application-level-control-channel')
        else: commandList.append('ping mpls l2circuit interface '+iface+'.'+vlan+
                          ' reply-mode application-level-control-channel')

        return commandList


    def cisco(self,pe,ls,iface,vlan,bw,ds,neighbor,vc,mtu,ncw):
        commandList = []
        ls = False
        if int(vlan) !=0:
            commandList.append('show running-config interface '+iface+'.'+vlan)
        else: commandList.append('show running-config interface '+iface)
        commandList.append('configure terminal')
        if not cw:
             commandList.append('pseudowire-class L2CIRCUIT')
             commandList.append('encapsulation mpls')
             commandList.append('no control-word')
        if int(vlan) !=0:
            commandList.append('interface '+iface+'.'+vlan)
            commandList.append('encapsulation dot1q '+vlan)
        else: commandList.append('interface '+iface)
        if bw != 'unlimited':
            commandList.append('service-policy input '+bw)
            commandList.append('service-policy output '+bw)
        commandList.append('set description "'+ds+'"')
        if ncw:
            commandList.append('xconnect '+neighbor+' '+vc+' pw-class L2CIRCUIT')
        else: commandList.append('xconnect '+neighbor+' '+vc+' encapsulation mpls')
        if mtu: commandList.append('mtu '+mtu)


        commandList.append('end')
        commandList.append('write memory')

        if int(vlan) !=0:
            commandList.append('show running-config interface '+iface+'.'+vlan)
        else: commandList.append('show running-config interface '+iface)

        if int(vlan) !=0:
            commandList.append('show xconnect interface '+iface+'.'+vlan)
        else: commandList.append('show xconnect interface '+iface)

        commandList.append('ping mpls pseudowire '+neighbor+'.'+vc+'timeout 0')

        return commandList


def test():
    username = 'fisi'
    password = 'fisi123'
    from initial import getIpFromFile, showInterfaces,showPolicer
    ipDict = getIpFromFile(path='c:\users\u\desktop\pacom\\')
    intDict = showInterfaces(username,password,ipDict)
    policerDict = showPolicer(username,password,ipDict)
    d = ServiceProvision(username,password,ipDict,intDict,policerDict)
    d.mainloop()

if __name__ == '__main__':
   test()
