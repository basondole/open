# This code accepts an interger input of vlan-id and searches the hosts to find matching interfaces
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
from initial import  getIpFromFile




def LoginGetDescription(loopbackIp,ipDict,vlan,username,password,lock):
# commented lines can be uncomment to provide insight during troubleshooting

   global outputvcheck
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp)
   try:
      #with lock: outputvcheck+='\n'+  (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)

      if authenticated==True:
         #with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         deviceOutput = ''
         cli = sshClient.invoke_shell()
         #with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") Gathering description > "+loopbackIp)
         if ipDict[loopbackIp][0] == 'juniper':
            cli.send("set cli screen-length 0 \n")
            cli.send('show interface description | match '+'"'+str(vlan)+' "\n')
            cli.send("quit\n")
         if ipDict[loopbackIp][0] == 'cisco':
            cli.send("terminal length 0 \n")
            cli.send("show interface description | include " +str(vlan)+"\n")
            cli.send("quit\n")
         time.sleep(5)
         while True:
            cliOutput = cli.recv(65536)
            if not cliOutput:
               break
            for line in cliOutput:
               deviceOutput+=(line)
         sshClient.close
         return deviceOutput
   except socket.error:
      with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)




def LoginGetTerse(loopbackIp,ipDict,vlan,username,password,lock):
# commented lines can be uncomment to provide insight during troubleshooting

   global outputvcheck
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #with lock: outputvcheck+='\n'+  (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp)
   try:
      #with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)

      if authenticated==True:
         #with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         deviceOutput = ''
         cli = sshClient.invoke_shell()
         #with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") checking vlan interface "+loopbackIp)
         if ipDict[loopbackIp][0] == 'juniper':
            cli.send("set cli screen-length 0 \n")
            cli.send('show interface terse | match '+'"\.'+str(vlan)+' "\n')
            cli.send("quit\n")
         if ipDict[loopbackIp][0] == 'cisco':
            cli.send("terminal length 0 \n")
            cli.send("show ip interface brief | include " +str(vlan)+"\n")
            cli.send("quit\n")
         time.sleep(5)
         while True:
            cliOutput = cli.recv(65536)
            if not cliOutput:
               break
            for line in cliOutput:
               deviceOutput+=(line)
         sshClient.close
         return deviceOutput
   except socket.error:
      with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)



def formatListItems(list):
   for line in list:
      list = line.rstrip()
      if list:
             yield list



def getIfName(loopbackIp,ipDict,vlan,match,username,password,lock):
   file = LoginGetDescription(loopbackIp,ipDict,vlan,username,password,lock)
   string = ""
   global descriptionv
   try:
      for line in file:
         string+=line
   except TypeError: filetype=None
   regex = r'^([ae|em|ge|xe|Gi|Fa|P|X|T].*)'
   found = 0

   def formatstuff(line):
      out = ''
      out += line.split()[0].ljust(14)
      for x in range(1,len(line.split())):
         out+= line.split()[x]+' '
      return out
   for item in match:
      for listItem in (string.split("\n")):
         if re.findall(regex,listItem):
            descriptionv+=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
            descriptionv+=(": ")
            descriptionv+=formatstuff(listItem)
            descriptionv+=("\n")
            found +=1
         elif (found == 0) and (listItem == (string.split("\n"))[-1]):
            descriptionv+=(loopbackIp).ljust(15)
            descriptionv+=(formatstuff(item)+": has no description")
            descriptionv+=("\n")


def getUsedVlan(loopbackIp,vlan,file):
   fileSplit = ''
   try:
      for line in file: fileSplit +=line
   except TypeError: match = False
   fileSplit = fileSplit.split("\n")
   usedVlans = []
   regex = r'^([ae|em|ge|xe|Gi|Fa].*)'
   match = False
   for line in fileSplit:
      if re.findall(regex,line):
         usedVlans.append(line)
      if usedVlans:
         match = usedVlans
   return  match



def kazi(loopbackIp,ipDict,vlan,username, password,lock):
   global vlans
   file = LoginGetTerse(loopbackIp,ipDict,vlan,username,password,lock)
   match = getUsedVlan(loopbackIp,vlan,file)
   if match:
      getIfName(loopbackIp,ipDict,vlan,match,username,password,lock)
      vlans+= str(loopbackIp).ljust(15)
      vlans+= (": has a match for VLAN ")
      vlans+= str(vlan)
      vlans+= ("\n")

def checkVlan(username,password,ipDict,vlan):

   global outputvcheck
   threads = []
   lock = threading.Lock()
   for loopbackIp in ipDict:
      t = threading.Thread(target=kazi, args=(loopbackIp,ipDict,vlan,username,password,lock))
      t.start()
      threads.append(t)
   for t in threads:
      t.join()
   if vlans:
      outputvcheck+= ("\n\nMATCHES:\n--------\n\n")
      if descriptionv: outputvcheck+= (descriptionv)
   else: outputvcheck+= ("\n\nMATCHES:\n---------\n\nno match found")


def buttonvcheck(username,password,ipDict,vlan):
   global outputvcheck, vlans, descriptionv
   vlans = ''
   outputvcheck = ''
   descriptionv = ''
   checkVlan(username,password,ipDict,vlan)
   buttonvcheck = outputvcheck
   vlans = ''
   outputvcheck = ''
   return buttonvcheck




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

   def getVlanId():
      print ("-------------------------------------------------------")
      vlan = raw_input("Enter the vlan to check : ")
      print ("-------------------------------------------------------")
      while int(vlan) not in range(1,4095):
         vlan = raw_input("enter the vlan to check : ")
         print ("-------------------------------------------------------")
      popDict= getIpFromFile()
      return popDict, vlan


   startTime = time.time()
   username, password = getUserDetails()
   ipDict, vlan = getVlanId()
   print (buttonvcheck(username,password,ipDict,vlan))
   print ("\ncode runtime "+str(round(time.time()-startTime)))
   if raw_input("\nPress any key to exit"): sys.exit()


if __name__=="__main__":
   test()
