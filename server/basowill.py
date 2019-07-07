#!/usr/bin/python
#Developed by Paul S.I. Basondole

import paramiko
import time
import re
import os
import sys
import socket
import getpass
import base64
import random
import threading
import Queue
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def inputstuff():
   try:
      try: commands = sys.argv[sys.argv.index("-commands")+1]
      except IndexError:
         print 'Specify commands example: basowilldo -commands "show system users:show system uptime"'
         sys.exit()
   except ValueError:
      try:
         try: commandsFile = sys.argv[sys.argv.index("-commandsFile")+1]
         except IndexError:
            print 'Specify commands file example: basowilldo -commandsFile mycommands.txt'
            sys.exit()
      except ValueError:
         print 'use [-commandsFile] followed by file name or'
         print 'use [-commands] followed by "command1:command2:etc", if more than one, commands are separated by :'
         print 'example: basowilldo -commands "show system users:show system uptime"'
         print 'example: basowilldo -commandsFile mycommands.txt'
         raw_input('NB: Use cmd to launch this tool with above options')
         sys.exit()
   try: ipaddress = sys.argv[sys.argv.index("-ipaddress")+1].strip()
   except (ValueError,IndexError):
      try:
         ipaddressFile = sys.argv[sys.argv.index("-ipaddressFile")+1]
      except (ValueError,IndexError):         
         print 'use [-ipaddress] to specify the host device or'
         print 'use [-ipaddressFile] followed by file name'
         print 'example: basowilldo -commands "show system users:show system uptime" -ipaddress 10.0.0.1'
         sys.exit()

   commandList = []
   try: commands = commands.split(":")
   except UnboundLocalError:
      commandFile = open(commandsFile)
      commands = commandFile
   if type(commands)==list:
      for command in commands:
         commands[commands.index(command)] = command.replace("'",'"')
   for line in commands:
      commandList.append(line)

   ipList = []
   try: ipList.append(ipaddress.strip())
   except UnboundLocalError:
      ipFile = open(ipaddressFile,'r')
      for line in ipFile:
         for item in line.split('\n'):
            if len(item)==0: continue
            ipList.append(item)
##   print commands, ipList
##   sys.exit()
   return commandList,ipList

def credentials(trial):
   def createLogin():
      ukey,username,key = encrypt(raw_input('Username: '))
      pkey,password,key = encrypt(getpass.getpass())
##      username = encrypt(bytes(str(username),'utf-8'))
##      password = encrypt(bytes(str(password),'utf-8'))
      mkfile = open('.basdoin','w')
      mkfile.write(key)
      mkfile.write(' ')
      mkfile.write('ux?/'+username)
      mkfile.write(' ')
      mkfile.write('kx!#'+password)
      mkfile.write(' ')
      mkfile.write('9$x!'+ukey)
      mkfile.write(' ')
      mkfile.write('Z@%*'+pkey)
      mkfile.close()
      return ukey,username,pkey,password
      
   if trial: ukey,username,pkey,password = createLogin()
   else:
      try:
         creds= open('.basdoin','r')
         for line in creds:
            try:
               username = re.findall(r'ux\?/(\S+)',line)[0]
               password = re.findall(r'kx\!\#(\S+)',line)[0]
               ukey = re.findall(r'9\$x\!(\S+)',line)[0]
               pkey= re.findall(r'Z\@\%\*(\S+)',line)[0]
               print ('')
               print ('INFO: username and password auto-retrieved')
            except IndexError: ukey,username,pkey,password = createLogin()

      except IOError: ukey,username,pkey,password = createLogin()
   try: ukey,username,pkey,password
   except UnboundLocalError: ukey,username,pkey,password = createLogin()
   return ukey,username,pkey,password



def verifyUser(ipaddress,trial):
   global returnQ
   ukey,username,pkey,password = credentials(trial)
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
##   if decrypt(ukey,username)==None:  ukey,username,pkey,password = credentials('Try')
         
##    print (time.ctime()+" (user = "+decrypt(ukey,username)+") initializing connection "+loopbackIp.rjust(15))
   try:
