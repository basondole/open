# This is the core GUI code for Basondole Tools
# This code levarages the other modules with little to do by its own
# AUTHOR: Paul S.I. Basondole

from __future__ import print_function
import Tkinter
from Tkinter import *
import ttk
import tkMessageBox
import tkFileDialog
from ScrolledText import ScrolledText
from PIL import Image, ImageTk

import re
import Queue
import threading
import time
import paramiko
import socket

import datetime

from vFinderUnNC import buttonvfinderun
from vFinderDeuxNC import buttonvfinderdx
from dCheckNC import buttondcheck
from vCheckNC import buttonvcheck
from ipCheckNC import buttonicheck
from bEditorNC import action
from bOnDemandNC import Server


from initial import verifyUser
from initial import showInterfaces
from initial import showPolicer
from initial import getIpFromFile

from ClassCommand import Commandwindow
from ClassLoading import loading
from ClassDialog import Dialog
from ClassDevice import Devices
from ClassOutput import outputWin
from ClassServiceProvision import ServiceProvision
from ClassBurstPackages import BurstPackages
from ClassBandwidthOnDemand import BandwidthOnDemand
from ClassSettings import Settings
from ClassSettings import readsettings

from manpage import manpage


# variable for GUI icons
program_icon = 'C:\Users\u\Desktop\PACOM\icon\paul-icon1.ico'
info_icon2 ='C:\Users\u\Desktop\PACOM\icon\info-icon2.png'
home_icon2 ='C:\Users\u\Desktop\PACOM\icon\home-icon2.gif'
devices_icon = 'C:\Users\u\Desktop\PACOM\icon\devices-icon.gif'
terminal_icon = 'C:\Users\u\Desktop\PACOM\icon\\terminal-icon.gif'
settings_icon ='C:\Users\u\Desktop\PACOM\icon\settings-icon.gif'
about_icon ='C:\Users\u\Desktop\PACOM\icon\\about-icon.gif'
quit_icon ='C:\Users\u\Desktop\PACOM\icon\quit-icon.gif'
ip_icon2 ='C:\Users\u\Desktop\PACOM\icon\ip-icon2.gif'
ip_icon3 ='C:\Users\u\Desktop\PACOM\icon\ip-icon3.gif'
traffic_icon= 'C:\Users\u\Desktop\PACOM\icon\\traffic-icon.gif'
find_icon = 'C:\Users\u\Desktop\PACOM\icon\\find-icon.gif'
bulb_icon = 'C:\Users\u\Desktop\PACOM\icon\\bulb-icon.gif'
package_icon2 ='C:\Users\u\Desktop\PACOM\icon\package-icon2.gif'
back_icon2='C:\Users\u\Desktop\PACOM\icon\\back-icon2.gif'
package_icon1 ='C:\Users\u\Desktop\PACOM\icon\package-icon1.gif'
search_icon ='C:\Users\u\Desktop\PACOM\icon\search-icon.gif'
back_icon ='C:\Users\u\Desktop\PACOM\icon\\back-icon.gif'
add_icon ='C:\Users\u\Desktop\PACOM\icon\\add-icon.gif'
delete_icon ='C:\Users\u\Desktop\PACOM\icon\delete-icon.gif'
add_symbol='C:\Users\u\Desktop\PACOM\icon\\add-symbol.gif'
cross_icon2="C:\Users\u\Desktop\PACOM\icon\cross-icon2.gif"
checkmark_icon ='C:\Users\u\Desktop\PACOM\icon\\checkmark-icon.gif'
cancel_icon = 'C:\Users\u\Desktop\PACOM\icon\cancel-icon.png'
ask_icon='C:\Users\u\Desktop\PACOM\icon\\ask-icon.png'
check_icon = "C:\Users\u\Desktop\PACOM\icon\check-icon.png"





class basoNx(Tkinter.Tk):

    def __init__(self, *args, **kwargs):


        self.paths = paths

        Tkinter.Tk.__init__(self, *args, **kwargs)
        Tkinter.Tk.iconbitmap(self,default=program_icon)
        Tkinter.Tk.title(self,'Basondole Tools')

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        style = ttk.Style()
        style.configure('.',background=_bgcolor)
        style.configure('.',foreground=_fgcolor)
        style.configure('.',font="TkDefaultFont")
        style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])


        Tkinter.Tk.geometry(self, "650x450+650+150")
        Tkinter.Tk.configure(self, background="#d9d9d9")
        Tkinter.Tk.resizable(self, width=False, height=False)

        menubar = Tkinter.Menu(self,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        Tkinter.Tk.configure(self, menu = menubar)

        menubar.add_command(
                            activebackground="#ececec",
                            activeforeground="#000000",
                            background="#d9d9d9",
                            compound="left",
                            font="TkMenuFont",
                            foreground="#000000",
                            label="Home",
                            command= lambda: self.show_frame(StartPage))


        menubar.add_command(
                            activebackground="#ececec",
                            activeforeground="#000000",
                            background="#d9d9d9",
                            compound="left",
                            font="TkMenuFont",
                            foreground="#000000",
                            label="Settings",
                            command= lambda: Settings(self,self.paths))

        def manual():
           output= outputWin()
           output.TB2('Manual',manpage(),frontend,self)

        dropmenu1_1 = Tkinter.Menu(self,tearoff=0)
        menubar.add_cascade(menu=dropmenu1_1,
                 activebackground="#ececec",
                 activeforeground="#000000",
                 background="#d9d9d9",
                 compound="left",
                 font="TkMenuFont",
                 foreground="#000000",
                 label="Help")
        dropmenu1_1.add_command(
                 activebackground="#ececec",
                 activeforeground="#000000",
                 background="#d9d9d9",
                 compound="left",
                 font="TkMenuFont",
                 foreground="#000000",
                 label="Licence",
                 command=lambda: Dialog(self,title='About',prompt='Licence valid until  \nMay 27 2019  \n',
                                        nobutton=True,icon=info_icon2))
        dropmenu1_1.add_command(
                 activebackground="#ececec",
                 activeforeground="#000000",
                 background="#d9d9d9",
                 compound="left",
                 font="TkMenuFont",
                 foreground="#000000",
                 label="Manual",
                 command=lambda: manual())


        dropmenu1_1.add_command(
                 activebackground="#ececec",
                 activeforeground="#000000",
                 background="#d9d9d9",
                 compound="left",
                 font="TkMenuFont",
                 foreground="#000000",
                 label="About",
                 command=lambda: Dialog(self,title='About',prompt='Basondole Tools  \n A network automation and administration tool  \ndesigned for service provider environments  \nDeveloped by  Paul S.I.Basondole  \n℗2019  \n',
                   nobutton=True,icon=info_icon2))


        dropmenu1_2 = Tkinter.Menu(self,tearoff=0)
        menubar.add_cascade(menu=dropmenu1_2,
                 activebackground="#ececec",
                 activeforeground="#000000",
                 background="#d9d9d9",
                 compound="left",
                 font="TkMenuFont",
                 foreground="#000000",
                 label="Devices")

        keylist = ipDict.keys()
        keylist.sort()
        for ip in keylist:
            dropmenu1_2.add_command(
                     activebackground="#ececec",
                     activeforeground="#000000",
                     background="#d9d9d9",
                     compound="left",
                     font="TkMenuFont",
                     foreground="#000000",
                     label=ip.ljust(15)+" "+ipDict[ip][0])


        menubar.add_command(
                            activebackground="#ececec",
                            activeforeground="#000000",
                            background="#d9d9d9",
                            compound="left",
                            font="TkMenuFont",
                            foreground="#000000",
                            label="Quit",
                            command= self.destroy)



        status  = Label(self, bd=1, relief=SUNKEN, anchor = W)
        status['text'] = 'Logged in as '+username.capitalize()
        status.pack(side=BOTTOM, fill=X)


        container = Tkinter.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        ''' Menu Bar Icons '''

        self.Button0_1Imgvar = PhotoImage(file=home_icon2)
        self.Button0_1 = ttk.Button(self, image=self.Button0_1Imgvar)
        self.Button0_1.place(relx=0.0, rely=0.0, height=40, width=102,bordermode='ignore')
        self.Button0_1.configure(command=lambda: self.show_frame(StartPage))
        self.Button0_1.configure(takefocus=False)
        self.Button0_1.configure(text='''Home''',compound='left')


        self.Button0_4Imgvar = PhotoImage(file=devices_icon)
        self.Button0_4 = ttk.Button(self, image=self.Button0_4Imgvar)
        self.Button0_4.place(relx=0.162, rely=0.0, height=40, width=111)
        self.Button0_4.configure(command=lambda: Devices(self,ipDict,path=paths[1]))
        self.Button0_4.configure(takefocus=False)
        self.Button0_4.configure(text='''Devices''',compound='left')


        self.Button0_5Imgvar = PhotoImage(file=terminal_icon)
        self.Button0_5 = ttk.Button(self, image=self.Button0_5Imgvar)
        self.Button0_5.place(relx=0.337, rely=0.0, height=40, width=128)
        self.Button0_5.configure(command=lambda: Commandwindow(self,ipDict,username,password))
        self.Button0_5.configure(takefocus=False)
        self.Button0_5.configure(text='''Command''',compound='left')


        self.Button0_3Imgvar = PhotoImage(file=settings_icon)
        self.Button0_3 = ttk.Button(self, image=self.Button0_3Imgvar)
        self.Button0_3.place(relx=0.542, rely=0.0, height=40, width=110)
        self.Button0_3.configure(command=lambda: Settings(self,self.paths))
        self.Button0_3.configure(takefocus=False)
        self.Button0_3.configure(text='''Settings''',compound='left')


        self.Button0_6Imgvar = PhotoImage(file=about_icon)
        self.Button0_6 = ttk.Button(self, image=self.Button0_6Imgvar)
        self.Button0_6.place(relx=0.716, rely=0.0, height=40, width=94)
        self.Button0_6.configure(command=lambda: Dialog(self,title='About',prompt='Basondole Tools  \n A network automation and administration tool  \ndesigned for service provider environments  \nDeveloped by  Paul S.I.Basondole  \n℗2019  \n',
                   nobutton=True,icon=info_icon2))
        self.Button0_6.configure(takefocus=False)
        self.Button0_6.configure(text='''About''',compound='left')

        self.Button0_2Imgvar = PhotoImage(file=quit_icon)
        self.Button0_2 = ttk.Button(self, image=self.Button0_2Imgvar)
        self.Button0_2.place(relx=0.864, rely=0.0, height=40, width=86)
        self.Button0_2.configure(command=lambda: self.destroy())
        self.Button0_2.configure(takefocus=False)
        self.Button0_2.configure(text='''Quit''',compound='left')


        ''' EOF Menu Bar Icons '''

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive,
                  OneVlanFinder,TwoVlanFinder):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(StartPage)


    def show_frame(self, cont):
        if cont == 'home': cont = StartPage
        frame = self.frames[cont]
        frame.tkraise()
        # on these frames put a quit button
        if cont in (StartPage, PageOne, PageTwo, PageThree, PageFour,PageFive):
            self.Button0_2.place(relx=0.864, rely=0.0, height=40, width=86)
        # do not put a quit button
        else:
            self.Button0_2.place_forget()






