# This code accepts a string input of description and searches the hosts to find matching interface description
# The affected hosts are defined in the Basondole Tools device menu and are accessed via ssh using paramiko lib
# AUTHOR: Paul S.I. Basondole

from __future__ import print_function
import re
import os
import sys
import time
import socket
import getpass
import paramiko
import datetime
import threading
from initial import getIpFromFile




def LoginGetDescription(loopbackIp,ipDict,name,username,password,lock):
# commented lines can be uncomment to provide insight during troubleshooting

   global outputdcheck
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #with lock: outputdcheck+='\n'+ print (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp)
   try:
      #with lock: outputdcheck+='\n'+ print (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         with lock: outputdcheck+='\n'+ (time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)
      if authenticated==True:
         #with lock: outputdcheck+='\n'+ (time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         deviceOutput = ''
         cli = sshClient.invoke_shell()
         #with lock: outputdcheck+='\n'+ (time.ctime()+" (user = "+username+") Gathering description > "+loopbackIp)
         if ipDict[loopbackIp][0] == 'juniper':
            cli.send("set cli screen-length 0 \n")
            cli.send('show interface description | match '+'"'+name+'"\n')
            cli.send("quit\n")
         if ipDict[loopbackIp][0] == 'cisco':
            cli.send("terminal length 0 \n")
            cli.send('show interface description | include ' +name.capitalize()+'|'+name.upper()+'|'+name.lower()+'|'+name+"\n")
            cli.send("quit\n")
         time.sleep(5)
         while True:
            cliOutput = cli.recv(65536)
            if not cliOutput:
               break
            for line in cliOutput:
               deviceOutput+=(line)
         sshClient.close
         #print (deviceOutput)
         return deviceOutput
   except socket.error:
      with lock: outputdcheck+='\n'+ (time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)


def getIfName(loopbackIp,ipDict,name,username,password,lock):
   file = LoginGetDescription(loopbackIp,ipDict,name,username,password,lock)
   string = ""
   global descriptiond
   try:
      for line in file:
         string+=line
   except TypeError: filetype=None
   def formatstuff(line):
      out = ''
      out += line.split()[0].ljust(14)
      for x in range(1,len(line.split())):
         out+= line.split()[x]+' '
      return out
   regex = r'^([aegxGFPXT].*)'
   for listItem in (string.split("\n")):
      if re.findall(regex,listItem):
         with lock:
            descriptiond+=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
            descriptiond+=(": ")
            descriptiond+=formatstuff(listItem)
            descriptiond+=("\n")


def checkDesc(username,password,ipDict,name):
      global outputdcheck
      threads = []
      lock = threading.Lock()
      for loopbackIp in ipDict:
         t = threading.Thread(target=getIfName, args=(loopbackIp,ipDict,name,username, password,lock))
         t.start()
         threads.append(t)
      for t in threads:
         t.join()
      if descriptiond:
         outputdcheck+='\n'+ ("\nMATCHES:\n--------\n")
         descList = descriptiond.split('\n')
         descList.sort()
         for item in descList: outputdcheck+='\n'+ (item)
      else: outputdcheck+='\n'+ ("\nMATCHES:\n--------\nno match found")


def buttondcheck(username,password,ipDict,name):
   global outputdcheck, descriptiond
   descriptiond = ''
   outputdcheck = ''
   checkDesc(username,password,ipDict,name)
   buttondcheck = outputdcheck
   descriptiond = ''
   outputdcheck = ''
   return buttondcheck




def test():

   def getUserDetails():
      alias = raw_input("Username: ")
      keylock = getpass.getpass()
      loopbackIp = "192.168.56.57"
      sshClient = paramiko.SSHClient()
      sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      try:
         sshClient.connect(loopbackIp, username=alias, password=keylock, timeout=4)
         sshClient.close
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         print ("-------------------------------------------------------")
         print(time.ctime()+" (user = "+alias+") failed authentication")
      while not authenticated:
         print ("-------------------------------------------------------")
         action = raw_input('Enter 1 to re-try else quit :')
         if action=="1":
            print ("-------------------------------------------------------")
            alias = raw_input("Username: ")
            keylock = getpass.getpass()
            try:
               sshClient.connect(loopbackIp, username=alias, password=keylock, timeout=4)
               sshClient.close
               authenticated = True
            except (socket.error, paramiko.AuthenticationException):
               authenticated = False
               print ("-------------------------------------------------------")
               print(time.ctime()+" (user = "+alias+") failed authentication")
         else:
            quit()
            sys.tracebacklimit = 0
            raise Exception('Exit by user')

      return alias, keylock

   def getName():
      print ("-------------------------------------------------------")
      name = raw_input("Enter the name to check : ")
      print ("-------------------------------------------------------")
      name = re.escape(name)
      popDict= getIpFromFile()
      return popDict, name


   startTime = time.time()
   username, password = getUserDetails()
   ipDict,name = getName()

   found = buttondcheck(username,password,ipDict,name)
   print (found)

   print ("\ncode runtime "+str(round(time.time()-startTime)))
   if raw_input("\nPress any key to exit"): sys.exit()


if __name__=="__main__":
   test()
