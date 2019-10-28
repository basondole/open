# This module is part of the core Basondole Tools
# This code provides a settings window to control various settings of Basondole Tools
# Creates a hidden settings file in the current directory
# AUTHOR: Paul S.I. Basondole

import Tkinter
import ttk

import os
import re

import subprocess

from ClassDialog import Dialog


# variables for GUI icons
program_icon ='C:\Users\u\Desktop\PACOM\icon\paul-icon1.ico'
warning_icon = "C:\Users\u\Desktop\PACOM\icon\warning-icon.png"


class Settings(Tkinter.Tk):

    def __init__(self,parent,paths=None):

        Tkinter.Tk.__init__(self)


        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font10 = "-family {Segoe UI} -size 8 -weight normal -slant "  \
            "italic -underline 0 -overstrike 0"
        font9 = "-family Calibri -size 15 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        self.style = ttk.Style()

        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        self.iconbitmap(self,default=program_icon)
        self.geometry("600x450+852+157")
        self.title('Settings')
        self.configure(background="#d9d9d9")
        self.configure(highlightbackground="#d9d9d9")
        self.configure(highlightcolor="black")
        self.resizable(width=False, height=False)

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])

        self.TNotebook1 = ttk.Notebook(self)
        self.TNotebook1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.TNotebook1.configure(width=300)
        self.TNotebook1.configure(takefocus="")

        self.TNotebook1_t0 = Tkinter.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t0, padding=3)
        self.TNotebook1.tab(0, text="General",compound="none",underline="-1",)
        self.TNotebook1_t0.configure(background="#d9d9d9")
        self.TNotebook1_t0.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t0.configure(highlightcolor="black")

        self.TNotebook1_t1 = Tkinter.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t1, padding=3)
        self.TNotebook1.tab(1, text="Burst packages", compound="none"
                ,underline="-1", )
        self.TNotebook1_t1.configure(background="#d9d9d9")
        self.TNotebook1_t1.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t1.configure(highlightcolor="black")

        self.TNotebook1_t2 = Tkinter.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t2, padding=3)
        self.TNotebook1.tab(2, text="Bandwidth on Demand", compound="none"
                ,underline="-1", )
        self.TNotebook1_t2.configure(background="#d9d9d9")
        self.TNotebook1_t2.configure(highlightbackground="#d9d9d9")
        self.TNotebook1_t2.configure(highlightcolor="black")

        self.TLabel2 = ttk.Label(self.TNotebook1_t0)
        self.TLabel2.place(relx=0.017, rely=0.024, height=41, width=205)
        self.TLabel2.configure(background="#d9d9d9")
        self.TLabel2.configure(foreground="#000000")
        self.TLabel2.configure(font=font9)
        self.TLabel2.configure(relief='flat')
        self.TLabel2.configure(takefocus="0")
        self.TLabel2.configure(text='''General settings''')

        self.TFrame1 = ttk.Frame(self.TNotebook1_t0)
        self.TFrame1.place(relx=0.034, rely=0.169, relheight=0.592
                , relwidth=0.361)
        self.TFrame1.configure(relief='groove')
        self.TFrame1.configure(borderwidth="2")
        self.TFrame1.configure(relief='groove')
        self.TFrame1.configure(width=215)
        self.TFrame1.configure(takefocus="0")

        self.TLabel1 = ttk.Label(self.TFrame1)
        self.TLabel1.place(relx=0.043, rely=0.041, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Authentication server''')

        self.TLabel1 = ttk.Label(self.TFrame1)
        self.TLabel1.place(relx=0.043, rely=0.204, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Path to device database''')

        self.TFrame1 = ttk.Frame(self.TNotebook1_t0)
        self.TFrame1.place(relx=0.403, rely=0.169, relheight=0.592
                , relwidth=0.579)
        self.TFrame1.configure(relief='groove')
        self.TFrame1.configure(borderwidth="2")
        self.TFrame1.configure(width=345)
        self.TFrame1.configure(takefocus="0")

        self.TEntry1 = ttk.Entry(self.TFrame1)
        self.TEntry1.place(relx=0.029, rely=0.204, relheight=0.127
                , relwidth=0.945)
        self.TEntry1.configure(foreground="#bcbcbc")
        self.TEntry1.configure(background="#c4c4c4")
        self.TEntry1.configure(takefocus="")
        self.TEntry1.configure(cursor="ibeam")
        if paths: self.TEntry1.insert(0,paths[1])

        self.TLabel1 = ttk.Label(self.TFrame1)
        self.TLabel1.place(relx=0.0, rely=0.367, height=29, width=340)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font=font10)
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''   eg: C:\users\paul\documents\\''')

        self.TEntry2 = ttk.Entry(self.TFrame1)
        self.TEntry2.place(relx=0.029, rely=0.041, relheight=0.127
                , relwidth=0.945)
        self.TEntry2.configure(foreground="#bcbcbc")
        self.TEntry2.configure(background="#c4c4c4")
        self.TEntry2.configure(takefocus="")
        self.TEntry2.configure(cursor="ibeam")
        if paths: self.TEntry2.insert(0,paths[0])

        self.TButton1 = ttk.Button(self.TNotebook1_t0)
        self.TButton1.place(relx=0.034, rely=0.773, height=35, width=100)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''Save''')
        self.TButton1.configure(command= lambda: self.save('general'))


        self.TLabel2 = ttk.Label(self.TNotebook1_t1)
        self.TLabel2.place(relx=0.017, rely=0.024, height=41, width=205)
        self.TLabel2.configure(background="#d9d9d9")
        self.TLabel2.configure(foreground="#000000")
        self.TLabel2.configure(font=font9)
        self.TLabel2.configure(relief='flat')
        self.TLabel2.configure(takefocus="0")
        self.TLabel2.configure(text='''Server settings''')

        self.TFrame2 = ttk.Frame(self.TNotebook1_t1)
        self.TFrame2.place(relx=0.017, rely=0.169, relheight=0.64
                , relwidth=0.394)
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(borderwidth="2")
        self.TFrame2.configure(width=235)
        self.TFrame2.configure(takefocus="0")

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.038, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Server address''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.284, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Server login name''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.540, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Path of client database''')

        self.TFrame2 = ttk.Frame(self.TNotebook1_t1)
        self.TFrame2.place(relx=0.419, rely=0.169, relheight=0.64
                , relwidth=0.562)
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(borderwidth="2")
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(width=335)
        self.TFrame2.configure(takefocus="0")

        self.TEntry3 = ttk.Entry(self.TFrame2)
        self.TEntry3.place(relx=0.03, rely=0.036, relheight=0.117
                , relwidth=0.943)
        self.TEntry3.configure(foreground="#bcbcbc")
        self.TEntry3.configure(background="#c4c4c4")
        self.TEntry3.configure(takefocus="")
        self.TEntry3.configure(cursor="ibeam")
        if paths:
            try: self.TEntry3.insert(0,paths[2])
            except IndexError: pass

        self.TEntry4 = ttk.Entry(self.TFrame2)
        self.TEntry4.place(relx=0.03, rely=0.284, relheight=0.117
                , relwidth=0.943)
        self.TEntry4.configure(foreground="#bcbcbc")
        self.TEntry4.configure(background="#c4c4c4")
        self.TEntry4.configure(takefocus="")
        self.TEntry4.configure(cursor="ibeam")
        if paths:
            try: self.TEntry4.insert(0,paths[3])
            except IndexError: pass

        self.TEntry5 = ttk.Entry(self.TFrame2)
        self.TEntry5.place(relx=0.03, rely=0.540, relheight=0.117
                , relwidth=0.943)
        self.TEntry5.configure(foreground="#bcbcbc")
        self.TEntry5.configure(background="#c4c4c4")
        self.TEntry5.configure(takefocus="")
        self.TEntry5.configure(cursor="ibeam")
        if paths:
            try: self.TEntry5.insert(0,paths[4])
            except IndexError: pass

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.0, rely=0.165, height=27, width=340)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font=font10)
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''   eg: 192.168.0.1''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.0, rely=0.412, height=29, width=340)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font=font10)
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''   eg: root''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.0, rely=0.690, height=29, width=340)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font=font10)
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''   eg: /home/basondole/burst/clients.bas''')

        self.TButton2 = ttk.Button(self.TNotebook1_t1)
        self.TButton2.place(relx=0.017, rely=0.821, height=35, width=110)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Save''')
        self.TButton2.configure(command= lambda: self.save('burst'))



        self.TLabel2 = ttk.Label(self.TNotebook1_t2)
        self.TLabel2.place(relx=0.017, rely=0.024, height=41, width=205)
        self.TLabel2.configure(background="#d9d9d9")
        self.TLabel2.configure(foreground="#000000")
        self.TLabel2.configure(font=font9)
        self.TLabel2.configure(relief='flat')
        self.TLabel2.configure(takefocus="0")
        self.TLabel2.configure(text='''Server settings''')

        self.TFrame2 = ttk.Frame(self.TNotebook1_t2)
        self.TFrame2.place(relx=0.017, rely=0.169, relheight=0.616
                , relwidth=0.394)
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(borderwidth="2")
        self.TFrame2.configure(width=235)
        self.TFrame2.configure(takefocus="0")

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.039, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Server address''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.196, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Server login name''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.353, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Path to working directory''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.51, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Pending tickets directory''')

        self.TLabel1 = ttk.Label(self.TFrame2)
        self.TLabel1.place(relx=0.043, rely=0.667, height=29, width=220)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(takefocus="0")
        self.TLabel1.configure(text='''Logs directory''')

        self.TFrame2 = ttk.Frame(self.TNotebook1_t2)
        self.TFrame2.place(relx=0.419, rely=0.169, relheight=0.616
                , relwidth=0.562)
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(borderwidth="2")
        self.TFrame2.configure(relief='groove')
        self.TFrame2.configure(width=335)
        self.TFrame2.configure(takefocus="0")

        self.TEntry6 = ttk.Entry(self.TFrame2)
        self.TEntry6.place(relx=0.03, rely=0.039, relheight=0.122
                , relwidth=0.943)
        self.TEntry6.configure(foreground="#bcbcbc")
        self.TEntry6.configure(background="#c4c4c4")
        self.TEntry6.configure(takefocus="")
        self.TEntry6.configure(cursor="ibeam")
        if paths:
            try: self.TEntry6.insert(0,paths[5])
            except IndexError: pass

        self.TEntry7 = ttk.Entry(self.TFrame2)
        self.TEntry7.place(relx=0.03, rely=0.196, relheight=0.122
                , relwidth=0.943)
        self.TEntry7.configure(foreground="#bcbcbc")
        self.TEntry7.configure(background="#c4c4c4")
        self.TEntry7.configure(takefocus="")
        self.TEntry7.configure(cursor="ibeam")
        if paths:
            try: self.TEntry7.insert(0,paths[6])
            except IndexError: pass

        self.TEntry8 = ttk.Entry(self.TFrame2)
        self.TEntry8.place(relx=0.03, rely=0.353, relheight=0.122
                , relwidth=0.943)
        self.TEntry8.configure(foreground="#bcbcbc")
        self.TEntry8.configure(background="#c4c4c4")
        self.TEntry8.configure(takefocus="")
        self.TEntry8.configure(cursor="ibeam")
        if paths:
            try: self.TEntry8.insert(0,paths[7])
            except IndexError: pass

        self.TEntry9 = ttk.Entry(self.TFrame2)
        self.TEntry9.place(relx=0.03, rely=0.51, relheight=0.122, relwidth=0.943)
        self.TEntry9.configure(foreground="#bcbcbc")
        self.TEntry9.configure(background="#c4c4c4")
        self.TEntry9.configure(takefocus="")
        self.TEntry9.configure(cursor="ibeam")
        self.TEntry9.insert(0,self.TEntry8.get()+'/PendingTickets/')

        self.TEntry10 = ttk.Entry(self.TFrame2)
        self.TEntry10.place(relx=0.03, rely=0.667, relheight=0.122
                , relwidth=0.943)
        self.TEntry10.configure(foreground="#bcbcbc")
        self.TEntry10.configure(background="#c4c4c4")
        self.TEntry10.configure(takefocus="")
        self.TEntry10.configure(cursor="ibeam")
        self.TEntry10.insert(0,self.TEntry8.get()+'/Logs/')

        self.TButton3 = ttk.Button(self.TNotebook1_t2)
        self.TButton3.place(relx=0.017, rely=0.797, height=35, width=110)
        self.TButton3.configure(takefocus="")
        self.TButton3.configure(text='''Save''')
        self.TButton3.configure(command= lambda: self.save('ondem'))



    def save(self,settings):

        settingsdict = {}
        try:
            settingsfile = open('settings')
            for line in settingsfile:
                if re.findall(r'^(general|burst|ondem)',line):
                    key = line.strip()
                    settingsdict[key]=[]
                else: settingsdict[key].append(line.strip())
            settingsfile.close()
        except IOError: pass

        if settings == 'general':
            devdata = self.TEntry1.get()
            auth_se = self.TEntry2.get()
            if not devdata or not auth_se:
                Dialog(self,prompt= 'Please fill all the field \n')
                return
            try: settingsdict.pop('general')
            except KeyError: pass
            settingsdict['general'] = ['devdata = '+devdata,
                                     'auth-se = '+auth_se]

        elif settings == 'burst':
            bp_serv = self.TEntry3.get()
            bp_user = self.TEntry4.get()
            bp_data = self.TEntry5.get()
            if not bp_serv or not bp_user or not bp_data:
                Dialog(self,prompt= 'Please fill all the field \n')
                return
            try: settingsdict.pop('burst')
            except KeyError: pass
            settingsdict['burst'] = ['bp-serv = '+bp_serv,
                                     'bp-user = '+bp_user,
                                     'bp-data = '+bp_data]

        elif settings == 'ondem':
            bd_serv = self.TEntry6.get()
            bd_user = self.TEntry7.get()
            bd__pwd = self.TEntry8.get()
            if not bd_serv or not bd_user or not bd__pwd:
                Dialog(self,prompt= 'Please fill all the field \n')
                return
            try: settingsdict.pop('ondem')
            except KeyError: pass
            settingsdict['ondem'] = ['bd-serv = '+bd_serv,
                                     'bd-user = '+bd_user,
                                     'bd--pwd = '+bd__pwd]

        subprocess.check_call(["attrib","-H","settings"])
        settingsfile = open('settings','w')
        for key in settingsdict.keys():
            settingsfile.write(key+'\n')
            for item in settingsdict[key]: settingsfile.write(' '+item+'\n')
        settingsfile.close()
        subprocess.check_call(["attrib","+H","settings"])
        self.destroy()
        return