class StartPage(Tkinter.Frame):

    def __init__(self, parent, controller):

        if datetime.datetime.now() < datetime.datetime.strptime('10-12-2020','%d-%m-%Y'):
            expired = False
        else: expired = True

        Tkinter.Frame.__init__(self,parent)

        Labelframe = Tkinter.LabelFrame(self)
        Labelframe.place(relx=0.0, rely=0.09, relheight=0.996, relwidth=1.0)
        Labelframe.configure(relief='groove')
        Labelframe.configure(foreground="black")
        Labelframe.configure(text='''Home''')
        Labelframe.configure(background="#d9d9d9")
        Labelframe.configure(width=470)

        TLabel = ttk.Label(Labelframe)
        TLabel.place(relx=0.011, rely=0.14, height=29, width=183
                , bordermode='ignore')
        TLabel.configure(background="#d9d9d9")
        TLabel.configure(foreground="#000000")
        TLabel.configure(font="TkDefaultFont")
        TLabel.configure(relief='flat')

        # for positioning elements in window
        dx = 0.15
        dy = -0.1


        TButton = Tkinter.Button(Labelframe)
        TButton.place(relx=0.023+dx, rely=0.326+dy, height=35, width=176
                , bordermode='ignore')
        TButton.configure(takefocus=False)
        self.TbuttonImgvar = PhotoImage(file=ip_icon2)
        TButton.configure(text=''' Vlan operation''',image=self.TbuttonImgvar, compound='left')
        TButton.configure(command=lambda: controller.show_frame(PageOne))
        TButton.configure(width=14)
        if expired: TButton.configure(command=lambda: Dialog(parent,prompt='   Licence expired   \n',nobutton=True,
                                                             icon=info_icon2))

        TButton_1 = Tkinter.Button(Labelframe)
        TButton_1.place(relx=0.369+dx, rely=0.326+dy, height=35, width=176
                , bordermode='ignore')
        TButton_1.configure(takefocus=False)
        self.TbuttonImgvar_1 = PhotoImage(file=traffic_icon)
        TButton_1.configure(text=''' Burst packages''',image=self.TbuttonImgvar_1, compound='left')
        TButton_1.configure(command=lambda: controller.show_frame(PageFour))
        TButton_1.configure(width=14)
        if expired: TButton_1.configure(command=lambda: Dialog(parent,prompt='   Licence expired   \n',nobutton=True,
                                                               icon=info_icon2))


        TButton_2 = Tkinter.Button(Labelframe)
        TButton_2.place(relx=0.023+dx, rely=0.512+dy, height=35, width=176
                , bordermode='ignore')
        TButton_2.configure(takefocus=False)
        self.TbuttonImgvar_2 = PhotoImage(file=ip_icon3)
        TButton_2.configure(text=''' ipv4 operation''',image=self.TbuttonImgvar_2, compound='left')
        TButton_2.configure(command=lambda: controller.show_frame(PageTwo))
        if expired: TButton_2.configure(command=lambda: Dialog(parent,prompt='   Licence expired   \n',nobutton=True,
                                                               icon=info_icon2))

        TButton_3 = Tkinter.Button(Labelframe)
        TButton_3.place(relx=0.369+dx, rely=0.512+dy, height=35, width=176
                , bordermode='ignore')
        TButton_3.configure(takefocus=False)
        self.TbuttonImgvar_3 = PhotoImage(file=find_icon)
        TButton_3.configure(text=''' Locate service''',image=self.TbuttonImgvar_3, compound='left')
        TButton_3.configure(command=lambda: controller.show_frame(PageThree))
        if expired: TButton_3.configure(command=lambda: Dialog(parent,prompt='   Licence expired   \n',nobutton=True,
                                                               icon=info_icon2))


        TButton_4 = Tkinter.Button(Labelframe)
        TButton_4.place(relx=0.023+dx, rely=0.698+dy, height=35, width=176
                , bordermode='ignore')
        TButton_4.configure(takefocus=False)
        self.TbuttonImgvar_4 = PhotoImage(file=bulb_icon)
        TButton_4.configure(text=''' Provision service''',image=self.TbuttonImgvar_4, compound='left')
        TButton_4.configure(command=lambda: ServiceProvision(username,password,ipDict,intDict,policerDict))
        if expired: TButton_4.configure(command=lambda: Dialog(parent,prompt='   Licence expired   \n',nobutton=True,
                                                               icon=info_icon2))


        TButton_5 = Tkinter.Button(Labelframe)
        TButton_5.place(relx=0.369+dx, rely=0.698+dy, height=35, width=176
                , bordermode='ignore')
        TButton_5.configure(takefocus=False)
        self.TbuttonImgvar_5 = PhotoImage(file=package_icon2)
        TButton_5.configure(text=''' B on Demand''',image=self.TbuttonImgvar_5, compound='left')
        TButton_5.configure(command=lambda: controller.show_frame(PageFive))
        if expired: TButton_5.configure(command=lambda: Dialog(parent,prompt='   Licence expired   \n',nobutton=True,
                                                               icon=info_icon2))



class PageOne(Tkinter.Frame):

    def __init__(self, parent, controller):
        Tkinter.Frame.__init__(self, parent)


        Labelframe1 = Tkinter.LabelFrame(self)
        Labelframe1.place(relx=0.0, rely=0.09, relheight=0.996, relwidth=1.0)
        Labelframe1.configure(relief='groove')
        Labelframe1.configure(foreground="black")
        Labelframe1.configure(text='''VLAN operations''')
        Labelframe1.configure(background="#d9d9d9")
        Labelframe1.configure(width=440)

        dx = 0.18

        TButton1 = ttk.Button(Labelframe1)
        TButton1.place(relx=0.022+dx, rely=0.126, height=50, width=160
                , bordermode='ignore')
        TButton1.configure(takefocus=False)
        TButton1.configure(text='''Vlan Finder''')
        TButton1.configure(command=lambda: controller.show_frame(OneVlanFinder))
        TButton1.configure(width=16)

        TButton1_1 = ttk.Button(Labelframe1)
        TButton1_1.place(relx=0.3+dx, rely=0.126, height=50, width=160
                , bordermode='ignore')
        TButton1_1.configure(takefocus=False)
        TButton1_1.configure(text='''Vlan Finder 2''')
        TButton1_1.configure(command=lambda: controller.show_frame(TwoVlanFinder))
        TButton1_1.configure(width=14)

        TButton1_2 = ttk.Button(Labelframe1)
        TButton1_2.place(relx=0.022+dx, rely=0.292, height=50, width=160
                , bordermode='ignore')
        TButton1_2.configure(takefocus=False)
        TButton1_2.configure(text='''Locate vlan''')
        TButton1_2.configure(command=lambda: Check(frontend,self,'VLAN'))
        TButton1_2.configure(width=14)

        TButton1_3 = Tkinter.Button(Labelframe1)
        TButton1_3.place(relx=0.022+dx, rely=0.458, height=38, width=158
                , bordermode='ignore')
        TButton1_3.configure(takefocus=False)
        TButton1_3.configure(background="#bfceff")
        TButton1_3.configure(disabledforeground="#a3a3a3")
        TButton1_3.configure(text=''' Back Home''')
        TButton1_3.configure(command=lambda: controller.show_frame(StartPage))
        TButton1_3.configure(width=14)
        self.TbuttonImgvar1_3 = PhotoImage(file=back_icon2)
        TButton1_3.configure(image=self.TbuttonImgvar1_3, compound='left')



