# This module is part of the core Basondole Tools
# This code creates a GUI for input data that will be used by bonDemand
# AUTHOR: Paul S.I. Basondole

import Tkinter
from Tkinter import *
import ttk
import datetime
import time

from vFinderUnNC import getUsedVlanDesc
from bOnDemandNC import boDbutton
from bOnDemandNC import Server

from ClassLoading import loading
from ClassDialog import Dialog
from ClassSendCommand import ClassSendCommand


# Variables for GUI elements
warning_icon = "C:\Users\u\Desktop\PACOM\icon\warning-icon.png"
error_icon = "C:\Users\u\Desktop\PACOM\icon\error-icon.png"
check_icon = "C:\Users\u\Desktop\PACOM\icon\check-icon.png"


class BandwidthOnDemand(Tkinter.Toplevel):

    def __init__(self,username,password,ipDict,intDict,policerDict,serverdata,choice=None):

        self.username = username
        self.password = password
        self.serverlogin = serverdata[0]
        self.server = serverdata[1]
        self.scriptPath = serverdata[2]

        if choice:
            self.choice = choice
        else: self.choice = False

        Tkinter.Toplevel.__init__(self)

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family Calibri -size 15 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        self.style = ttk.Style()
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        self.geometry("570x690+346+156")
        self.resizable(width=False,height=False)
        self.title("Bandwidth on Demand")
        self.configure(background="#d9d9d9")
        self.configure(highlightbackground="#d9d9d9")
        self.configure(highlightcolor="black")

        self.Frame1 = Tkinter.Frame(self)
        self.Frame1.place(relx=0.018, rely=0.014, relheight=0.978
                , relwidth=0.974)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=555)

        self.Label1 = Tkinter.Label(self.Frame1)
        self.Label1.place(relx=0.018, rely=0.015, height=43, width=289)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font9)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#f0f0f0f0f0f0")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Bandwidth on demand''')


        self.Frame3 = Tkinter.Frame(self.Frame1)
        self.Frame3.place(relx=0.018, rely=0.104, relheight=0.881
                , relwidth=0.964)
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(background="#d9d9d9")
        self.Frame3.configure(highlightbackground="#d9d9d9")
        self.Frame3.configure(highlightcolor="black")
        self.Frame3.configure(width=535)

        self.Frame3_9 = Tkinter.Frame(self.Frame3)
        self.Frame3_9.place(relx=0.037, rely=0.218, relheight=0.261
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
            self.TCombobox1_6.configure(textvar=self.intselect, values=intDict[self.devselect.get()])
            self.TCombobox1_6.set('Select interface')
            self.TCombobox1_7.configure(textvar=self.vlanselect, values=self.usedvlans)
            self.TCombobox1_7.set('')
            self.TCombobox1_10.configure(textvar=self.cirselect, values=policerDict[self.devselect.get()])
            self.TCombobox1_10.set('Select')
            self.TCombobox1_11.configure(textvar=self.pirselect, values=policerDict[self.devselect.get()])
            self.TCombobox1_11.set('Select')
            try: self.TCombobox1_4.set(ipDict[self.devselect.get()][2])
            except IndexError: self.TCombobox1_4.set('None')


        self.devselect = Tkinter.StringVar(self.Frame3_9)
        self.TCombobox1_5 = ttk.Combobox(self.Frame3_9)
        self.TCombobox1_5.place(relx=0.02, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_5.configure(takefocus="")
        self.TCombobox1_5.configure(textvariable=self.devselect, values=ipList)
        self.TCombobox1_5.bind("<<ComboboxSelected>>", updateint)


        self.TCombobox1_4 = ttk.Combobox(self.Frame3_9)
        self.TCombobox1_4.place(relx=0.505, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_4.configure(takefocus="")

        def updatevlan(*args):
            self.TEntry1_12.delete(0,END)
            if self.TCombobox1_6.get() == 'Null':
                self.usedvlans = []
                self.TCombobox1_7.configure(textvar=self.vlanselect, values=self.usedvlans)
                return
            self.loading = loading(self.Frame3_9,self,pbar=[0.505,0.71,0.2,0.448],words='Loading vlans')
            self.update_idletasks()
            self.vlanDict = getUsedVlanDesc(self.TCombobox1_5.get(),ipDict,self.TCombobox1_6.get(),self.username,self.password)
            self.usedvlans = self.vlanDict.keys()
            self.usedvlans.sort()
            self.TCombobox1_7.configure(textvar=self.vlanselect, values=self.usedvlans)
            self.TCombobox1_7.set('Select')
            self.config(cursor='')
            self.update()
            self.loading.stop(self)

        self.intselect = Tkinter.StringVar(self.Frame3_9)
        self.TCombobox1_6 = ttk.Combobox(self.Frame3_9)
        self.TCombobox1_6.place(relx=0.02, rely=0.71, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_6.configure(takefocus="")
        self.TCombobox1_6.bind("<<ComboboxSelected>>", updatevlan)

        def updatedesc(*args):
            self.TEntry1_12.delete(0,END)
            self.TEntry1_12.insert(0,self.vlanDict[self.vlanselect.get()])

        self.vlanselect = Tkinter.StringVar(self.Frame3_9)
        self.TCombobox1_7 = ttk.Combobox(self.Frame3_9)
        self.TCombobox1_7.place(relx=0.505, rely=0.71, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_7.configure(takefocus="")
        self.TCombobox1_7.bind("<<ComboboxSelected>>", updatedesc)

        self.TLabel1_7 = ttk.Label(self.Frame3_9)
        self.TLabel1_7.place(relx=0.02, rely=0.06, height=29, width=150)
        self.TLabel1_7.configure(background="#d9d9d9")
        self.TLabel1_7.configure(foreground="#000000")
        self.TLabel1_7.configure(font="TkDefaultFont")
        self.TLabel1_7.configure(relief='flat')
        self.TLabel1_7.configure(text='''Edge router''')

        self.TLabel1_6 = ttk.Label(self.Frame3_9)
        self.TLabel1_6.place(relx=0.505, rely=0.06, height=29, width=150)
        self.TLabel1_6.configure(background="#d9d9d9")
        self.TLabel1_6.configure(foreground="#000000")
        self.TLabel1_6.configure(font="TkDefaultFont")
        self.TLabel1_6.configure(relief='flat')
        self.TLabel1_6.configure(text='''Logical system''')

        self.TLabel1_8 = ttk.Label(self.Frame3_9)
        self.TLabel1_8.place(relx=0.02, rely=0.516, height=29, width=100)
        self.TLabel1_8.configure(background="#d9d9d9")
        self.TLabel1_8.configure(foreground="#000000")
        self.TLabel1_8.configure(font="TkDefaultFont")
        self.TLabel1_8.configure(relief='flat')
        self.TLabel1_8.configure(text='''Interface''')

        self.TLabel1_9 = ttk.Label(self.Frame3_9)
        self.TLabel1_9.place(relx=0.505, rely=0.516, height=29, width=100)
        self.TLabel1_9.configure(background="#d9d9d9")
        self.TLabel1_9.configure(foreground="#000000")
        self.TLabel1_9.configure(font="TkDefaultFont")
        self.TLabel1_9.configure(relief='flat')
        self.TLabel1_9.configure(text='''VLAN''')

        self.Frame3_10 = Tkinter.Frame(self.Frame3)
        self.Frame3_10.place(relx=0.037, rely=0.034, relheight=0.16
                , relwidth=0.925)
        self.Frame3_10.configure(relief='groove')
        self.Frame3_10.configure(borderwidth="2")
        self.Frame3_10.configure(relief='groove')
        self.Frame3_10.configure(background="#d9d9d9")
        self.Frame3_10.configure(highlightbackground="#d9d9d9")
        self.Frame3_10.configure(highlightcolor="black")
        self.Frame3_10.configure(width=495)

        # Service ticket
        self.TCombobox1_8 = ttk.Combobox(self.Frame3_10)
        self.TCombobox1_8.place(relx=0.02, rely=0.35, relheight=0.326
                , relwidth=0.448)
        self.TCombobox1_8.configure(takefocus="")
        if choice:
            def updateothers(*args):
                self.TCombobox1_5.set(self.bigdict[self.sts.get()][0])
                self.TCombobox1_6.set(self.bigdict[self.sts.get()][1])
                self.TCombobox1_7.set(self.bigdict[self.sts.get()][2])
                self.TCombobox1_9.set(self.bigdict[self.sts.get()][5])
                self.TCombobox1_10.configure(textvar=self.cirselect, values=policerDict[self.devselect.get()])
                self.TCombobox1_10.set(self.bigdict[self.sts.get()][3])
                self.TCombobox1_11.configure(textvar=self.pirselect, values=policerDict[self.devselect.get()])
                self.TCombobox1_11.set('Select')

            serv = Server(self.serverlogin,self.server,self.scriptPath,'*')
            if serv.up:
                self.bigdict = serv.retrieveRemoteFile(bigdict=True)
                self.sts = StringVar(self.Frame3_10)
                self.TCombobox1_8.configure(state='readonly')
                self.TCombobox1_8.configure(textvar=self.sts,values=self.bigdict.keys())
                self.TCombobox1_8.bind("<<ComboboxSelected>>", updateothers)
            else: Dialog(self.parent,prompt='Can not access server \n'+server+' \n')


        # revert date
        self.TCombobox1_9 = ttk.Combobox(self.Frame3_10)
        self.TCombobox1_9.place(relx=0.505, rely=0.35, relheight=0.326
                , relwidth=0.448)
        self.TCombobox1_9.configure(takefocus="")

        self.TLabel1_11 = ttk.Label(self.Frame3_10)
        self.TLabel1_11.place(relx=0.02, rely=0.02, height=29, width=130)
        self.TLabel1_11.configure(background="#d9d9d9")
        self.TLabel1_11.configure(foreground="#000000")
        self.TLabel1_11.configure(font="TkDefaultFont")
        self.TLabel1_11.configure(relief='flat')
        self.TLabel1_11.configure(text='''Service ticket''')
        self.TLabel1_11.configure(width=130)

        self.TLabel1_12 = ttk.Label(self.Frame3_10)
        self.TLabel1_12.place(relx=0.505, rely=0.02, height=29, width=180)
        self.TLabel1_12.configure(background="#d9d9d9")
        self.TLabel1_12.configure(foreground="#000000")
        self.TLabel1_12.configure(font="TkDefaultFont")
        self.TLabel1_12.configure(relief='flat')
        self.TLabel1_12.configure(text='''Revert date''')


        self.TLabel1_13 = ttk.Label(self.Frame3_10)
        self.TLabel1_13.place(relx=0.50, rely=0.70, height=20, width=240)
        self.TLabel1_13.configure(justify='left')
        font14 = "-family {Segoe UI} -size 7 -weight normal -slant "  \
             "italic -underline 0 -overstrike 0"
        self.TLabel1_13.configure(font=font14,anchor='w')
        self.TLabel1_13.configure(text='eg: June 1 2019 or 10 days')


        self.Frame3_11 = Tkinter.Frame(self.Frame3)
        self.Frame3_11.place(relx=0.037, rely=0.504, relheight=0.261
                , relwidth=0.925)
        self.Frame3_11.configure(relief='groove')
        self.Frame3_11.configure(borderwidth="2")
        self.Frame3_11.configure(relief='groove')
        self.Frame3_11.configure(background="#d9d9d9")
        self.Frame3_11.configure(highlightbackground="#d9d9d9")
        self.Frame3_11.configure(highlightcolor="black")
        self.Frame3_11.configure(width=495)

        self.cirselect = Tkinter.StringVar(self.Frame3_11)
        self.TCombobox1_10 = ttk.Combobox(self.Frame3_11)
        self.TCombobox1_10.place(relx=0.02, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_10.configure(takefocus="")

        self.pirselect = Tkinter.StringVar(self.Frame3_11)
        self.TCombobox1_11 = ttk.Combobox(self.Frame3_11)
        self.TCombobox1_11.place(relx=0.505, rely=0.258, relheight=0.2
                , relwidth=0.448)
        self.TCombobox1_11.configure(takefocus="")

        self.TLabel1_11 = ttk.Label(self.Frame3_11)
        self.TLabel1_11.place(relx=0.02, rely=0.516, height=29, width=190)
        self.TLabel1_11.configure(background="#d9d9d9")
        self.TLabel1_11.configure(foreground="#000000")
        self.TLabel1_11.configure(font="TkDefaultFont")
        self.TLabel1_11.configure(relief='flat')
        self.TLabel1_11.configure(text='''Client name (optional)''')
        self.TLabel1_11.configure(width=190)

        self.TLabel1_12 = ttk.Label(self.Frame3_11)
        self.TLabel1_12.place(relx=0.02, rely=0.06, height=29, width=180)
        self.TLabel1_12.configure(background="#d9d9d9")
        self.TLabel1_12.configure(foreground="#000000")
        self.TLabel1_12.configure(font="TkDefaultFont")
        self.TLabel1_12.configure(relief='flat')
        self.TLabel1_12.configure(text='''Standard subscription''')
        self.TLabel1_12.configure(width=180)

        self.TLabel1_13 = ttk.Label(self.Frame3_11)
        self.TLabel1_13.place(relx=0.505, rely=0.06, height=29, width=210)
        self.TLabel1_13.configure(background="#d9d9d9")
        self.TLabel1_13.configure(foreground="#000000")
        self.TLabel1_13.configure(font="TkDefaultFont")
        self.TLabel1_13.configure(relief='flat')
        self.TLabel1_13.configure(text='''On-demand subscription''')
        self.TLabel1_13.configure(width=210)


        self.TEntry1_12 = ttk.Entry(self.Frame3_11)
        self.TEntry1_12.place(relx=0.02, rely=0.71, relheight=0.2
                , relwidth=0.94)
        self.TEntry1_12.configure(takefocus="")
        self.TEntry1_12.configure(cursor="ibeam")

        self.Button1 = Tkinter.Button(self.Frame3)
        self.Button1.place(relx=0.093, rely=0.857, height=42, width=158)
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Submit''')
        self.Button1.configure(command= lambda: conf(self,ipDict,intDict,policerDict))

        self.Button1_13 = Tkinter.Button(self.Frame3)
        self.Button1_13.place(relx=0.579, rely=0.857, height=42, width=158)
        self.Button1_13.configure(pady="0")
        self.Button1_13.configure(text='''Clear''')
        self.Button1_13.configure(command= lambda: self.clear())

    def clear(self,confirmed=False):
       if not confirmed:
           d = Dialog(self,prompt="Are you sure? \n",icon = warning_icon)
       if confirmed or d.ans == 'ok':
           comboboxes = [self.TCombobox1_4,self.TCombobox1_5,self.TCombobox1_6,
                         self.TCombobox1_7,self.TCombobox1_8,self.TCombobox1_9,
                         self.TCombobox1_10,self.TCombobox1_11]
           for cbox in comboboxes: cbox.set('')
           self.TEntry1_12.delete(0,END)
       else: return


class  conf():
    def __init__(self,parent,ipDict,intDict,policerDict,choice=None):

            confDict = {}
            self.error = error_icon
            self.warning = warning_icon

            ls = parent.TCombobox1_4.get()
            if ls == 'None': ls=False

            pe = parent.TCombobox1_5.get()
            if not pe in ipDict.keys():
                Dialog(parent,prompt="Edge router unknown\n",icon = self.error)
                return

            iface = parent.TCombobox1_6.get()
            if not iface in intDict[pe] or iface=='Null':
                Dialog(parent,prompt="Interface unknown\n",icon = self.error)
                return

            vlan = parent.TCombobox1_7.get()
            try:
                if int(vlan) not in range(0,4095):
                    Dialog(parent,prompt="VLAN not in correct range\n",icon = self.error)
                    return
            except ValueError:
                Dialog(parent,prompt="VLAN not in correct range\n",icon = self.error)
                return

            cir = parent.TCombobox1_10.get()
            if not cir in policerDict[pe]:
                Dialog(parent,prompt="Standard subscription is not defined\n",icon = self.error)
                return

            pir = parent.TCombobox1_11.get()
            if not pir in policerDict[pe]:
                Dialog(parent,prompt="onDemand subscription is not defined\n",icon = self.error)
                return

            st = parent.TCombobox1_8.get()
            try: int(st)
            except ValueError:
                if parent.choice: pass
                else:
                    Dialog(parent,prompt="Service ticket must be in numbers\n",icon = self.error)
                    return

            rev = parent.TCombobox1_9.get()
            try:
                datetime.datetime.strptime(rev, '%B %d %Y')
                date = True
            except ValueError:
                date=False
                if re.findall(r'^[0-9]+.?(min|day|days|month|months)$',rev):
                    rev = 'now+'+rev
                else:
                    Dialog(parent,prompt="Revert date has wrong format\n",icon = self.error)
                    return

            ds = parent.TEntry1_12.get()


            if parent.choice:
               ticket = st
               jobid = parent.bigdict[ticket][4]
               serv = Server(parent.serverlogin,parent.server,parent.scriptPath,ticket+'.sh')
               if serv.up:
                   success = check_icon
                   serv.deleteFromRemoteFile(ticket,jobid)
                   time.sleep(1)
                   Dialog(parent,prompt='Ticket '+ticket+' deleted successfully \n',icon=success)
               # convert the ST back to an integer without 'ST' and 'byuser'
               st = str(int(re.findall(r'\d+',ticket.split('by')[0])[0]))

            ''' call the loading class '''
            parent.loading = loading(parent.Frame3,parent,pbar=[0.093,0.857,0.08,0.300],words='Loading')
            parent.update_idletasks()

            d = createConfig()

            ''' create a job to revert on server '''

            commandList = []
            if ipDict[pe][0] == 'juniper' :
                 commandList = d.junos(pe,ls,iface,vlan,cir)
            elif ipDict[pe][0] == 'juniper' :
                 commandList = d.cisco(pe,ls,iface,vlan,cir)

            data = [pe,ls,iface,vlan,cir,st,rev]
            serverlogin = parent.serverlogin
            server = parent.server
            FQP = parent.scriptPath

            done = False
            if commandList:
                done = boDbutton(parent,serverlogin,server,FQP,data,commandList)

            ''' configure the on demand bandwidth on router '''

            commandList = []
            if ipDict[pe][0] == 'juniper' :
                 commandList = d.junos(pe,ls,iface,vlan,pir)
            elif ipDict[pe][0] == 'juniper' :
                 commandList = d.cisco(pe,ls,iface,vlan,pir)

            confDict[pe] = [ipDict[pe][0],ipDict[pe][1],commandList]
            self.c = ClassSendCommand()
            error = False
            if done:
                error = self.c.execute(parent,confDict,parent.username, parent.password,extra=done)

            parent.config(cursor='')
            parent.update()
            parent.loading.stop(parent)
            if done and error:
                Dialog(parent,prompt='There was an error in configuration of '+pe+
                       ' \nHowever a revert task has been added on server '+server+
                       ' \nPlease configure the device manually revert will be automated\n',
                             icon = self.warning)
            parent.clear(confirmed=True)


class createConfig():

    def junos(self,pe,ls,iface,vlan,bw,ds=None,inet6=None):
        commandList = []
        if ls: commandList.append('show configuration logical-systems '+ls+' interface '+iface+'.'+vlan)
        else: commandList.append('show configuration interface '+iface+'.'+vlan)
        commandList.append('configure private')
        if ls: commandList.append('edit logical-systems '+ls)
        commandList.append('edit interface '+iface+'.'+vlan)

        if bw != 'Unlimited':
            commandList.append('set family inet policer input '+bw)
            commandList.append('set family inet policer output '+bw)

        if inet6:
            if bw:
                commandList.append('set family inet6 policer input '+bw)
                commandList.append('set family inet6 policer output '+bw)

        commandList.append('top')
        commandList.append('show | compare')
        commandList.append('commit and-quit')
        if ls: commandList.append('show configuration logical-systems '+ls+' interface '+iface+'.'+vlan)
        else: commandList.append('show configuration interface '+iface+'.'+vlan)

        return commandList


    def cisco(self,pe,ls,iface,vlan,bw,ds=None,inet6=None):
        commandList = []
        ls = False
        if int(vlan) !=0:
            commandList.append('show running-config interface '+iface+'.'+vlan)
        else: commandList.append('show running-config interface '+iface)
        commandList.append('configure terminal')
        if int(vlan) !=0:
            commandList.append('interface '+iface+'.'+vlan)
        else: commandList.append('interface '+iface)

        if bw != 'Unlimited':
            commandList.append('service-policy input '+bw)
            commandList.append('service-policy output '+bw)

        commandList.append('end')
        commandList.append('write memory')
        if int(vlan) !=0:
            commandList.append('show running-config interface '+iface+'.'+vlan)
        else: commandList.append('show running-config interface '+iface)

        return commandList



def test():
    username = 'fisi'
    password = 'fisi123'
    from initial import getIpFromFile, showInterfaces,showPolicer
    ipDict = getIpFromFile(path="c:\users\u\desktop\pacom\\")
    intDict = showInterfaces(username,password,ipDict)
    policerDict = showPolicer(username,password,ipDict)
    serverdata = ['basondole','192.168.56.2','/home/basondole/bOB']
    d=BandwidthOnDemand(username,password,ipDict,intDict,policerDict,serverdata)
    d.mainloop()

if __name__ == '__main__':
    test()
