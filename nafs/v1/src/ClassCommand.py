# This module is part of the core Basondole Tools
# This code provides GUI for user to issue commands to hosts
# The commands will be sent to the hosts via SSH and the output will be returned on a window
# Commands and hosts can be input directly in the input window or can be loaded from a file
# Does not play well with commands that result to infinite lines of output such us continous ping
# AUTHOR: Paul S.I. Basondole

import Tkinter
from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox

import re
import time
import paramiko
import socket
import Queue
import threading
from initial import getIpFromFile
from ClassLoading import loading
from ClassOutput import outputWin

# variables for GUI icons defined as path to the icon
home_icon='C:\Users\u\Desktop\PACOM\icon\home-icon2.gif'
checkmark_icon='C:\Users\u\Desktop\PACOM\icon\\checkmark-icon.gif'
cross_icon2='C:\Users\u\Desktop\PACOM\icon\\cross-icon2.gif'
program_icon='C:\Users\u\Desktop\PACOM\icon\paul-icon1.ico'

class Commandwindow(Tkinter.Frame):


    def __init__(self, parent, ipDict, username, password):

        Tkinter.Frame.__init__(self,parent)

        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
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

        self.username = username
        self.password = password

        self.Labelframe1 = Tkinter.LabelFrame(parent)
        self.Labelframe1.place(relx=0.0, rely=0.09, relheight=0.997
                , relwidth=0.998)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Input Parameters''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(width=500)


        ''' Menu Bar Icons '''

        def home():
            self.Labelframe1.destroy()
            parent.show_frame('home')

        self.Button0_1Imgvar = PhotoImage(file=home_icon)
        self.Button0_1 = ttk.Button(parent, image=self.Button0_1Imgvar)
        self.Button0_1.place(relx=0.0, rely=0.0, height=40, width=102,bordermode='ignore')
        self.Button0_1.configure(command=lambda: home())
        self.Button0_1.configure(takefocus=False)
        self.Button0_1.configure(text='''Home''',compound='left')
        ''' EOF Menu Bar Icons '''

        self.Label1_4 = Tkinter.Label(self.Labelframe1)
        self.Label1_4.place(relx=0.17, rely=0.09, height=31, width=99
                , bordermode='ignore')
        self.Label1_4.configure(activebackground="#f9f9f9")
        self.Label1_4.configure(activeforeground="black")
        self.Label1_4.configure(background="#d9d9d9")
        self.Label1_4.configure(disabledforeground="#a3a3a3")
        self.Label1_4.configure(foreground="#000000")
        self.Label1_4.configure(highlightbackground="#d9d9d9")
        self.Label1_4.configure(highlightcolor="black")
        self.Label1_4.configure(text='''Command''')
        self.Label1_4.configure(width=99)

        self.Label1_1 = Tkinter.Label(self.Labelframe1)
        self.Label1_1.place(relx=0.18, rely=0.373, height=31, width=128
                , bordermode='ignore')
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(activeforeground="black")
        self.Label1_1.configure(background="#d9d9d9")
        self.Label1_1.configure(disabledforeground="#a3a3a3")
        self.Label1_1.configure(foreground="#000000")
        self.Label1_1.configure(highlightbackground="#d9d9d9")
        self.Label1_1.configure(highlightcolor="black")
        self.Label1_1.configure(anchor='w')
        self.Label1_1.configure(width=128)
        self.Label1_1.configure(text='''Command''')


        self.Label1_3 = Tkinter.Label(self.Labelframe1)
        self.Label1_3.place(relx=0.525, rely=0.373, height=31, width=98
                , bordermode='ignore')
        self.Label1_3.configure(activebackground="#f9f9f9")
        self.Label1_3.configure(activeforeground="black")
        self.Label1_3.configure(background="#d9d9d9")
        self.Label1_3.configure(disabledforeground="#a3a3a3")
        self.Label1_3.configure(foreground="#000000")
        self.Label1_3.configure(highlightbackground="#d9d9d9")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(anchor='w')
        self.Label1_3.configure(text='''Devices''')


        def butact(*args):
            choice = self.Button1_5.get()
            if choice == 'Load File':
                self.commands = []
                loadfile(self.Button1_5,self.commands)
            else:
                self.commands = []
                self.commands.append(choice)

        self.commands = []
        self.command_list = ['Load File']
        self.comselect = StringVar(self.Labelframe1)

        self.Button1_5 = ttk.Combobox(self.Labelframe1)
        self.Button1_5.configure(textvar=self.comselect, values=self.command_list)
        self.Button1_5.place(relx=0.185, rely=0.478, height=32, relwidth=0.308
                , bordermode='ignore')
        self.Button1_5.bind("<<ComboboxSelected>>", butact)
        self.Button1_5.set('type | upload')



        def comboxact(*args):
            choice = self.TCombobox2.get()
            if choice == 'Load File':
                self.devices = []
                loadfile(self.TCombobox2,self.devices)
            elif choice == 'All Juniper':
                self.devices = []
                for line in createDb(ipDict,'juniper').split('\n'):
                    line = line.split()[0]
                    self.devices.append(line.strip())
            elif choice == 'All Cisco':
                self.devices = []
                try:
                    for line in createDb(ipDict,'cisco').split('\n'):
                        line = line.split()[0]
                        self.devices.append(line.strip())
                except IndexError: tkMessageBox.showerror('Error','No cisco device in list')
            else:
                self.devices = []
                self.devices.append(choice)

        self.devices = []
        self.devselect = StringVar(self.Labelframe1)

        self.TCombobox2 = ttk.Combobox(self.Labelframe1)
        self.TCombobox2.place(relx=0.525, rely=0.478, height=32
                , relwidth=0.308, bordermode='ignore')
        self.value_list = ['All Cisco','All Juniper','Load File',]
        self.TCombobox2.configure(textvar=self.devselect, values=self.value_list)
        self.TCombobox2.configure(width=152)
        self.TCombobox2.configure(takefocus="")
        self.TCombobox2.bind("<<ComboboxSelected>>", comboxact)
        self.TCombobox2.set('type | select')

        self.Scrolledentry1 = ScrolledEntry(self.Labelframe1)
        self.Scrolledentry1.place(relx=0.18, rely=0.194, height=55
                , relwidth=0.648, bordermode='ignore')
        self.Scrolledentry1.configure(background="white")
        self.Scrolledentry1.configure(disabledforeground="#a3a3a3")
        self.Scrolledentry1.configure(foreground="black")
        self.Scrolledentry1.configure(highlightbackground="#d9d9d9")
        self.Scrolledentry1.configure(highlightcolor="black")
        self.Scrolledentry1.configure(insertbackground="black")
        self.Scrolledentry1.configure(insertborderwidth="1")
        self.Scrolledentry1.configure(selectbackground="#c4c4c4")
        self.Scrolledentry1.configure(selectforeground="black")
        self.Scrolledentry1.configure(width=15)
        self.Scrolledentry1.insert(0,'Only issue commands with finite output lines. Commands tha produce continous output eg: continous ping cannot be processed correctly')
        self.Scrolledentry1.configure(state='readonly')


        self.Button1 = ttk.Button(self.Labelframe1)
        self.Button1.place(relx=0.26, rely=0.657, height=40, width=120
                , bordermode='ignore')
        self.Button1.configure(command= lambda: self.execute(parent,self.commands,self.devices))
        self._img1 = PhotoImage(file=checkmark_icon)
        self.Button1.configure(text='''Send''',image=self._img1)


        self.Button1_6 = ttk.Button(self.Labelframe1)
        self.Button1_6.place(relx=0.54, rely=0.657, height=40, width=120
                , bordermode='ignore')
        self.Button1_6.configure(command=lambda: self.clear())
        self._img1_6 = PhotoImage(file=cross_icon2)
        self.Button1_6.configure(text='''Clear''',image=self._img1_6)


    def execute(self,parent,commandList,deviceList):
           username = self.username
           password = self.password

           self.output = ''

           if not commandList:
              command = self.comselect.get()
              if command : commandList = [command]
           if not deviceList:
              device = self.devselect.get()
              if device: deviceList = [device]


           if not commandList or deviceList ==1: return

           def kazi(username,password,ipaddress,lock):
              sshClient = paramiko.SSHClient()
              sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              try:
                 try:
                    sshClient.connect(ipaddress, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
                    authenticated = True
                 except (socket.error, paramiko.AuthenticationException):
                    authenticated = False
                    with lock: self.output+= '\n'+(time.ctime()+" (user = "+username+") failed authentication > "+ipaddress.ljust(15))

                 if authenticated==True:
                    deviceOutput = ''
                    secureCli = sshClient.invoke_shell()
                    time.sleep(0.1)
                    secureCli.send('set cli screen-length 0\n')
                    secureCli.send('terminal length 0\n')
                    for line in commandList:
                       secureCli.send(line)
                       secureCli.send('\n')
                    time.sleep(2)
                    try:
                       secureCli.send('quit\n')
                       secureCli.send('exit\n')
                    except socket.error: sessionClosed=True
                    time.sleep(5)
                    while True:
                       output = secureCli.recv(65535)
                       if not output: break
                       for line in output:
                          deviceOutput+=line
                    outputList = deviceOutput.split('\n')
                    sshClient.close()
                    self.output+= '\n'+('\n')
                    CISCOEXEC = '#'#+commandList[0]
                    CISCOUSER = '>'#+commandList[0]
                    JUNIPEROP = '> '#+commandList[0][0]+commandList[0][1]
                    LINUXUSER = '$ '#+commandList[0]
                    LINUXROOT = '# '#+commandList[0]
                    start = None
                    end = None
                    for line in outputList:
                       if CISCOEXEC in line and commandList[0] in line:
                          start=(line)
                          break
                       if CISCOUSER in line and commandList[0] in line:
                          start=(line)
                          break
                       if JUNIPEROP in line and (commandList[0].split())[0] in line:
                          start=(line)
                          break
                       if LINUXUSER in line and commandList[0] in line:
                          start=(line)
                          break
                       if LINUXROOT in line and commandList[0] in line:
                          start=(line)
                          break

                    for line in outputList:
                       if re.findall(r'[>#$].*(quit|exit)',line):
                          end = (line)
                          break

                    if start==None:
                       with lock: self.output+= '\n'+ ('['+ipaddress+']')+'\n'+ 'Device is up but taking too long to respond'

                    else:
                       with lock:
                           self.output+= '\n'+ ('['+ipaddress+']')
                           for line in range(outputList.index(start),outputList.index(end)):
                               self.output+= '\n' + '   '+outputList[line]

              except:
                 self.output+= '\n [' + ipaddress+'] ' + sys.exc_info()[1]


           threads = []
           lock = threading.Lock()

           self.loading = loading(self,parent)

           for ipaddress in deviceList:
              t = threading.Thread(target=kazi, args=(username,password,ipaddress,lock))
              t.start()
              threads.append(t)
           for t in threads:
              t.join()
           self.devices, self.commands = [],[]


           output= outputWin()
           output.TB2('Commands',self.output,parent,self)
           self.loading.stop(parent)
           parent.attributes('-disabled', True)
           self.clear()

    def clear(self):
       self.TCombobox2.set('')
       self.Button1_5.set('')



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


def loadfile(button,var):

    # dialog for openening files

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


def test():

    ipDict = getIpFromFile()
    username = 'fisi'
    password = 'fisi123'
    parent = Tkinter.Tk()

    parent.iconbitmap(default=program_icon)
    parent.title('Big Paul Tools')
    parent.geometry("501x336+387+422")

    Commandwindow(parent,ipDict, username,password)

    parent.mainloop()

if __name__ == '__main__':
   test()