class PageTwo(Tkinter.Frame):

    def __init__(self, parent, controller):
        Tkinter.Frame.__init__(self, parent)


        Labelframe2 = Tkinter.LabelFrame(self)
        Labelframe2.place(relx=0.0, rely=0.09, relheight=0.996, relwidth=1.0)
        Labelframe2.configure(relief='groove')
        Labelframe2.configure(foreground="black")
        Labelframe2.configure(text='''IPv4 operations''')
        Labelframe2.configure(background="#d9d9d9")
        Labelframe2.configure(width=440)


        TButton2 = ttk.Button(Labelframe2)
        TButton2.place(relx=0.022, rely=0.126, height=50, width=160
                , bordermode='ignore')
        TButton2.configure(takefocus=False)
        TButton2.configure(text='''Locate address''')
        TButton2.configure(command=lambda: Check(frontend,self,'IP'))
        TButton2.configure(width=16)

        TButton2_1 = Tkinter.Button(Labelframe2)
        TButton2_1.place(relx=0.022, rely=0.292, height=38, width=158
                , bordermode='ignore')
        TButton2_1.configure(takefocus=False)
        TButton2_1.configure(text='''Back Home''')
        TButton2_1.configure(command=lambda: controller.show_frame(StartPage))
        TButton2_1.configure(width=14)
        TButton2_1.configure(background="#bfceff")
        TButton2_1.configure(disabledforeground="#a3a3a3")
        TButton2_1.configure(text=''' Back Home''')
        self.TbuttonImgvar2_1 = PhotoImage(file=back_icon2)
        TButton2_1.configure(image=self.TbuttonImgvar2_1, compound='left')



class PageThree(Tkinter.Frame):

    def __init__(self, parent, controller):
        Tkinter.Frame.__init__(self, parent)

        Labelframe3 = Tkinter.LabelFrame(self)
        Labelframe3.place(relx=0.0, rely=0.09, relheight=0.996, relwidth=1.0)
        Labelframe3.configure(relief='groove')
        Labelframe3.configure(foreground="black")
        Labelframe3.configure(text='''Locate services''')
        Labelframe3.configure(background="#d9d9d9")
        Labelframe3.configure(width=440)

        # for positioning of GUI elements on a window
        dx = 0.18

        TButton3 = ttk.Button(Labelframe3)
        TButton3.place(relx=0.022+dx, rely=0.126, height=45, width=158
                , bordermode='ignore')
        TButton3.configure(takefocus=False)
        TButton3.configure(text='''Locate VLAN''')
        TButton3.configure(command=lambda: Check(frontend,self,'VLAN'))
        TButton3.configure(width=16)

        TButton3_1 = ttk.Button(Labelframe3)
        TButton3_1.place(relx=0.3+dx, rely=0.126, height=45, width=158
                , bordermode='ignore')
        TButton3_1.configure(takefocus=False)
        TButton3_1.configure(text='''Locate IPv4''')
        TButton3_1.configure(command=lambda: Check(frontend,self,'IP'))
        TButton3_1.configure(width=14)

        TButton3_2 = ttk.Button(Labelframe3)
        TButton3_2.place(relx=0.022+dx, rely=0.292, height=45, width=158
                , bordermode='ignore')
        TButton3_2.configure(takefocus=False)
        TButton3_2.configure(text='''Locate name''')
        TButton3_2.configure(command=lambda: Check(frontend,self,'NAME'))
        TButton3_2.configure(width=14)

        TButton3_3 = Tkinter.Button(Labelframe3)
        TButton3_3.place(relx=0.022+dx, rely=0.458, height=38, width=158
                , bordermode='ignore')
        TButton3_3.configure(takefocus=False)
        TButton3_3.configure(text=''' Back Home''')
        TButton3_3.configure(command=lambda: controller.show_frame(StartPage))
        TButton3_3.configure(width=14)
        TButton3_3.configure(background="#bfceff")
        TButton3_3.configure(disabledforeground="#a3a3a3")
        self.TbuttonImgvar3_3 = PhotoImage(file=back_icon2)
        TButton3_3.configure(image=self.TbuttonImgvar3_3, compound='left')


class PageFour(Tkinter.Frame):

    def __init__(self, parent, controller):
        Tkinter.Frame.__init__(self, parent)

        serverlogin = paths[3]
        server = paths[2]
        FQP = paths[4]
        serverdata = [serverlogin,server,FQP]

        Labelframe4 = Tkinter.LabelFrame(self)
        Labelframe4.place(relx=0.0, rely=0.09, relheight=0.996, relwidth=1.0)
        Labelframe4.configure(relief='groove')
        Labelframe4.configure(foreground="black")
        Labelframe4.configure(text='''Burst packages''')
        Labelframe4.configure(background="#d9d9d9")
        Labelframe4.configure(width=440)

        TLabel4 = Tkinter.Label(Labelframe4)
        TLabel4.place(relx=0.01, rely=0.02, height=29, width=630)
        TLabel4.configure(justify='left',anchor='w')
        TLabel4.configure(text= 'Server address : '+serverlogin+'@'+server)

        TLabel4_1 = Tkinter.Label(Labelframe4)
        TLabel4_1.place(relx=0.01, rely=0.10, height=29, width=630)
        TLabel4_1.configure(justify='left',anchor='w')
        TLabel4_1.configure(text= 'Clients database : '+FQP)

        # for positioning GUI elements on window
        dx = 0.15
        dy = 0.18

        TButton4 = ttk.Button(Labelframe4)
        TButton4.place(relx=0.022+dx, rely=0.126+dy, height=40, width=180
                , bordermode='ignore')
        TButton4.configure(takefocus=False)
        TButton4.configure(text=''' Add a client''')
        TButton4.configure(command=lambda: BurstPackages(username,password,ipDict,intDict,policerDict,serverdata,choice='Add client'))
        TButton4.configure(width=16)
        self.TbuttonImgvar4 = PhotoImage(file=add_icon)
        TButton4.configure(image=self.TbuttonImgvar4, compound='left')

        TButton4_1 = ttk.Button(Labelframe4)
        TButton4_1.place(relx=0.4+dx, rely=0.126+dy, height=40, width=180
                , bordermode='ignore')
        TButton4_1.configure(takefocus=False)
        TButton4_1.configure(text=''' Remove client''')
        TButton4_1.configure(command=lambda: BurstPackages(username,password,ipDict,intDict,policerDict,serverdata,choice='Remove client'))
        TButton4_1.configure(width=14)
        self.TbuttonImgvar4_1 = PhotoImage(file=delete_icon)
        TButton4_1.configure(image=self.TbuttonImgvar4_1, compound='left')


        TButton4_2 = ttk.Button(Labelframe4)
        TButton4_2.place(relx=0.022+dx, rely=0.292+dy, height=40, width=180
                , bordermode='ignore')
        TButton4_2.configure(takefocus=False)
        TButton4_2.configure(text=''' Move client ''')
        TButton4_2.configure(command=lambda: BurstPackages(username,password,ipDict,intDict,policerDict,serverdata,choice='Update client'))
        TButton4_2.configure(width=14)
        self.TbuttonImgvar4_2 = PhotoImage(file=package_icon1)
        TButton4_2.configure(image=self.TbuttonImgvar4_2, compound='left')


        def view():
            self.view = action(server,serverlogin,FQP)
            output= outputWin()
            output.TB2('Burst clients', self.view.view(),frontend,self)

        TButton4_3 = ttk.Button(Labelframe4)
        TButton4_3.place(relx=0.4+dx, rely=0.292+dy, height=40, width=180
                , bordermode='ignore')
        TButton4_3.configure(takefocus=False)
        TButton4_3.configure(text=''' View clients''')
        TButton4_3.configure(command=lambda: view())
        TButton4_3.configure(width=14)
        self.TbuttonImgvar4_3 = PhotoImage(file=search_icon)
        TButton4_3.configure(image=self.TbuttonImgvar4_3, compound='left')

        TButton4_4 = Tkinter.Button(Labelframe4)
        TButton4_4.place(relx=0.022+dx, rely=0.458+dy, height=38, width=180
                , bordermode='ignore')
        TButton4_4.configure(takefocus=False)
        TButton4_4.configure(text=''' Back Home''')
        TButton4_4.configure(command=lambda: controller.show_frame(StartPage))
        TButton4_4.configure(width=14)
        TButton4_4.configure(background="#bfceff")
        TButton4_4.configure(disabledforeground="#a3a3a3")
        self.TbuttonImgvar4_4 = PhotoImage(file=back_icon2)
        TButton4_4.configure(image=self.TbuttonImgvar4_4, compound='left')


        if not serverlogin or not server or not FQP:
            buttons = [TButton4,TButton4_1, TButton4_2,TButton4_3]
            for button in buttons: button.configure(state= 'disabled')