##         print (time.ctime()+" (user = "+decrypt(ukey,username)+") authentication starting " + ipaddress.ljust(15))
      try:
         sshClient.connect(ipaddress, username=decrypt(ukey,username), password=decrypt(pkey,password), timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         print(time.ctime()+" (user = "+decrypt(ukey,username)+") failed authentication > "+ipaddress.ljust(15))
         returnQ.put(None)
      if authenticated==True:
##            print(time.ctime()+" (user = "+decrypt(ukey,username)+") passed authentication > "+ipaddress.ljust(15))
         sshClient.close()
         returnQ.put('Success')
      return ukey,username,pkey,password
   except socket.error:
      print(time.ctime()+" (user = "+decrypt(ukey,username)+") failed to connect > "+ipaddress.ljust(15))
      returnQ.put('Failed connection')
   
      
   
def job(ukey,username,pkey,password):
   void,ipList = inputstuff()
    
   def kazi(ukey,username,pkey,password,ipaddress,lock,returnQ):
      commandList,xxx = inputstuff()
      sshClient = paramiko.SSHClient()
      sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
##      if not trial:
##         with lock: print ('')
##      if not trial:
##         with lock: print (time.ctime()+" (user = "+decrypt(ukey,username)+") initializing connection "+ipaddress.ljust(15))
      try:
##         if not trial:
##            with lock: print (time.ctime()+" (user = "+decrypt(ukey,username)+") authentication starting " + ipaddress.ljust(15))
         try:
            sshClient.connect(ipaddress, username=decrypt(ukey,username), password=decrypt(pkey,password), timeout=10,allow_agent=False,look_for_keys=False)
            authenticated = True
         except (socket.error, paramiko.AuthenticationException):
            authenticated = False
            with lock: print(time.ctime()+" (user = "+decrypt(ukey,username)+") failed authentication > "+ipaddress.ljust(15))
##            returnQ.put(None)

         if authenticated==True: 
##            if not trial:
##               with lock: print(time.ctime()+" (user = "+decrypt(ukey,username)+") passed authentication > "+ipaddress.ljust(15))
            deviceOutput = ''
            secureCli = sshClient.invoke_shell()
            time.sleep(0.1)
            secureCli.send('set cli screen-length 0\n')
            secureCli.send('terminal length 0\n')
            for line in commandList:
               secureCli.send(line)
               secureCli.send('\n')
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
##            print 'LENGTH ', len(outputList)
            sshClient.close()
            print('\n')
##            if len(outputList) < 5: time.sleep(5)
            with lock: print ('['+ipaddress+']')
##            print 'LENGTH ', len(outputList)
            ciscoexec = '#'#+commandList[0]
            ciscouser = '>'#+commandList[0]
            juniperoperator = '> '#+commandList[0][0]+commandList[0][1]
            linuxuser = '$ '#+commandList[0]
            linuxroot = '# '#+commandList[0]
##            print firstcommandc,firstcommandc2,firstcommandj
            start = None
            end = None
            for line in outputList:
               if ciscoexec in line and commandList[0] in line:
                  start=(line)
##                  print 'CISCOEXEC'
                  break
               if ciscouser in line and commandList[0] in line:
                  start=(line)
##                  print 'CISOUSER'
                  break
               if juniperoperator in line and (commandList[0].split())[0] in line:
                  start=(line)
##                  print 'JUNIPEROP',start
                  break
               if linuxuser in line and commandList[0] in line:
                  start=(line)
##                  print 'LINUXUSER',start
                  break
               if linuxroot in line and commandList[0] in line:
                  start=(line)
##                  print 'LINUXROOT',start
                  break
               
            for line in outputList:
               if re.findall(r'[>#$].*(quit|exit)',line):
                  end = (line)
##                  print 'END',line
                  break
               
##            print outputList.index(found)
##            count = 0
##            for line in outputList:
##               if firstcommandj in line :
##                  print breaking
##                  break
##               if not firstcommandc in line or not firstcommandj in line:
##                  count+=1
##                  outputList.remove(line)
##            print count
            if start==None:
               with lock: print 'Device is up but taking too long to respond'
            
            else:
               for line in range(outputList.index(start),outputList.index(end)):
##                  print line,outputList[line]
                  with lock: print '  ',outputList[line]

##            returnQ.put('Success')
      except TypeError:
         returnQ.put(None)


   global returnQ
   threads = []
   lock = threading.Lock()
   
   for ipaddress in ipList:
      t = threading.Thread(target=kazi, args=(ukey,username,pkey,password,ipaddress,lock,returnQ))
      t.start()
      threads.append(t)  
   for t in threads:
      t.join()
      

def encrypt(data):
   key = 'eeCCJ-A1Kazl55rohV4V1q0xC0xl1dOewxhHBaXo4DY='
   cipher_suite = Fernet(key)
   result = cipher_suite.encrypt(data)
   key=random.choice("0123456789abcde")+random.choice('*()^%$')+random.choice('ABCDEFGH')
   return key,base64.b64encode(base64.b64encode(data+key)+key)+key,result

def decrypt(key,data):
##   key = 'eeCCJ-A1Kazl55rohV4V1q0xC0xl1dOewxhHBaXo4DY='
##   cipher_suite = Fernet(key)
##   result = (cipher_suite.decrypt(data))
##   return bytes(result).decode("utf-8").strip()
   try: base64.b64decode(base64.b64decode(data.split(key)[0]).split(key)[0]).split(key)[0]
   except TypeError:
      try: os.remove('.basdoin')
      except WindowsError: deleted=True
      print 'INFO: Auto-retrieved login could not be decrypted, the login file has been tempered with'
      print 'INFO: Saved logins will now be destroyed'
      sys.exit('INFO: re-Run the command and enter credentials')
   return base64.b64decode(base64.b64decode(data.split(key)[0]).split(key)[0]).split(key)[0]
 

if __name__== "__main__":
   returnQ = Queue.Queue()
   commands,ipList = inputstuff()
##   job(None)
##   retry = returnQ.get()   
##   while retry==None:
##      job('Try')
##      retry = returnQ.get()
##      if retry == 'Failed connection': break
##      if retry == 'Success': break

   ukey,username,pkey,password = verifyUser(ipList[0].strip(),None)
   verified = returnQ.get()
   while verified==None:
      ukey,username,pkey,password =verifyUser(ipList[0].strip(),'try')
      verified = returnQ.get()
   if verified: job(ukey,username,pkey,password)

   print '\nINFO: Developed by Paul S.I. Basondole\n'
   
