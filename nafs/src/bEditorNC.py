# This code provides a means to manage the data file used by bBurst
# The data file will be stored on a server
# This code is used as a client to manage the file on the server
# AUTHOR: Paul S.I. Basondole

import re
import readline
import subprocess
import paramiko
import socket

from ClassDialog import Dialog
from initial import getIpFromFile
from initial import delEmptyLine

from ClassOutput import outputWin

# Variable for GUI elements
warning_icon = "C:\Users\u\Desktop\PACOM\icon\warning-icon.png"
cancel_icon = "C:\Users\u\Desktop\PACOM\icon\cancel-icon.png"


class Server():

   def __init__(self,server,FQP):
      self.server = server
      self.FQP = FQP
      sshClient = paramiko.SSHClient()
      sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      self.up = True
      try:
         sshClient.connect(self.server,timeout=10)
         sshClient.close()
      except socket.timeout:
         self.up = False
      except paramiko.ssh_exception.AuthenticationException: pass


   def retrieveRemoteFile(self,serverlogin):
      strfile = ''
      cmd = ['ssh', serverlogin+'@'+self.server, 'cat '+self.FQP]
      read = subprocess.Popen(cmd, stdout=subprocess.PIPE)
      for line in read.stdout: strfile+=line
      return strfile


   def saveRemoteFile(self,serverlogin,cleanFile):
      cmd = ['ssh', serverlogin+'@'+self.server, 'echo "'+cleanFile+'" > '+self.FQP]
      subprocess.Popen(cmd, stdout=subprocess.PIPE)
      return



class action():

   def __init__(self,server,serverlogin,FQP):
      self.server = server
      self.status = Server(self.server,FQP)
      self.login = serverlogin
      self.warning = warning_icon
      self.error = cancel_icon

   def add(self,parent,data):
      ip,interface,vlan = data[0], data[1], data[2]
      update = self.client(data)
      if self.status.up:
         clientList,removed = self.deleteClient(ip,interface,vlan)
         strfile = '\n'.join(clientList)
         if removed:
            proceed = Dialog(parent,prompt='Client alread exist in package \Proceed anyway? \n',
                             icon= self.warning)
            if procced.ans != 'ok': return

         else: proceed = Dialog(parent,prompt='Click ok to proceed \nor cancel to review \n',
                          icon=self.warning)
         if proceed.ans == 'ok':
            strfile+=update
            cleanFile = delEmptyLine(strfile)
            self.status.saveRemoteFile(self.login,cleanFile)
            Dialog(parent,prompt= 'Client file updated successfully\n')
      else: Dialog(parent,prompt='Can not access server \n'+self.server+' \n', icon=self.error)


   def remove(self,parent,data):
      ip,interface,vlan = data[0], data[1], data[2]

      if self.status.up:
         clientList,removed = self.deleteClient(ip,interface,vlan)
         if removed:
            proceed = Dialog(parent,prompt='Click ok to proceed \nor cancel to review \n',
                          icon=self.warning)
            strfile = '\n'.join(clientList)
            cleanFile = delEmptyLine(strfile)
            self.status.saveRemoteFile(self.login,cleanFile)
            Dialog(parent,prompt= 'Client file updated successfully\n',nobutton=True)

         else: Dialog(parent,prompt= '\nClient not found at '+ip+' interface '+interface+'.'+vlan)
      else: Dialog(parent,prompt='Can not access server \n'+self.server+' \n',icon=self.error)


   def update(self,parent,data):
      ip,interface,vlan = data[0], data[1], data[2]
      update = self.client(data)
      if self.status.up:
         clientList,removed = self.deleteClient(ip,interface,vlan)
         strfile = '\n'.join(clientList)
         strfile+=update
         cleanFile = delEmptyLine(strfile)
         self.status.saveRemoteFile(self.login,cleanFile)

         outputtext = ''
         outputtext+= '\n'
         outputtext+= 'Removed:'
         outputtext+= '--------'
         outputtext+= removed
         outputtext+= '\n'
         outputtext+= 'Added:'
         outputtext+= '------'
         outputtext+= update.strip()
         outputtext+= '\n'
         outputtext+= 'Client file updated successfully\n'

         output= outputWin()
         output.TB2('Vlan Finder',otputtext,parent,self)

      else: Dialog(parent,prompt='Can not access server \n'+self.server+' \n',icon=self.error)


   def view(self):
      if self.status.up:
         return self.status.retrieveRemoteFile(self.login)
      else: Dialog(parent,prompt='Can not access server \n'+self.server+' \n',icon=self.error)


   def deleteClient(self,ip,interface,vlan):
      regex = r'.*'+ip+'.*'+interface+'.*'+vlan
      clients = self.status.retrieveRemoteFile(self.login).split('\n')
      removed = ''
      index = []
      for line in clients:
         if re.match(regex,line):
            index.append(line)
      for line in index:
         clients.remove(line)
         removed+=line+'\n'
      return clients,removed

   def client(self,data):
      pe = 'pe='+data[0].ljust(15)
      interface = 'interface='+data[1].ljust(8)
      vlan = 'vlan='+data[2].ljust(4)
      daybandwidth = 'daybandwidth='+data[3].ljust(14)
      nightbandwidth = 'nightbandwidth='+data[4].ljust(14)
      starttime = 'starttime='+data[5].ljust(4)
      endtime = 'endtime='+data[6].ljust(4)
      days = 'days='+data[7].ljust(8)
      name= 'name='+data[8].replace(' ','-')
      client = '\n'+pe+'  '+interface+'  '+vlan+'  '+daybandwidth+'  '+nightbandwidth+'  '+starttime+'  '+endtime+'  '+days+'  '+name
      return client



def bEditorbutton(parent,serverlogin,server,FQP,choice,data):
   d= action(server,serverlogin,FQP)
   if choice == 'Add client' : d.add(parent,data)
   elif choice == 'Remove client': d.remove(parent,data)
   elif choice == 'Update client': d.update(parent,data)
   elif choice == 'View clients': d.view()