class PageFive(Tkinter.Frame):

    def __init__(self, parent, controller):
        Tkinter.Frame.__init__(self, parent)

        serverlogin = paths[6]
        server = paths[5]
        scriptPath = paths[7]

        serverdata = [serverlogin,server,scriptPath]


        Labelframe5 = Tkinter.LabelFrame(self)
        Labelframe5.place(relx=0.0, rely=0.09, relheight=0.996, relwidth=1.0)
        Labelframe5.configure(relief='groove')
        Labelframe5.configure(foreground="black")
        Labelframe5.configure(text='''Bandwidth on Demand''')
        Labelframe5.configure(background="#d9d9d9")
        Labelframe5.configure(width=440)


        TLabel5 = Tkinter.Label(Labelframe5)
        TLabel5.place(relx=0.01, rely=0.02, height=29, width=400)
        TLabel5.configure(justify='left',anchor='w')
        TLabel5.configure(text= 'Server address : '+serverlogin+'@'+server)

        TLabel5_1 = Tkinter.Label(Labelframe5)
        TLabel5_1.place(relx=0.01, rely=0.10, height=29, width=400)
        TLabel5_1.configure(justify='left',anchor='w')
        TLabel5_1.configure(text= 'Working directory : '+scriptPath)


        dy = 0.2
        dx = 0.12
        TButton5 = ttk.Button(Labelframe5)
        TButton5.place(relx=0.022+dx, rely=0.126+dy, height=40, width=200
                , bordermode='ignore')
        TButton5.configure(takefocus=False)
        TButton5.configure(text=''' Add a ticket''')
        TButton5.configure(command=lambda: BandwidthOnDemand(username,password,ipDict,intDict,policerDict,serverdata))
        TButton5.configure(width=16)
        self.TbuttonImgvar5 = PhotoImage(file=add_icon)
        TButton5.configure(image=self.TbuttonImgvar5, compound='left')

        def view():
            serv = Server(serverlogin,server,scriptPath,'*')
            output= outputWin()
            output.TB2('Pending Tickets', serv.retrieveRemoteFile(),frontend,self)

        TButton5_1 = ttk.Button(Labelframe5)
        TButton5_1.place(relx=0.4+dx, rely=0.126+dy, height=40, width=200
                , bordermode='ignore')
        TButton5_1.configure(takefocus=False)
        TButton5_1.configure(text=''' View tickets''')
        TButton5_1.configure(command=lambda: view())
        TButton5_1.configure(width=14)
        self.TbuttonImgvar5_1 = PhotoImage(file=search_icon)
        TButton5_1.configure(image=self.TbuttonImgvar5_1, compound='left')


        TButton5_2 = ttk.Button(Labelframe5)
        TButton5_2.place(relx=0.022+dx, rely=0.292+dy, height=40, width=200
                , bordermode='ignore')
        TButton5_2.configure(takefocus=False)
        TButton5_2.configure(text=''' Delete ticket''')
        TButton5_2.configure(command=lambda: Check(frontend,self,'Delete ticket'))
        TButton5_2.configure(width=14)
        self.TbuttonImgvar5_2 = PhotoImage(file=delete_icon)
        TButton5_2.configure(image=self.TbuttonImgvar5_2, compound='left')

        TButton5_3 = ttk.Button(Labelframe5)
        TButton5_3.place(relx=0.4+dx, rely=0.292+dy, height=40, width=200
                , bordermode='ignore')
        TButton5_3.configure(takefocus=False)
        TButton5_3.configure(text=''' Update ticket''')
        TButton5_3.configure(command=lambda: BandwidthOnDemand(username,password,ipDict,intDict,policerDict,serverdata,choice=True))
        TButton5_3.configure(width=14)
        self.TbuttonImgvar5_3 = PhotoImage(file=add_symbol)
        TButton5_3.configure(image=self.TbuttonImgvar5_3, compound='left')

        TButton5_4 = Tkinter.Button(Labelframe5)
        TButton5_4.place(relx=0.022+dx, rely=0.458+dy, height=38, width=200
                , bordermode='ignore')
        TButton5_4.configure(takefocus=False)
        TButton5_4.configure(text=''' Back Home''')
        TButton5_4.configure(command=lambda: controller.show_frame(StartPage))
        TButton5_4.configure(width=14)
        TButton5_4.configure(background="#bfceff")
        TButton5_4.configure(disabledforeground="#a3a3a3")
        self.TbuttonImgvar5_4 = PhotoImage(file=back_icon2)
        TButton5_4.configure(image=self.TbuttonImgvar5_4, compound='left')


        if not serverlogin or not server or not scriptPath:
            buttons = [TButton5,TButton5_1, TButton5_2,TButton5_3]
            for button in buttons: button.configure(state= 'disabled')

class LoginPage(Tkinter.Tk):

    def __init__(self, *args, **kwargs):

        Tkinter.Tk.__init__(self, *args, **kwargs)
        Tkinter.Tk.iconbitmap(self,default=program_icon)
        Tkinter.Tk.title(self,'')

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        style = ttk.Style()
        style.configure('.',background=_bgcolor)
        style.configure('.',foreground=_fgcolor)
        style.configure('.',font="TkDefaultFont")
        style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        Tkinter.Tk.geometry(self,"320x210+597+262")
        Tkinter.Tk.resizable(self,width=False, height=False)
        Tkinter.Tk.configure(self, background="#d9d9d9")


        self.LabelFrame = Tkinter.LabelFrame(self)
        self.LabelFrame.place(relx=0.0, rely=0.0, relheight=0.987, relwidth=0.995)
        self.LabelFrame.configure(relief='groove')
        self.LabelFrame.configure(foreground="black")
        self.LabelFrame.configure(text='''Login''')
        self.LabelFrame.configure(background="#d9d9d9")
        self.LabelFrame.configure(highlightbackground="#d9d9d9")
        self.LabelFrame.configure(highlightcolor="black")
        self.LabelFrame.configure(width=300)


        Label = Tkinter.Label(self.LabelFrame)
        Label.place(relx=0.038, rely=0.2, height=31, width=85
                , bordermode='ignore')
        Label.configure(background="#d9d9d9")
        Label.configure(disabledforeground="#a3a3a3")
        Label.configure(foreground="#000000")
        Label.configure(underline="0")
        Label.configure(text='''Username''')
        Label.configure(width=85)

        Label_2 = Tkinter.Label(self.LabelFrame)
        Label_2.place(relx=0.038, rely=0.433, height=31, width=85
                , bordermode='ignore')
        Label_2.configure(activebackground="#f9f9f9")
        Label_2.configure(activeforeground="black")
        Label_2.configure(background="#d9d9d9")
        Label_2.configure(disabledforeground="#a3a3a3")
        Label_2.configure(foreground="#000000")
        Label_2.configure(highlightbackground="#d9d9d9")
        Label_2.configure(highlightcolor="black")
        Label_2.configure(underline="0")
        Label_2.configure(text='''Password''')
        Label_2.configure(width=85)


        usernamebox = Tkinter.Entry(self.LabelFrame)
        usernamebox.place(relx=0.365, rely=0.2, height=26, relwidth=0.515
                , bordermode='ignore')
        usernamebox.configure(background="white")
        usernamebox.configure(disabledforeground="#a3a3a3")
        usernamebox.configure(foreground="#000000")
        usernamebox.configure(highlightbackground="#d9d9d9")
        usernamebox.configure(highlightcolor="black")
        usernamebox.configure(insertbackground="black")
        usernamebox.configure(selectbackground="#c4c4c4")
        usernamebox.configure(selectforeground="black")
        usernamebox.configure(width=134)

        passwordbox = Tkinter.Entry(self.LabelFrame,show='*')
        passwordbox.place(relx=0.365, rely=0.433, height=26, relwidth=0.515
                , bordermode='ignore')
        passwordbox.configure(background="white")
        passwordbox.configure(disabledforeground="#a3a3a3")
        passwordbox.configure(foreground="#000000")
        passwordbox.configure(highlightbackground="#d9d9d9")
        passwordbox.configure(highlightcolor="black")
        passwordbox.configure(insertbackground="black")
        passwordbox.configure(selectbackground="#c4c4c4")
        passwordbox.configure(selectforeground="black")
        passwordbox.configure(width=134)


        self.status  = Tkinter.Label(self, bd=1, relief=SUNKEN, anchor = W)
        self.status['text'] = ''
        self.status.pack(side=BOTTOM, fill=X)
        font14 = "-family {Segoe UI} -size 8 -weight normal -slant "  \
             "italic -underline 0 -overstrike 0"
        self.status.configure(font=font14)


        def getUser(*event):
            global username,password,loginAttempt,intDict,policerDict
            if usernamebox.get()=='':
                self.status.configure(text='Username cannot be blank')
            elif passwordbox.get()=='':
                self.status.configure(text='Password cannot be blank')
            elif verifyUser(usernamebox.get(),passwordbox.get(),server=paths[0]):
               username,password = usernamebox.get(),passwordbox.get()
               self.LabelFrame.destroy()
               self.update_idletasks()
               Label_4 = Tkinter.Label(self)
               Label_4.configure(background="#d9d9d9")
               Label_4.configure(text='Loading components...')
               Label_4.place(relx=0.5, rely=0.4, anchor=CENTER)
               self.configure(cursor='wait')
               self.LabelFrame.update()
               intDict = showInterfaces(username,password,ipDict)
               policerDict = showPolicer(username,password,ipDict)
               self.configure(cursor='')
               return self.destroy()
            else:
                loginAttempt+=1
                self.status.configure(text='Login attempt ('+str(loginAttempt)+') Failed')
                if loginAttempt==5:
                    message = tkMessageBox.showinfo('Information', 'Too many login attempts by '+usernamebox.get()+'\nPlease confirm the authentication server  \n')
                    username, password = True,True
                    return self.destroy()
            usernamebox.delete(0,END)
            passwordbox.delete(0,END)

        self.TButton1_3 = Tkinter.Button(self.LabelFrame)
        self.TButton1_3.place(relx=0.365, rely=0.633, height=35, width=162
                , bordermode='ignore')
        self.TButton1_3.configure(text='''Login''')
        self.TButton1_3.configure(width=120)
        self.TButton1_3.configure(takefocus=True)
        self.TButton1_3.configure(command=getUser)
        self.TButton1_3.bind('<Return>',getUser)






