# This module is part of the core Basondole Tools
# This code provided GUI for input data to be used with bBurst
# AUTHOR: Paul S.I. Basondole

import Tkinter
from Tkinter import *
import ttk

from vFinderUnNC import getUsedVlanDesc
from bEditorNC import bEditorbutton

from ClassLoading import loading
from ClassDialog import Dialog

# variables for GUI icons
warning_icon="C:\Users\u\Desktop\PACOM\icon\warning-icon.png"


class BurstPackages(Tkinter.Toplevel):
    def __init__(self,username,password,ipDict,intDict,policerDict,serverdata,choice=None):

        self.user = username
        self.key = password

        if not choice: title = 'Untitled'

        Toplevel.__init__(self)
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

        self.geometry("570x690+442+154")
        self.resizable(width=False, height=False)
        self.title(choice)
        self.configure(background="#d9d9d9")

        self.Frame1 = Tkinter.Frame(self)
        self.Frame1.place(relx=0.013, rely=0.014, relheight=0.978
                , relwidth=0.974)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(width=555)

        self.Label1 = Tkinter.Label(self.Frame1)
        self.Label1.place(relx=0.013, rely=0.015, height=43, width=193)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font11)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#f0f0f0f0f0f0")
        self.Label1.configure(text='''Burst Packages''')


        self.Frame3 = Tkinter.Frame(self.Frame1)
        self.Frame3.place(relx=0.013, rely=0.104, relheight=0.881, relwidth=0.964)


        self.Frame3.configure(background="#d9d9d9")
        self.Frame3.configure(highlightbackground="#d9d9d9")
        self.Frame3.configure(highlightcolor="black")
        self.Frame3.configure(width=535)

        self.Frame3_9 = Tkinter.Frame(self.Frame3)
        self.Frame3_9.place(relx=0.037, rely=0.034, relheight=0.261
                , relwidth=0.925)
        self.Frame3_9.configure(relief='groove')
        self.Frame3_9.configure(borderwidth="2")
        self.Frame3_9.configure(relief='groove')
        self.Frame3_9.configure(background="#d9d9d9")
        self.Frame3_9.configure(highlightbackground="#d9d9d9")
        self.Frame3_9.configure(highlightcolor="black")
        self.Frame3_9.configure(width=495)

        ipList = ipDict.keys()
        ipList.sort()

        def updateint(*args):
            self.usedvlans = []
            self.TEntry1_12.delete(0,END)
            self.TCombobox1_6.configure(textvar=self.vlanselect, values=self.usedvlans)
            self.TCombobox1_6.set('')
            self.TCombobox1_5.configure(textvar=self.intselect, values=intDict[self.devselect.get()])
            self.TCombobox1_5.set('Select interface')
            self.TCombobox1_10.configure(textvar=self.cirselect, values=policerDict[self.devselect.get()])
            self.TCombobox1_10.set('Select CIR')
            self.TCombobox1_11.configure(textvar=self.pirselect, values=policerDict[self.devselect.get()])
            self.TCombobox1_11.set('Select PIR')


        self.devselect =StringVar(self.Frame3_9)
        self.TCombobox1_4 = ttk.Combobox(self.Frame3_9)
        self.TCombobox1_4.place(relx=0.02, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_4.configure(textvariable=self.devselect, values=ipList)
        self.TCombobox1_4.configure(takefocus="")
        self.TCombobox1_4.bind("<<ComboboxSelected>>", updateint)



        def updatevlan(*args):
            self.TEntry1_12.delete(0,END)
            if self.TCombobox1_5.get() == 'Null':
                self.usedvlans = []
                self.TCombobox1_6.configure(textvar=self.vlanselect, values=self.usedvlans)
                return
            self.loading = loading(self.Frame3_9,self,pbar=[0.505,0.71,0.2,0.448],words='Loading vlans')
            self.update_idletasks()
            self.vlanDict = getUsedVlanDesc(self.TCombobox1_4.get(),ipDict,self.TCombobox1_5.get(),self.user,self.key)
            self.usedvlans = self.vlanDict.keys()
            self.usedvlans.sort()
            self.TCombobox1_6.configure(textvar=self.vlanselect, values=self.usedvlans)
            self.TCombobox1_6.set('Select')
            self.config(cursor='')
            self.update()
            self.loading.stop(self)

        self.intselect =StringVar(self.Frame3_9)
        self.TCombobox1_5 = ttk.Combobox(self.Frame3_9)
        self.TCombobox1_5.place(relx=0.02, rely=0.71, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_5.configure(takefocus="")
        self.TCombobox1_5.bind("<<ComboboxSelected>>", updatevlan)


        def updatedesc(*args):
            self.TEntry1_12.delete(0,END)
            self.TEntry1_12.insert(0,self.vlanDict[self.vlanselect.get()])

        self.vlanselect = StringVar(self.Frame3_9)
        self.TCombobox1_6 = ttk.Combobox(self.Frame3_9)
        self.TCombobox1_6.place(relx=0.505, rely=0.71, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_6.configure(takefocus="")
        self.TCombobox1_6.bind("<<ComboboxSelected>>", updatedesc)

        self.TLabel1_6 = ttk.Label(self.Frame3_9)
        self.TLabel1_6.place(relx=0.02, rely=0.065, height=29, width=150)
        self.TLabel1_6.configure(background="#d9d9d9")
        self.TLabel1_6.configure(foreground="#000000")
        self.TLabel1_6.configure(font="TkDefaultFont")
        self.TLabel1_6.configure(relief='flat')
        self.TLabel1_6.configure(text='''Edge router''')

        self.TLabel1_7 = ttk.Label(self.Frame3_9)
        self.TLabel1_7.place(relx=0.02, rely=0.516, height=29, width=100)
        self.TLabel1_7.configure(background="#d9d9d9")
        self.TLabel1_7.configure(foreground="#000000")
        self.TLabel1_7.configure(font="TkDefaultFont")
        self.TLabel1_7.configure(relief='flat')
        self.TLabel1_7.configure(text='''Interface''')

        self.TLabel1_8 = ttk.Label(self.Frame3_9)
        self.TLabel1_8.place(relx=0.505, rely=0.516, height=29, width=100)
        self.TLabel1_8.configure(background="#d9d9d9")
        self.TLabel1_8.configure(foreground="#000000")
        self.TLabel1_8.configure(font="TkDefaultFont")
        self.TLabel1_8.configure(relief='flat')
        self.TLabel1_8.configure(text='''VLAN''')

        self.Frame3_10 = Tkinter.Frame(self.Frame3)
        self.Frame3_10.place(relx=0.037, rely=0.319, relheight=0.261
                , relwidth=0.925)
        self.Frame3_10.configure(relief='groove')
        self.Frame3_10.configure(borderwidth="2")
        self.Frame3_10.configure(relief='groove')
        self.Frame3_10.configure(background="#d9d9d9")
        self.Frame3_10.configure(highlightbackground="#d9d9d9")
        self.Frame3_10.configure(highlightcolor="black")
        self.Frame3_10.configure(width=495)

        self.dayselect = StringVar(self.Frame3_10)
        self.TCombobox1_7 = ttk.Combobox(self.Frame3_10)
        self.TCombobox1_7.place(relx=0.02, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_7.configure(textvariable=self.dayselect, values=['weekdays','weekends'])
        self.TCombobox1_7.configure(takefocus="")
        self.TCombobox1_7.configure(state='readonly')

        self.starttime = StringVar(self.Frame3_10)
        self.TCombobox1_8 = ttk.Combobox(self.Frame3_10)
        self.TCombobox1_8.place(relx=0.02, rely=0.71, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_8.configure(textvariable=self.starttime, values=['1800'])
        self.TCombobox1_8.configure(takefocus="")
        self.TCombobox1_8.configure(state='readonly')

        self.endtime = StringVar(self.Frame3_10)
        self.TCombobox1_9 = ttk.Combobox(self.Frame3_10)
        self.TCombobox1_9.place(relx=0.505, rely=0.71, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_9.configure(textvariable=self.endtime, values=['0600','0800'])
        self.TCombobox1_9.configure(takefocus="")
        self.TCombobox1_9.configure(state='readonly')

        self.TLabel1_9 = ttk.Label(self.Frame3_10)
        self.TLabel1_9.place(relx=0.02, rely=0.065, height=29, width=150)
        self.TLabel1_9.configure(background="#d9d9d9")
        self.TLabel1_9.configure(foreground="#000000")
        self.TLabel1_9.configure(font="TkDefaultFont")
        self.TLabel1_9.configure(relief='flat')
        self.TLabel1_9.configure(text='''Days applicable''')

        self.TLabel1_10 = ttk.Label(self.Frame3_10)
        self.TLabel1_10.place(relx=0.02, rely=0.516, height=29, width=100)
        self.TLabel1_10.configure(background="#d9d9d9")
        self.TLabel1_10.configure(foreground="#000000")
        self.TLabel1_10.configure(font="TkDefaultFont")
        self.TLabel1_10.configure(relief='flat')
        self.TLabel1_10.configure(text='''Start time''')

        self.TLabel1_11 = ttk.Label(self.Frame3_10)
        self.TLabel1_11.place(relx=0.505, rely=0.516, height=29, width=100)
        self.TLabel1_11.configure(background="#d9d9d9")
        self.TLabel1_11.configure(foreground="#000000")
        self.TLabel1_11.configure(font="TkDefaultFont")
        self.TLabel1_11.configure(relief='flat')
        self.TLabel1_11.configure(text='''End time''')

        self.Frame3_11 = Tkinter.Frame(self.Frame3)
        self.Frame3_11.place(relx=0.037, rely=0.604, relheight=0.261
                , relwidth=0.925)
        self.Frame3_11.configure(relief='groove')
        self.Frame3_11.configure(borderwidth="2")
        self.Frame3_11.configure(relief='groove')
        self.Frame3_11.configure(background="#d9d9d9")
        self.Frame3_11.configure(highlightbackground="#d9d9d9")
        self.Frame3_11.configure(highlightcolor="black")
        self.Frame3_11.configure(width=495)


        self.cirselect = StringVar(self.Frame3_11)
        self.TCombobox1_10 = ttk.Combobox(self.Frame3_11)
        self.TCombobox1_10.place(relx=0.02, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_10.configure(takefocus="")


        self.pirselect = StringVar(self.Frame3_11)
        self.TCombobox1_11 = ttk.Combobox(self.Frame3_11)
        self.TCombobox1_11.place(relx=0.505, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_11.configure(takefocus="")

        self.TLabel1_10 = ttk.Label(self.Frame3_11)
        self.TLabel1_10.place(relx=0.02, rely=0.516, height=29, width=150)
        self.TLabel1_10.configure(background="#d9d9d9")
        self.TLabel1_10.configure(foreground="#000000")
        self.TLabel1_10.configure(font="TkDefaultFont")
        self.TLabel1_10.configure(relief='flat')
        self.TLabel1_10.configure(text='''Client name''')

        self.TLabel1_11 = ttk.Label(self.Frame3_11)
        self.TLabel1_11.place(relx=0.02, rely=0.065, height=29, width=160)
        self.TLabel1_11.configure(background="#d9d9d9")
        self.TLabel1_11.configure(foreground="#000000")
        self.TLabel1_11.configure(font="TkDefaultFont")
        self.TLabel1_11.configure(relief='flat')
        self.TLabel1_11.configure(text='''Subscription (CIR)''')

        self.TLabel1_12 = ttk.Label(self.Frame3_11)
        self.TLabel1_12.place(relx=0.505, rely=0.065, height=29, width=100)
        self.TLabel1_12.configure(background="#d9d9d9")
        self.TLabel1_12.configure(foreground="#000000")
        self.TLabel1_12.configure(font="TkDefaultFont")
        self.TLabel1_12.configure(relief='flat')
        self.TLabel1_12.configure(text='''Burst (PIR)''')

        self.TEntry1_12 = ttk.Entry(self.Frame3_11)
        self.TEntry1_12.place(relx=0.02, rely=0.71, relheight=0.2
                , relwidth=0.933)
        self.TEntry1_12.configure(takefocus="")
        self.TEntry1_12.configure(cursor="ibeam")

        self.Button1 = Tkinter.Button(self.Frame3)
        self.Button1.place(relx=0.093, rely=0.900, height=42, width=158)
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Save''')
        self.Button1.configure(command= lambda: conf(self,ipDict,intDict,policerDict,serverdata,choice))

        self.Button1_13 = Tkinter.Button(self.Frame3)
        self.Button1_13.place(relx=0.550, rely=0.900, height=42, width=158)
        self.Button1_13.configure(pady="0")
        self.Button1_13.configure(text='''Clear''')
        self.Button1_13.configure(command= lambda: self.clear())

        if choice == 'Remove client':
            self.geometry("570x400")
            self.Label1.place(relx=0.013, rely=0.01, height=43, width=193)
            self.Frame3_9.place(relx=0.037, rely=0.1, relheight=0.461
                , relwidth=0.925)
            self.Button1.place(relx=0.093, rely=0.700, height=42, width=158)
            self.Button1_13.place(relx=0.550, rely=0.700, height=42, width=158)
            self.Frame3_10.place_forget()
            self.Frame3_11.place_forget()


    def clear(self):
       comboboxes = [self.TCombobox1_4,self.TCombobox1_5,self.TCombobox1_6,
                     self.TCombobox1_7,self.TCombobox1_8,self.TCombobox1_9,
                     self.TCombobox1_10,self.TCombobox1_11]
       for cbox in comboboxes: cbox.set('')
       self.TEntry1_12.delete(0,END)



class  conf():
    def __init__(self,parent,ipDict,intDict,policerDict,serverdata,choice):

            pe = parent.TCombobox1_4.get()
            if not pe in ipDict.keys():
                Dialog(parent,prompt="Edge router unknown\n",
                       icon= warning_icon)
                return


            iface = parent.TCombobox1_5.get()
            if not iface in intDict[pe] or iface=='Null':
                Dialog(parent,prompt="Interface unknown\n")
                return

            vlan = parent.TCombobox1_6.get()
            try:
                if int(vlan) not in range(0,4095):
                    Dialog(parent,prompt="VLAN not in correct range\n")
                    return
            except ValueError:
                Dialog(parent,prompt="VLAN not in correct range\n")
                return

            if choice != 'Remove client':
                days = parent.TCombobox1_7.get()
                if not days:
                    Dialog(parent,prompt="Specify applicable days\n")
                    return

                st = parent.TCombobox1_8.get()
                if not st:
                    Dialog(parent,prompt="Specify start time\n")
                    return

                et = parent.TCombobox1_9.get()
                if not et:
                    Dialog(parent,prompt="Specify end time\n")
                    return

                cir = parent.TCombobox1_10.get()
                if not cir in policerDict[pe]:
                    Dialog(parent,prompt="CIR is not defined\n")
                    return

                pir = parent.TCombobox1_11.get()
                if not pir in policerDict[pe]:
                    Dialog(parent,prompt="PIR is not defined\n")
                    return

                ds = parent.TEntry1_12.get()
                if not ds:
                    Dialog(parent,prompt="Client name is not defined\n")
                    return
                ds = ds.replace(' ','-')

                data = [pe,iface,vlan,cir,pir,st,et,days,ds]
            else: data = [pe,iface,vlan]

            serverlogin = serverdata[0]
            server = serverdata[1]
            FQP = serverdata[2]

            parent.loading = loading(parent.Frame3,parent,pbar=[0.093,0.9,0.08,0.300],words='Loading')
            parent.update_idletasks()

            bEditorbutton(parent,serverlogin,server,FQP,choice,data)

            parent.config(cursor='')
            parent.update()
            parent.loading.stop(parent)

            parent.clear()


def test():
    username = 'fisi'
    password = 'fisi123'
    from initial import getIpFromFile, showInterfaces,showPolicer
    ipDict = getIpFromFile(path='c:\users\u\desktop\pacom')
    intDict = showInterfaces(username,password,ipDict)
    policerDict = showPolicer(username,password,ipDict)
    serverdata = ['basondole','192.168.56.2','/home/basondole/remotefile']
    d=BurstPackages(username,password,ipDict,intDict,policerDict,serverdata,choice = 'Add client')
    d.mainloop()

if __name__ == '__main__':
   test()