def readsettings(parent):
    warning = warning_icon
    try:
        settingsfile = open('settings', 'r')
        settingsfile = ' '.join((''.join(settingsfile)).split('\n'))
        line = settingsfile
        if re.findall(r'auth-se.?=.?(\S+)',line): authserver = re.findall(r'auth-se.?=.?(\S+)',line)[0]
        else:
            d = Settings(None)
            Dialog(d,resizable=False,nobutton=True,icon=warning,
                   prompt='Authentication server not found \nPlease go to general settings tab \nand specify the authentication server \n')
            d.mainloop()
            return
        if re.findall(r'devdata.?=.?(\S+)',line): devicedbpath = re.findall(r'devdata.?=.?(\S+)',line)[0]
        else:
            d = Settings(None,paths=[authserver])
            Dialog(d,resizable=False,nobutton=True,icon=warning,
                   prompt='Devices database not found \nPlease go to general settings tab \nand specify the database full location \n')
            d.mainloop()
            return
        if re.findall(r'bp-serv.?=.?(\S+)',line): burstserver = re.findall(r'bp-serv.?=.?(\S+)',line)[0]
        else: burstserver = ''

        if re.findall(r'bp-user.?=.?(\S+)',line): burstuser = re.findall(r'bp-user.?=.?(\S+)',line)[0]
        else: burstuser = ''

        if re.findall(r'bp-data.?=.?(\S+)',line): burstdb = re.findall(r'bp-data.?=.?(\S+)',line)[0]
        else: burstdb = ''

        if re.findall(r'bd-serv.?=.?(\S+)',line): ondemserver = re.findall(r'bd-serv.?=.?(\S+)',line)[0]
        else: ondemserver = ''

        if re.findall(r'bd-user.?=.?(\S+)',line): ondemuser = re.findall(r'bd-user.?=.?(\S+)',line)[0]
        else: ondemuser = ''

        if re.findall(r'bd--pwd.?=.?(\S+)',line): ondempwd = re.findall(r'bd--pwd.?=.?(\S+)',line)[0]
        else: ondempwd = ''


        paths = [authserver,devicedbpath,burstserver,burstuser,burstdb,ondemserver,ondemuser,ondempwd]

        return paths

    except IOError:
        d=Settings(None)
        Dialog(d,resizable=False,nobutton=True, icon=warning,
               prompt='System settings are missing.  \nGeneral settings are required for system to work  \nPlease setup the system and restart the application  \n')
        d.mainloop()
        return False



def test():
    paths = readsettings(None)
    if paths:
        d = Settings(None,paths=paths)
        d.mainloop()

if __name__ == '__main__':
    test()