class OneVlanFinder(Tkinter.Frame):


    def __init__(self, parent, controller):
        Tkinter.Frame.__init__(self,parent)

        self.Labelframe1_1 = Tkinter.LabelFrame(self)
        self.Labelframe1_1.place(relx=0.0, rely=0.09, relheight=1.0, relwidth=0.998)
        self.Labelframe1_1.configure(relief='groove')
        self.Labelframe1_1.configure(foreground="black")
        self.Labelframe1_1.configure(text='''Input Parameters''')
        self.Labelframe1_1.configure(background="#d9d9d9")
        self.Labelframe1_1.configure(width=500)

        Label1_0 = Tkinter.Label(self.Labelframe1_1)

        Label1_1 = Tkinter.Label(self.Labelframe1_1)
        Label1_1.place(relx=0.18, rely=0.09, height=31, width=59
                , bordermode='ignore')
        Label1_1.configure(background="#d9d9d9")
        Label1_1.configure(disabledforeground="#a3a3a3")
        Label1_1.configure(foreground="#000000")
        Label1_1.configure(text='''Router''')
        Label1_1.configure(justify='left')



        def defif(*args):
            global username,password
            try: self.OPTIONS1_2 = intDict[self.ip.get()]
            except KeyError: reason = 'key does not exist in dictionary'
            self.interfaces=StringVar(self.Labelframe1_1)
            self.dropdown1_1.place_forget()
            self.dropdown1_1 = ttk.OptionMenu(self.Labelframe1_1, self.interfaces, 'Select', *self.OPTIONS1_2)
            self.dropdown1_1.place(relx=0.54, rely=0.179, height=34, relwidth=0.308
                    , bordermode='ignore')

        OPTIONS1_1 = ipDict.keys()
        OPTIONS1_1.sort()
        self.ip=StringVar(self.Labelframe1_1)

        dropdown_2 = ttk.OptionMenu(self.Labelframe1_1, self.ip, 'Select', *OPTIONS1_1)
        dropdown_2.place(relx=0.18, rely=0.179, height=34, relwidth=0.312
                , bordermode='ignore')
        self.ip.trace('w',defif)


        Label1_1 = Tkinter.Label(self.Labelframe1_1)
        Label1_1.place(relx=0.54, rely=0.09, height=31, width=88
                , bordermode='ignore')
        Label1_1.configure(background="#d9d9d9")
        Label1_1.configure(disabledforeground="#a3a3a3")
        Label1_1.configure(foreground="#000000")
        Label1_1.configure(text='''Interface''')
        Label1_1.configure(justify='left')


        self.OPTIONS1_2 = []
        self.interfaces=StringVar(self.Labelframe1_1)
        self.dropdown1_1 = ttk.OptionMenu(self.Labelframe1_1, self.interfaces,'Select', *self.OPTIONS1_2)
        self.dropdown1_1.place(relx=0.44, rely=0.179, height=34, relwidth=0.308
                , bordermode='ignore')


        Label1_2 = Tkinter.Label(self.Labelframe1_1)
        Label1_2.place(relx=0.18, rely=0.284, height=31, width=98
                , bordermode='ignore')
        Label1_2.configure(background="#d9d9d9")
        Label1_2.configure(disabledforeground="#a3a3a3")
        Label1_2.configure(foreground="#000000")
        Label1_2.configure(text='''Search type''')
        Label1_2.configure(justify='left')

        self.searchmode=StringVar(self.Labelframe1_1)

        Radiobutton1_1 = ttk.Radiobutton(self.Labelframe1_1, variable=self.searchmode,value='vall')
        Radiobutton1_1.place(relx=0.24, rely=0.373, relheight=0.11
                , relwidth=0.254, bordermode='ignore')
        Radiobutton1_1.configure(takefocus=False)
        Radiobutton1_1.configure(text='''List all vlans''')
        Radiobutton1_1.configure(command=lambda: self.radio('vall'))


        Radiobutton1_2 = ttk.Radiobutton(self.Labelframe1_1, variable=self.searchmode,value='vrange')
        Radiobutton1_2.place(relx=0.53, rely=0.373, relheight=0.11
                , relwidth=0.254, bordermode='ignore')
        Radiobutton1_2.configure(takefocus=False)
        Radiobutton1_2.configure(text='''List in range''')
        Radiobutton1_2.configure(command=lambda: self.radio('vrange'))


        self.Frame1_1 = Tkinter.Frame(self.Labelframe1_1)
        self.Frame1_1.configure(relief='ridge')
        self.Frame1_1.configure(borderwidth="2")
        self.Frame1_1.configure(relief='ridge')
        self.Frame1_1.configure(background="#d9d9d9")
        self.Frame1_1.configure(width=255)

        self.Label1_3 = Tkinter.Label(self.Frame1_1) 
        self.Label1_3.configure(activebackground="#f9f9f9")
        self.Label1_3.configure(activeforeground="black")
        self.Label1_3.configure(background="#d9d9d9")
        self.Label1_3.configure(disabledforeground="#a3a3a3")
        self.Label1_3.configure(foreground="#000000")
        self.Label1_3.configure(highlightbackground="#d9d9d9")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(text='''*Specify range below eg: 100 - 200''')
        self.Label1_3.configure(justify='left')

        font14 = "-family {Segoe UI} -size 8 -weight normal -slant "  \
             "italic -underline 0 -overstrike 0"
        self.Label1_3.configure(font=font14)

        self.vlan1_1 = Tkinter.Entry(self.Frame1_1)
        self.vlan1_1.configure(background="#e2e2e2")
        self.vlan1_1.configure(disabledforeground="#a3a3a3")
        self.vlan1_1.configure(foreground="#000000")
        self.vlan1_1.configure(insertbackground="black")
        self.vlan1_1.configure(width=50)

        self.Label1_4 = Tkinter.Label(self.Frame1_1)
        self.Label1_4.configure(background="#d9d9d9")
        self.Label1_4.configure(disabledforeground="#a3a3a3")
        self.Label1_4.configure(foreground="#000000")
        self.Label1_4.configure(text='''-''')

        self.vlan1_2 = Tkinter.Entry(self.Frame1_1)
        self.vlan1_2.configure(background="#e2e2e2")
        self.vlan1_2.configure(disabledforeground="#a3a3a3")
        self.vlan1_2.configure(foreground="#000000")
        self.vlan1_2.configure(insertbackground="black")
        self.vlan1_2.configure(width=50)


        self.Button1_1 = ttk.Button(self.Labelframe1_1)
        self._img1_1 = PhotoImage(file=cross_icon2)
        self.Button1_1.configure(text='''Clear''',image=self._img1_1, compound= 'left')
        self.Button1_1.configure(command=self.clear)

        self.Button1 = ttk.Button(self.Labelframe1_1, )
        self._img1 = PhotoImage(file=checkmark_icon)
        self.Button1.configure(text='''Search''',image=self._img1, compound= 'left')
        self.Button1.configure(command=lambda: self.executeOneFinder())


        ''' Menu Bar Icons '''

        self.Button1_2Imgvar = PhotoImage(file=back_icon)
        self.Button1_2 = ttk.Button(self, image=self.Button1_2Imgvar)
        self.Button1_2.place(relx=0.864, rely=0.0, height=40, width=86)
        self.Button1_2.configure(command=lambda: controller.show_frame(PageOne))
        self.Button1_2.configure(text='''Back''')
        self.Button1_2.configure(takefocus=False)


    def executeOneFinder(self):
       try: interface = self.interfaces.get()
       except AttributeError:
           reason = 'interface widget has not been created'
           interface = None
       pe = self.ip.get()
       search = self.searchmode.get()
       vlan1, vlan2 = self.vlan1_2.get(),self.vlan1_1.get()


       if not pe or not interface :
           Dialog(self,title='Error',prompt='Choose router and interface\n',
                           nobutton=True,icon=cancel_icon)
           return None
       if pe == 'Select' or interface == 'Select':
           Dialog(self,title='Error',prompt='Choose router and interface\n',
                           nobutton=True,icon=cancel_icon)
           return None
       if interface == 'Null':
           Dialog(self,title='Interface missing',prompt='Interfaces could not be loaded during start-up\nBasoNx could not contact the device\nMake sure the device is up and can be accessed\nthen restart basoNx\n',
                           nobutton=True,icon=cancel_icon)
           return None
       if vlan1 > vlan2 :
           Dialog(self,title='Error',prompt='Start range cannot be greater than end\n',
                           nobutton=True,icon=cancel_icon)
           return None
       if not vlan1 or not vlan2 : search = 'vall'

       if vlan1 and vlan2:
           endpoints = [vlan1,vlan2]
           for item in endpoints:
               try: item = int(item)
               except ValueError:
                   Dialog(self,title='Error',prompt='Start and endpoint must be numbers\n',
                           nobutton=True,icon=cancel_icon)
                   return None
           vlan1,vlan2 = int(vlan1), int(vlan2)

       if vlan1 > vlan2 :
           Dialog(self,title='Error',prompt='Start point cannot be greater than end\n',
                           nobutton=True,icon=cancel_icon)
           return None

       answer = Dialog(self,title='Confirm',prompt='Proceed with search?  \n'+interface+' @ '+pe+'  \n',
                       icon=ask_icon,lbutton='Yes',rbutton='No')

       if answer.ans == 'ok':

           self.loading = loading(self,frontend)
           output= outputWin()
           output.TB2('Vlan Finder',buttonvfinderun(username,password,pe,ipDict,interface,search,vlan1,vlan2),frontend,self)
           self.loading.stop(frontend)
           frontend.attributes('-disabled', True)
           self.clear()

    def clear(self):
        self.OPTIONS1_2 = []
        self.dropdown1_1.place_forget()
        self.dropdown1_1 = ttk.OptionMenu(self.Labelframe1_1, self.interfaces,'Select', *self.OPTIONS1_2)
        self.dropdown1_1.place(relx=0.44, rely=0.179, height=34, relwidth=0.308
                    , bordermode='ignore')

        self.ip.set('Select')
        self.searchmode.set(None)
        widgets = [self.vlan1_1,self.vlan1_2,
                   self.Label1_3,self.Label1_4,self.Frame1_1,
                   self.Button1_1,self.Button1]
        for widget in widgets:
            try: widget.place_forget()
            except AttributeError : attributeError = True


    def radio(self,search):

        if search == 'vall':
            self.Button1_1.place(relx=0.54, rely=0.600, height=42, width=120
                , bordermode='ignore')
            self.Button1.place(relx=0.30, rely=0.600, height=42, width=120
              , bordermode='ignore')

            try:
                self.Frame1_1.place_forget()
                self.vlan1_1.place_forget()
                self.vlan1_2.place_forget()
                self.Label1_3.place_forget()
                self.Label1_4.place_forget()
            except AttributeError : attributeError = True

        if search == 'vrange':
            try:
                self.Button1_1.place_forget()
                self.Button1.place_forget()
            except AttributeError : attributeError = True
            self.Frame1_1.place(relx=0.24, rely=0.507, relheight=0.224, relwidth=0.51
                 , bordermode='ignore')

            self.Button1_1.place(relx=0.54, rely=0.776, height=42, width=120
                , bordermode='ignore')

            self.Button1.place(relx=0.30, rely=0.776, height=42, width=120
              , bordermode='ignore')

            self.vlan1_1.place(relx=0.569, rely=0.467, height=26, relwidth=0.369
                    , bordermode='ignore')

            self.Label1_4.place(relx=0.472, rely=0.467, height=26, width=13
                    , bordermode='ignore')

            self.vlan1_2.place(relx=0.059, rely=0.467, height=26, relwidth=0.369
                    , bordermode='ignore')

            self.Label1_3.place(relx=0.039, rely=0.04, height=31, width=280
                    , bordermode='ignore')




