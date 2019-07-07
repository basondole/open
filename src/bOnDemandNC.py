
# This code will create or delete shell scripts on a server
# These scripts will be used to change bandwidth configuration on routers on the specified date and time
# Task schedulrer used is linux 'at'
# The code can be ran from client or the server itself
# AUTHOR: Paul S.I. Basondole

import re
import time
import subprocess
import socket
import paramiko

from ClassDialog import Dialog

# variables for GUI icons
cancel_icon = "C:\Users\u\Desktop\PACOM\icon\cancel-icon.png"


class Server():

   def __init__(self,serverlogin,server,scriptPath,scriptname):
      self.server = server
      self.serverlogin = serverlogin
      self.scriptPath = scriptPath
      self.scriptname = scriptname
      sshClient = paramiko.SSHClient()
      sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      self.up = True

      try:
         sshClient.connect(self.server,timeout=10)
         sshClient.close()
      except socket.timeout:
         self.up = False
      except paramiko.ssh_exception.AuthenticationException: pass

   def revertJob(self,revertDate):
      cmd = ['ssh', self.serverlogin+'@'+self.server, 'at '+revertDate+' -f '+self.scriptPath+'/PendingTickets/'+self.scriptname+' &>> '+self.scriptPath+'/PendingTickets/'+self.scriptname+'\n']
      tsk = subprocess.Popen(cmd, stdin=subprocess.PIPE)


   def revertScript(self,task):
      cmd = ['ssh', self.serverlogin+'@'+self.server, 'echo "'+task+'" > '+self.scriptPath+'/PendingTickets/'+self.scriptname+'\n']
      tsk = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE)


   def retrieveRemoteFile(self,stdict=None,bigdict=None):
      strfile = ''
      cmd = ['ssh', self.serverlogin+'@'+self.server, 'cat '+self.scriptPath+'/PendingTickets/'+self.scriptname+'\n']
      read = subprocess.Popen(cmd, stdout=subprocess.PIPE)
      regex = self.scriptPath+r'/?/Logs/'+r'(\S+)'

      if stdict: sdict= {}
      if bigdict: bdict = {}

      sn = 1
      for line in read.stdout:
         if re.findall(regex,line):
            script = re.findall(regex,line)[0]
            strfile+='   '+str(sn).rjust(3)+'. '
            strfile+=script.split('.')[0]+'\n'
            sn+=1
            if bigdict:
               if re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',line):
                  bdict[script.split('.')[0]]=[re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',line)[0]]
               if re.findall(r'interface.(\S+)',line):
                  bdict[script.split('.')[0]].append(re.findall(r'interface.(\S+)',line)[0].split(':')[0].split('.')[0])
                  bdict[script.split('.')[0]].append(re.findall(r'interface.(\S+)',line)[0].split(':')[0].split('.')[1].strip())
               if re.findall(r'input.(\S+)',line):
                  bdict[script.split('.')[0]].append(re.findall(r'input.(\S+)',line)[0].split(':')[0].strip())

         elif re.findall(r'job.(\d+)',line):
            ''' if script was not defined from above it is corrupt '''
            try: script
            except NameError:
               script = 'Unknown Ticket'
               strfile+='   '+str(sn).rjust(3)+'. '
               strfile+=script.split('.')[0]+'\n'
               if bigdict: bdict[script.split('.')[0]] = []
               if stdict: sdict[script.split('.')[0]] = []
            strfile+='   '+' '.rjust(5)+line+'\n'
            if stdict: sdict[script.split('.')[0]]= re.findall(r'job.(\d+)',line)[0]
            if bigdict:
               date = line.split()[4],line.split()[5],line.split()[-1]
               bdict[script.split('.')[0]].append(re.findall(r'job.(\d+)',line)[0])
               bdict[script.split('.')[0]].append(date)

      if stdict: return sdict
      if bigdict:
         return bdict
      else: return strfile

   def deleteFromRemoteFile(self,scriptname,jobid):
      scriptname = scriptname.strip()+'.sh'
      task = 'rm '+self.scriptPath+'/PendingTickets/'+scriptname+'\natrm '+jobid+'\n'
      cmd = ['ssh', self.serverlogin+'@'+self.server, task]
      subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE)



def boDbutton(parent,serverlogin,server,FQP,data,commandList):

   pe = data[0]
   st = data[5]
   revertDate = data[6]

   stnumber = 'ST'+st.zfill(6)+'by'+parent.username
   scriptname = stnumber+'.sh'
   scriptPath = FQP

   error = cancel_icon

   commandStr = ':'.join(commandList)
   task = scriptPath+"/basowilldo.py -commands \'"+commandStr+"\' -ipaddress "+pe+" >"+scriptPath+"/Logs/"+stnumber+".log\nrm "+scriptPath+"/PendingTickets/"+scriptname

   status = Server(serverlogin,server,scriptPath,scriptname)

   if status.up:
      status.revertScript(task)
      time.sleep(2)
      status.revertJob(revertDate)
      time.sleep(1)
      return status.retrieveRemoteFile()
   else:
      Dialog(parent,prompt='Can not access server \n'+server+' \n',icon=error)
      return False