class TwoVlanFinder(Tkinter.Frame):

    def __init__(self, parent, controller):
        Tkinter.Frame.__init__(self,parent)

        self.Labelframe2_1 = Tkinter.LabelFrame(self)
        self.Labelframe2_1.place(relx=0.0, rely=0.09, relheight=1.0, relwidth=0.998)
        self.Labelframe2_1.configure(relief='groove')
        self.Labelframe2_1.configure(foreground="black")
        self.Labelframe2_1.configure(text='''Input Parameters''')
        self.Labelframe2_1.configure(background="#d9d9d9")
        self.Labelframe2_1.configure(width=500)


        Label2_1 = Tkinter.Label(self.Labelframe2_1)
        Label2_1.place(relx=0.18, rely=0.09, height=31, width=59
                , bordermode='ignore')
        Label2_1.configure(background="#d9d9d9")
        Label2_1.configure(disabledforeground="#a3a3a3")
        Label2_1.configure(foreground="#000000")
        Label2_1.configure(text='''Router''')
        Label2_1.configure(justify='left')


        def defif1(*args):
            global username,password
            try: self.OPTIONS2_3 = intDict[self.ip1.get()]
            except KeyError: reason = 'key does not exist in dictionary'
            self.interfaces2_1=StringVar(self.Labelframe2_1)
            self.dropdown2_3.place_forget()
            self.dropdown2_3 = ttk.OptionMenu(self.Labelframe2_1, self.interfaces2_1, 'Select', *self.OPTIONS2_3)
            self.dropdown2_3.place(relx=0.54, rely=0.179, height=34, relwidth=0.308
                    , bordermode='ignore')

        def defif2(*args):
            global username,password
            try: self.OPTIONS2_4 = intDict[self.ip2.get()]
            except KeyError: reason = 'key does not exist in dictionary'
            self.interfaces2_2=StringVar(self.Labelframe2_1)
            self.dropdown2_4.place_forget()
            self.dropdown2_4 = ttk.OptionMenu(self.Labelframe2_1, self.interfaces2_2, 'Select', *self.OPTIONS2_4)
            self.dropdown2_4.place(relx=0.54, rely=0.286, height=34, relwidth=0.308
                , bordermode='ignore')


        OPTIONS2_1 = ipDict.keys()
        OPTIONS2_1.sort()
        self.ip1=StringVar(self.Labelframe2_1)

        dropdown2_1 = ttk.OptionMenu(self.Labelframe2_1, self.ip1,'Select PE1', *OPTIONS2_1)
        dropdown2_1.place(relx=0.18, rely=0.180, height=34, relwidth=0.312
                , bordermode='ignore')
        self.ip1.trace('w',defif1)

        OPTIONS2_2 = ipDict.keys()
        OPTIONS2_2.sort()
        self.ip2=StringVar(self.Labelframe2_1)
        dropdown2_2 = ttk.OptionMenu(self.Labelframe2_1, self.ip2,'Select PE2', *OPTIONS2_2)
        dropdown2_2.place(relx=0.18, rely=0.286, height=34, relwidth=0.312
                , bordermode='ignore')
        self.ip2.trace('w',defif2)

        Label2_2 = Tkinter.Label(self.Labelframe2_1)
        Label2_2.place(relx=0.54, rely=0.09, height=31, width=88
                , bordermode='ignore')
        Label2_2.configure(background="#d9d9d9")
        Label2_2.configure(disabledforeground="#a3a3a3")
        Label2_2.configure(foreground="#000000")
        Label2_2.configure(text='''Interface''')
        Label2_2.configure(justify='left')


        self.OPTIONS2_3 = []
        self.interfaces2_1=StringVar(self.Labelframe2_1)
        self.dropdown2_3 = ttk.OptionMenu(self.Labelframe2_1, self.interfaces2_1,'Select', *self.OPTIONS2_3)
        self.dropdown2_3.configure(width=10)
        self.dropdown2_3.place(relx=0.54, rely=0.180, height=34, relwidth=0.308
                , bordermode='ignore')

        self.OPTIONS2_4 = []
        self.interfaces2_2=StringVar(self.Labelframe2_1)
        self.dropdown2_4 = ttk.OptionMenu(self.Labelframe2_1, self.interfaces2_2,'Select', *self.OPTIONS2_4)
        self.dropdown2_4.configure(width=10)
        self.dropdown2_4.place(relx=0.54, rely=0.286, height=34, relwidth=0.308
                , bordermode='ignore')


        Label2_3 = Tkinter.Label(self.Labelframe2_1)
        Label2_3.place(relx=0.18, rely=0.392, height=28, width=90
                , bordermode='ignore')
        Label2_3.configure(background="#d9d9d9")
        Label2_3.configure(disabledforeground="#a3a3a3")
        Label2_3.configure(foreground="#000000")
        Label2_3.configure(text='''Search type''')
        Label2_3.configure(justify='left')

        self.searchmode=StringVar(self.Labelframe2_1)

        Radiobutton2_1 = ttk.Radiobutton(self.Labelframe2_1, variable=self.searchmode,value='vall')
        Radiobutton2_1.place(relx=0.24, rely=0.476, relheight=0.11
                , relwidth=0.254, bordermode='ignore')
        Radiobutton2_1.configure(takefocus=False)
        Radiobutton2_1.configure(text='''List all vlans''')
        Radiobutton2_1.configure(command=lambda: self.radio('vall'))


        Radiobutton2_2 = ttk.Radiobutton(self.Labelframe2_1, variable=self.searchmode,value='vrange')
        Radiobutton2_2.place(relx=0.53, rely=0.476, relheight=0.11
                , relwidth=0.254, bordermode='ignore')
        Radiobutton2_2.configure(takefocus=False)
        Radiobutton2_2.configure(text='''List in range''')
        Radiobutton2_2.configure(command=lambda: self.radio('vrange'))



        self.Frame2_1 = Tkinter.Frame(self.Labelframe2_1)
        self.Frame2_1.configure(relief='ridge')
        self.Frame2_1.configure(borderwidth="2")
        self.Frame2_1.configure(background="#d9d9d9")
        self.Frame2_1.configure(width=255)

        self.Label2_4 = Tkinter.Label(self.Frame2_1)
        self.Label2_4.configure(activebackground="#f9f9f9")
        self.Label2_4.configure(activeforeground="black")
        self.Label2_4.configure(background="#d9d9d9")
        self.Label2_4.configure(disabledforeground="#a3a3a3")
        self.Label2_4.configure(foreground="#000000")
        self.Label2_4.configure(highlightbackground="#d9d9d9")
        self.Label2_4.configure(highlightcolor="black")
        self.Label2_4.configure(text='''Specify range below eg: 10 - 200''')
        self.Label2_4.configure(justify='left')
        font14 = "-family {Segoe UI} -size 8 -weight normal -slant "  \
             "italic -underline 0 -overstrike 0"
        self.Label2_4.configure(font=font14)

        self.vlan2_1 = Tkinter.Entry(self.Frame2_1)
        self.vlan2_1.configure(background="#e2e2e2")
        self.vlan2_1.configure(disabledforeground="#a3a3a3")
        self.vlan2_1.configure(foreground="#000000")
        self.vlan2_1.configure(insertbackground="black")
        self.vlan2_1.configure(width=50)


        self.Label2_5 = Tkinter.Label(self.Frame2_1)
        self.Label2_5.configure(background="#d9d9d9")
        self.Label2_5.configure(disabledforeground="#a3a3a3")
        self.Label2_5.configure(foreground="#000000")
        self.Label2_5.configure(text='''-''')

        self.vlan2_2 = Tkinter.Entry(self.Frame2_1)
        self.vlan2_2.configure(background="#e2e2e2")
        self.vlan2_2.configure(disabledforeground="#a3a3a3")
        self.vlan2_2.configure(foreground="#000000")
        self.vlan2_2.configure(insertbackground="black")
        self.vlan2_2.configure(width=50)


        self._img2_1 = PhotoImage(file=checkmark_icon)
        self.Button2_1 = ttk.Button(self.Labelframe2_1)
        self.Button2_1.configure(text='''Search''', image = self._img2_1, compound = 'left' )
        self.Button2_1.configure(command=lambda: self.executeTwoFinder())

        self._img2_2 = PhotoImage(file=cross_icon2)
        self.Button2_2 = ttk.Button(self.Labelframe2_1)
        self.Button2_2.configure(text='''Clear''',image=self._img2_2, compound = 'left')
        self.Button2_2.configure(command=self.clear)


        ''' Menu Bar Icons '''

        self.Button2_3Imgvar = PhotoImage(file=back_icon)
        self.Button2_3 = ttk.Button(self, image=self.Button2_3Imgvar)
        self.Button2_3.place(relx=0.864, rely=0.0, height=40, width=86)
        self.Button2_3.configure(command=lambda: controller.show_frame(PageOne))
        self.Button2_3.configure(text='''Back''')
        self.Button2_3.configure(takefocus=False)



    def executeTwoFinder(self):
       try: interface1,interface2 = self.interfaces2_1.get(),self.interfaces2_2.get()
       except AttributeError:
           reason = 'interface widget has not been created'
           interface1,interface2 = None, None

       pe1,pe2 = self.ip1.get(),self.ip2.get()
       search = self.searchmode.get()
       vlan1, vlan2 = self.vlan2_2.get(), self.vlan2_1.get()

       if not pe1 or not interface1 :
           Dialog(self,title='Error',prompt='Choose first router and interface\n',
                   nobutton=True,icon=cancel_icon)
           return None
       if not pe2 or not interface2 :
           Dialog(self,title='Error',prompt='Choose second router and interface\n',
                   nobutton=True,icon=cancel_icon)
           return None
       if pe1 == 'Select PE1' or interface1 == 'Select':
           Dialog(self,title='Error',prompt='Choose first router and interface\n',
                   nobutton=True,icon=cancel_icon)
           return None
       if pe2 == 'Select PE2' or interface2 == 'Select':
           Dialog(self,title='Error',prompt='Choose second router and interface\n',
                   nobutton=True,icon=cancel_icon)
           return None

       if interface1 == 'Null' or interface2 == 'Null':
           Dialog(self,title='Interface missing',
                  prompt='Interfaces could not be loaded during start-up\nBasoNx could not contact the device\nMake sure the device is up and can be accessed\nthen restart basoNx\n',
                  nobutton=True,icon=cancel_icon)
           return None
       if not vlan1 or not vlan2 : search = 'vall'

       if vlan1 and vlan2:
           endpoints = [vlan1,vlan2]
           for item in endpoints:
               try: item = int(item)
               except ValueError:
                   Dialog(self,title='Error',prompt='Start and endpoint must be numbers\n',
                           nobutton=True,icon=cancel-icon)
                   return None
           vlan1,vlan2 = int(vlan1), int(vlan2)

       if vlan1 > vlan2 :
           Dialog(self,title='Error',prompt='Start range cannot be greater than end\n',
                   nobutton=True,icon=cancel_icon)
           return None

       answer = Dialog(self,title='Confirm',prompt='Proceed with search?  \n'+interface1+' @ '+pe1+'  \n'+interface2+' @ '+pe2+'  \n',
                       lbutton='Yes',rbutton='No',icon=ask_icon)


       if answer.ans == 'ok':

           self.loading = loading(self,frontend)
           output= outputWin()
           output.TB2('Vlan Finder',buttonvfinderdx(username, password,pe1, interface1, pe2, interface2, ipDict,search,vlan1,vlan2),frontend,self)
           self.loading.stop(frontend)
           frontend.attributes('-disabled', True)
           self.clear()

    def clear(self):
        self.OPTIONS2_3 = []
        self.dropdown2_3.place_forget()
        self.dropdown2_3 = ttk.OptionMenu(self.Labelframe2_1, self.interfaces2_1,'Select', *self.OPTIONS2_3)
        self.dropdown2_3.place(relx=0.44, rely=0.180, height=34, relwidth=0.312
                , bordermode='ignore')

        self.OPTIONS2_4 = []
        self.dropdown2_4.place_forget()
        self.dropdown2_4 = ttk.OptionMenu(self.Labelframe2_1, self.interfaces2_2,'Select', *self.OPTIONS2_4)
        self.dropdown2_4.place(relx=0.44, rely=0.286, height=34, relwidth=0.312
                , bordermode='ignore')

        self.ip1.set('Select PE1')
        self.ip2.set('Select PE2')
        self.searchmode.set(None)
        entries = [self.vlan2_1,self.vlan2_2]
        for entry in entries:
            try: entry.delete(0,END)
            except AttributeError : reason = 'widget do not exist'
        widgets = [self.vlan2_1,self.vlan2_2,
                   self.Label2_4,self.Label2_5,
                   self.Button2_1,self.Button2_2,self.Frame2_1]
        for widget in widgets:
            try: widget.place_forget()
            except AttributeError : reason = 'widget do not exist'


    def radio(self,search):
        if search == 'vall':
            self.Button2_2.place(relx=0.54, rely=0.736, height=42, width=120
                , bordermode='ignore')
            self.Button2_1.place(relx=0.30, rely=0.736, height=42, width=120
              , bordermode='ignore')

            try:
                self.vlan2_1.place_forget()
                self.vlan2_2.place_forget()
                self.Label2_4.place_forget()
                self.Label2_5.place_forget()
                self.Frame2.place_forget()
            except AttributeError : attributeError = True
        if search == 'vrange':
            try:
                self.Button2_1.place_forget()
                self.Button2_2.place_forget()
            except AttributeError : attributeError = True

            self.Frame2_1.place(relx=0.24, rely=0.473, relheight=0.224, relwidth=0.51
                 , bordermode='ignore')

            self.Button2_2.place(relx=0.54, rely=0.736, height=42, width=120
                , bordermode='ignore')

            self.Button2_1.place(relx=0.30, rely=0.736, height=42, width=120
              , bordermode='ignore')

            self.vlan2_1.place(relx=0.569, rely=0.52, height=30, relwidth=0.369
                    , bordermode='ignore')

            self.Label2_5.place(relx=0.472, rely=0.52, height=22, width=13
                    , bordermode='ignore')

            self.vlan2_2.place(relx=0.059, rely=0.52, height=30, relwidth=0.369
                    , bordermode='ignore')

            self.Label2_4.place(relx=0.04, rely=0.08, height=31, width=280
                    , bordermode='ignore')



class Check(Tkinter.Frame):

    def __init__(self, parent, frame, searchType):
        Tkinter.Frame.__init__(self,parent)

        self.parent = parent

        Labelframe3_1 = Tkinter.LabelFrame(frame)
        Labelframe3_1.place(relx=0.0, rely=0.09, relheight=0.996, relwidth=0.998)
        Labelframe3_1.configure(relief='groove')
        Labelframe3_1.configure(foreground="black")
        Labelframe3_1.configure(text='''Input Parameters''')
        Labelframe3_1.configure(background="#d9d9d9")
        Labelframe3_1.configure(width=500)


        Label3_1 = Tkinter.Label(Labelframe3_1)
        Label3_1.place(relx=0.05, rely=0.09, height=31, width=126
                , bordermode='ignore')
        Label3_1.configure(background="#d9d9d9")
        Label3_1.configure(disabledforeground="#a3a3a3")
        Label3_1.configure(foreground="#000000")
        Label3_1.configure(text=searchType.capitalize()+''' to locate''')
        Label3_1.configure(anchor='w')


        self.item3_1 = ttk.Combobox(Labelframe3_1,font=('Calibri', 10,'normal'))
        self.item3_1.place(relx=0.05, rely=0.180, height=30, relwidth=0.308
                , bordermode='ignore')
        self.item3_1.configure(background="white")
        self.item3_1.configure(foreground="#000000")
        self.item3_1.configure(width=50)

        if searchType == 'Delete ticket':
            Label3_1.configure(text='Choose ticket')
            self.server = Server(paths[6],paths[5],paths[7],'*')
            if self.server.up:
                self.stdict = self.server.retrieveRemoteFile(stdict=True)
                self.sts = StringVar(Labelframe3_1)
                self.item3_1.configure(textvar=self.sts,values=self.stdict.keys(),state='readonly')
            else: Dialog(self.parent,prompt='Can not access server \n'+server+' \n')


        self.Label3_3 = Tkinter.Label(Labelframe3_1)
        self.Label3_3.configure(activebackground="#f9f9f9")
        self.Label3_3.configure(activeforeground="black")
        self.Label3_3.configure(background="#d9d9d9")
        self.Label3_3.configure(disabledforeground="#a3a3a3")
        self.Label3_3.configure(foreground="#000000")
        self.Label3_3.configure(highlightbackground="#d9d9d9")
        self.Label3_3.configure(highlightcolor="black")
        self.Label3_3.configure(justify='left')
        font14 = "-family {Segoe UI} -size 8 -weight normal -slant "  \
             "italic -underline 0 -overstrike 0"
        self.Label3_3.configure(font=font14,anchor='w')

        Button3_1 = ttk.Button(Labelframe3_1)
        Button3_1.place(relx=0.05, rely=0.294, height=36, width=98, bordermode='ignore')
        self.Button3_1Imgvar = PhotoImage(file=checkmark_icon)
        Button3_1.configure(text='''Search''',image=self.Button3_1Imgvar)
        Button3_1.configure(command=lambda: self.executeCheck(frame,searchType))


        Button3_2 = ttk.Button(Labelframe3_1)
        Button3_2.place(relx=0.205, rely=0.294, height=36, width=98
                        , bordermode='ignore')
        self._img3_2 = PhotoImage(file=cross-icon2)
        Button3_2.configure(text='''Clear''',image=self._img3_2)
        Button3_2.configure(command=self.clear)

        self.bind("<Return>", lambda: self.executeCheck(frame,searchType))
        self.bind("<Escape>", self.clear)

        ''' Menu Bar Icons '''

        self.Button3_3Imgvar = PhotoImage(file=back_icon)
        self.Button3_3 = ttk.Button(parent, image=self.Button3_3Imgvar)
        self.Button3_3.place(relx=0.864, rely=0.0, height=40, width=86)
        self.Button3_3.configure(command=lambda: back())
        self.Button3_3.configure(text='''Back''')
        self.Button3_3.configure(takefocus=False)

        def back():
            Labelframe3_1.destroy()
            self.Button3_3.destroy()

    def executeCheck(self,frame,searchType):
       self.Label3_3.configure(text='')
       self.Label3_3.place(relx=0.05, rely=0.4, height=28, width=240, bordermode='ignore')

       if searchType == 'NAME':
           searchItem = self.item3_1.get()

           answer = Dialog(self.parent,title='Confirm',prompt='Proceed with search?  \n'+searchType.capitalize()+' '+searchItem+'\n',
                           lbutton='Yes',rbutton='No', resizable=False,
                           icon=ask_icon)

           if answer.ans == 'ok':
               self.loading = loading(frame,frontend)
               output= outputWin()
               output.TB2('Locate '+searchType,buttondcheck(username,password,ipDict,searchItem),frontend,self)
               self.loading.stop(frontend)
               frontend.attributes('-disabled', True)
               self.clear()

       if searchType == 'VLAN':
           searchItem = self.item3_1.get()
           try:
               if int(searchItem) not in range(0,4095):
                    self.Label3_3.configure(text='''VLAN must be in range 1 - 4094''')
                    return None
           except ValueError:
               self.Label3_3.configure(text='''*VLAN must be in range 1 - 4094''')
               return None

           answer = Dialog(self.parent,title='Confirm',prompt='Proceed with search?  \n'+searchType.capitalize()+' '+searchItem+'\n',
                           lbutton='Yes',rbutton='No',resizable=False,
                           icon=ask_icon)

           if answer.ans == 'ok':
               self.loading = loading(frame,frontend)
               output= outputWin()
               output.TB2('Locate '+searchType, buttonvcheck(username,password,ipDict,searchItem),frontend,self)
               self.loading.stop(frontend)
               frontend.attributes('-disabled', True)
               self.clear()


       if searchType == 'IP':
           searchItem = self.item3_1.get()
           if not "/" in searchItem or len(searchItem.split("."))!=4 :
               self.Label3_3.configure(text='''Enter correct subnet/mask''')
               return None

           try:
               subnetmask = searchItem.split(".")[3].split("/")[-1]
           except IndexError:
               self.Label3_3.configure(text='''Enter correct subent/mask''')
               return None
           try:
               if not int(subnetmask) in range(8,33):
                   self.Label3_3.configure(text='''Subnet must be /8 - /32''')
                   return None
               for octate in searchItem.split("."):
                   if "/" in octate: octate = octate.split("/")[0]
                   if int(octate)>255:
                       self.Label3_3.configure(text='''Wrong IP address entered''')
                       return None
           except ValueError:
               self.Label3_3.configure(text='''Wrong IP address entered''')
               return None

           answer = Dialog(self.parent,title='Confirm',prompt='Proceed with search?  \n'+searchType.capitalize()+' '+searchItem+'\n',
                           lbutton='Yes',rbutton='No',resizable=False,
                           icon=ask_icon)

           if answer.ans == 'ok':
               self.loading = loading(frame,frontend)
               output= outputWin()
               output.TB2('Locate '+searchType,buttonicheck(username,password,ipDict,searchItem),frontend,self)
               self.loading.stop(frontend)
               frontend.attributes('-disabled', True)
               self.clear()


       if searchType == 'Delete ticket':
           ticket = self.item3_1.get()
           jobid = self.stdict[ticket]
           serv = Server(serverdata[0],serverdata[1],serverdata[2],ticket+'.sh')
           if serv.up:
               success = check_icon
               serv.deleteFromRemoteFile(ticket,jobid)
               time.sleep(1)
               Dialog(self.parent,prompt='Ticket '+ticket+' deleted successfully \n',icon=success)
               self.item3_1.set('')

           else:
              error = cancel-icon
              Dialog(self.parent,prompt='Can not access server \n'+server+' \n',icon=error)
              return False



    def clear(self):
        self.item3_1.delete(0,END)
        self.Label3_3.place_forget()



def loadfile(button,var):

    # dialog for opening files

    openfilename=tkFileDialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    try:
        fp=open(openfilename,"r")
        for line in fp : var.append(line.strip())
        fp.close()
    except:
        if button != None:
            button.set(sys.exc_info()[1])
        return
    if button != None:
        button.set(openfilename.split('/')[-1])



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





def main():

    paths = readsettings(None)
    if not paths:sys.exit()

    serverdata = [paths[6],paths[5],paths[7]]

    '''Will be used by login page to store credentials'''
    username,password,loginAttempt = '','',0

    try: ipDict = getIpFromFile(path=paths[1])
    except IOError:
        d = Settings(None,paths=paths)
        Dialog(d,nobutton=True, resizable=False,
               prompt='Device database not found \nPlease confirm the path to device database \nfrom the general settings tab then restart \nthe application\n')
        d.mainloop()
        sys.exit()

    if not ipDict:
        frontend = outputWin()
        frontend.Error()
        sys.exit()

    loginwin=LoginPage()
    loginwin.mainloop()

    if username and password:
        frontend = basoNx()
        frontend.mainloop()



if __name__=='__main__':
   main()
