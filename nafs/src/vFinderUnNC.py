# This code accepts host ip and interface name for input and finds unused vlans from the interface (as sub-intefaces)
# The affected host is accessed via ssh using paramiko lib
# AUTHOR: Paul S.I. Basondole

from __future__ import print_function
import os
import re
import sys
import time
import readline
import socket
import getpass
import paramiko
import datetime
from initial import getIpFromFile



def makePort(interface):
   port = ''
   for x in range(len(re.findall(r'[0-9]',interface))):
      port += re.findall(r'[0-9]',interface)[x]
      if x==0 or x==1: port += '/'
   return port


def LoginGetTerse(loopbackIp,ipDict,interface,username,password):
# commented lines can be uncomment to provide insight during troubleshooting

   global outputvfinderun
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #outputvfinderun+='\n'+ (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp)
   try:
      #outputvfinderun+='\n'+ (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         try: outputvfinderun+= '\n'+(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)
         except NameError: print ('\n'+(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp))

      if authenticated==True:
         #outputvfinderun+='\n'+(time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         deviceOutput = ''
         cli = sshClient.invoke_shell()
         #outputvfinderun+='\n'+(time.ctime()+" (user = "+username+") Gathering details.... > "+loopbackIp)
         if ipDict[loopbackIp][0] == 'juniper':
            cli.send("set cli screen-length 0 \n")
            cli.send("show interface terse | match "+interface+"\n")
            cli.send("quit\n")
         if ipDict[loopbackIp][0] == 'cisco':
            cli.send("terminal length 0 \n")
            cli.send("show ip interface brief | include " +makePort(interface)+"\.\n")
            cli.send("quit\n")
         time.sleep(5)
         while True:
            cliOutput = cli.recv(65536)
            if not cliOutput:
               break
            for line in cliOutput:
               deviceOutput+=(line)
         #print (deviceOutput)
         sshClient.close()
         return deviceOutput
   except socket.error:
      try: outputvfinderun+='\n'+(time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)
      except NameError: print ('\n'+(time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp))


def getUsedVlan(loopbackIp,ipDict,interface,deviceOutput):
   global outputvfinderun
   file = deviceOutput.split('\n')
   usedVlans = []
   if ipDict[loopbackIp][0] == 'juniper': regex = re.escape(interface) + r'\.(\S+)'
   if ipDict[loopbackIp][0] == 'cisco':regex = re.escape(makePort(interface)) + r'\.(\S+)'
   for line in file:
      vlantag = re.findall(regex,line)
      for vlan in vlantag:
         usedVlans.append(vlan.strip())
   if len(usedVlans)==0:
      try:
         outputvfinderun+='\n'+ (loopbackIp+': ['+interface+']')
         outputvfinderun+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")
         return None
      except NameError: pass

   return usedVlans

def LoginGetDescription(loopbackIp,ipDict,interface,username,password):
# commented lines can be uncomment to provide insight during troubleshooting

   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp)
   try:
      #outputvcheck+='\n'+  (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=4,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         try: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)
         except NameError: print ('\n'+ (time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp))

      if authenticated==True:
         #outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         deviceOutput = ''
         cli = sshClient.invoke_shell()
         #with lock: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") Gathering description > "+loopbackIp)
         if ipDict[loopbackIp][0] == 'juniper':
            cli.send("set cli screen-length 0 \n")
            cli.send('show interface description | match '+str(interface)+'\n')
            cli.send("quit\n")
         if ipDict[loopbackIp][0] == 'cisco':
            cli.send("terminal length 0 \n")
            cli.send("show interface description | include " +str(interface)+"\n")
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
      try: outputvcheck+='\n'+ (time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)
      except NameError: print ('\n'+ (time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)) 


def getUsedVlanDesc(loopbackIp,ipDict,interface,username,password):
   deviceOutput = LoginGetDescription(loopbackIp,ipDict,interface,username,password)
   file = deviceOutput.split('\n')
   usedVlans = {}
   if ipDict[loopbackIp][0] == 'juniper': regex = re.escape(interface) + r'\.(\S+)'
   if ipDict[loopbackIp][0] == 'cisco':regex = re.escape(makePort(interface)) + r'\.(\S+)'
   for line in file:
      if re.findall(regex,line):
         desc = line.split()
         desc.remove(desc[0])
         desc.remove(desc[0])
         desc.remove(desc[0])
         usedVlans[(re.findall(regex,line)[0].strip())]= ' '.join(desc)
   return usedVlans



def findAllFreeVlan(loopbackIp,interface,usedVlans):
   global outputvfinderun
   freeVlans = []
   if int(usedVlans[0])>1:
      for freeVlanPrefix in range(1,int(usedVlans[0])):
         freeVlans.append(freeVlanPrefix)

   for vlan in range(len(usedVlans)):
      if int(usedVlans[vlan])-int(usedVlans[vlan-1]) > 1:
         diff = int(usedVlans[vlan])-int(usedVlans[vlan-1])
         counter = 0
         while diff != 1:
            diff -=1
            counter +=1
            if int(usedVlans[vlan-1])+counter <= 4094:
               freeVlans.append(int(usedVlans[vlan-1])+counter)

   if int(usedVlans[len(usedVlans)-1]) <= 4094:
      for freeVlanSufix in range(int(usedVlans[len(usedVlans)-1])+1,4094+1):
         freeVlans.append(freeVlanSufix)
   elif int(usedVlans[0]) > 4094:
      outputvfinderun+='\n'+ (loopbackIp+': ['+interface+']')
      outputvfinderun+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")
   else:
      try:
         counter-=1
      except NameError:
         outputvfinderun+='\n'+ (loopbackIp+': ['+interface+']')
         outputvfinderun+='\n'+ ("all Vlans are used, no free Vlan")

   return freeVlans


def groupVlans(freeVlans):
   tempdic={}
   for vlan in freeVlans:
      if vlan-1 in tempdic:
         tempdic[vlan-1]= vlan
      elif vlan-1 in tempdic.values():
         for key in tempdic.keys():
            if vlan-1==tempdic[key]:
               foundkey = key
         tempdic[foundkey]=vlan
      else:
         tempdic[vlan]=0
   keylist = sorted(tempdic)
   noRangeVlan = []
   rangeVlan = []
   for key in keylist:
      if tempdic[key] > 0:
         if tempdic[key] > 4094: tempdic[key] = 4094
         rangeVlan.append("["+(str(key)).rjust(4)+"-"+(str(tempdic[key])).ljust(4)+"]")
      else:
         noRangeVlan.append((str(key)).ljust(4))

   formatedRangeVlan = ""
   column = 0
   for vRange in rangeVlan:
      formatedRangeVlan +=(vRange+" ")
      column +=1
      if column%6==0:
         formatedRangeVlan +=("\n")

   column = 0
   formatedNoRangeVlan = ""
   for noVRange in noRangeVlan:
      formatedNoRangeVlan +=(noVRange+" ")
      column +=1
      if column%14==0:
         formatedNoRangeVlan +=("\n")

   return formatedRangeVlan, formatedNoRangeVlan


def vlanFinder(loopbackIp,ipDict,interface,username,password,):
   deviceOutput = LoginGetTerse(loopbackIp,ipDict,interface,username,password)
   usedVlans = getUsedVlan(loopbackIp,ipDict,interface,deviceOutput)
   if usedVlans:
      freeVlans = findAllFreeVlan(loopbackIp,interface,usedVlans)
      return freeVlans
   else:
      freeVlans = []
      for x in range(1,4095): freeVlans.append(x)
      return freeVlans



def makeAllFreeVlan(loopbackIp,interface,freeVlans):
   global outputvfinderun
   if len(freeVlans) == 4094:
      outputvfinderun+='\n'+ (loopbackIp+': ['+interface+']')
      outputvfinderun+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")

   outputvfinderun+='\n'
   outputvfinderun+='\n'+ ("Free Vlans:")
   outputvfinderun+='\n'+ ("-----------")
   formatedRangeVlan, formatedNoRangeVlan = groupVlans(freeVlans)
   outputvfinderun+='\n'+ (formatedNoRangeVlan)
   outputvfinderun+='\n'+ ("")
   outputvfinderun+='\n'+ (formatedRangeVlan)
   total = len(freeVlans)
   if total > 4094:  total = 4094
   outputvfinderun+='\n'+ ("\n\nTotal number of unused VLANS is "+str(total))



def makeFreeVlanInRange(loopbackIp,interface,freeVlans,startNumber,endNumber):
   global outputvfinderun
   if len(freeVlans) == 4094:
      outputvfinderun+='\n'+ (loopbackIp+': ['+interface+']')
      outputvfinderun+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")

   outputvfinderun+='\n'+ ("Free Vlans:")
   outputvfinderun+='\n'+ ("-----------")

   vlanCount = []
   for vlan in freeVlans:
      if vlan in range(startNumber,endNumber+1):
         vlanCount.append(vlan)
   formatedRangeVlan, formatedNoRangeVlan = groupVlans(vlanCount)

   outputvfinderun+='\n'+ (formatedNoRangeVlan)
   outputvfinderun+='\n'+ ("")
   outputvfinderun+='\n'+ (formatedRangeVlan)

   if len(vlanCount)==0:
      outputvfinderun+='\n'+'\n'+("none")

   outputvfinderun+='\n'+ ("\n\nTotal number of unused VLANS in range "+str(len(vlanCount)))



def vlanFinderSinglePe(username,password,loopbackIp,ipDict,interface,search,startNumber,endNumber):
      freeVlans = vlanFinder(loopbackIp,ipDict,interface,username,password)
      if freeVlans :
         if search == 'vall': makeAllFreeVlan(loopbackIp,interface,freeVlans)
         if search == 'vrange': makeFreeVlanInRange(loopbackIp,interface,freeVlans,int(startNumber),int(endNumber))


def buttonvfinderun(username,password,loopbackIp,ipDict,interface,search,startNumber,endNumber):
   global outputvfinderun
   outputvfinderun = ''
   vlanFinderSinglePe(username,password,loopbackIp,ipDict,interface,search,startNumber,endNumber)
   buttonvfinderdx = outputvfinderun
   outputvfinderun = ''
   return buttonvfinderdx



def test():

   def getUserDetails():
      alias = raw_input("Username: ")
      keylock = getpass.getpass()
      loopbackIp = "192.168.56.36"
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
               sshClient.close()
               authenticated = True
            except (socket.error, paramiko.AuthenticationException):
               authenticated = False
               print ("-------------------------------------------------------")
               print(time.ctime()+" (user = "+alias+") failed authentication")
         else:
            sys.exit("\n            --- EXITING ---\n")

      return alias, keylock


   def getIpandInterfaceFromUser():
      ipDict=getIpFromFile()
      print ("-------------------------------------------------------")
      print ("\n")
      print ("           * Specify the pe loopback address *")
      print ("\n")
      print ("-------------------------------------------------------") 
      loopbackIp= raw_input("enter the loopback address : ")
      print ("-------------------------------------------------------")
      while (loopbackIp not in ipDict):
         print ("unknown loopback address")
         print ("-------------------------------------------------------")
         loopbackIp= raw_input("enter PE Loopback address : ")
         print ("-------------------------------------------------------")
      print ("\n")
      print (" * Choose the interface by typing the interface name *")
      print ("\n")
      print ("           example: xe-0/1/3, ge-0/0/3 etc")
      print ("\n")
      print ("-------------------------------------------------------")
      interface = raw_input("enter interface to find vlan from : ")
      print ("-------------------------------------------------------")
      while len(interface) !=8 and len(interface) !=7 and len(interface)!=3:
         print ("Interface name is incorect, please retype")
         interface = raw_input("enter interface to find vlan from : ")
         print ("-------------------------------------------------------")
      return loopbackIp,ipDict,interface


   def getVlanTaskSelector():
      print ("-------------------------------------------------------")
      print ("\n")
      print ("         * Specify vlan search mode *")
      print ("\n")
      print ("      1. List all available free vlans")
      print ("      2. List availabe vlans from a specific range")
      print ("\n")
      print ("     At any time press Ctrl+C to exit the programm")
      print ("\n")
      print ("-------------------------------------------------------")
      job = raw_input("Enter your choice in number ie 1 or 2 : ")
      print ("-------------------------------------------------------")
      job =int(job)
      while job not in (1,2):
         print ("Error:",job,"is not a valid option")
         print ("-------------------------------------------------------")
         job = raw_input("Enter your choice in numbers ie 1 or 2 : ")
         job =int(job)
         print ("-------------------------------------------------------")
      print ("\n")
      if job == 1: return 'vall'
      if job == 2: return 'vrange'


   def getRange():
      startNumber = raw_input ("enter the start point of range : ")
      startNumber = int(startNumber)
      print ("-------------------------------------------------------")
      while startNumber not in range(1,4095):
         print ("invalid input, choose 1 - 4094")
         startNumber = raw_input ("enter the start point of range : ")
         print ("-------------------------------------------------------")
         startNumber = int(startNumber)
      endNumber = raw_input ("enter the end point of range : ")
      print ("-------------------------------------------------------")
      endNumber = int(endNumber)
      while endNumber not in range(1,4095):
         print ("invalid input, choose 1 - 4094")
         endNumber = raw_input ("enter the end point of range : ")
         print ("-------------------------------------------------------")
         endNumber = int(endNumber)
      while endNumber < startNumber:
         print ("invalid input, end point must be greater than starpoint")
         endNumber = raw_input ("enter the end point of range : ")
         print ("-------------------------------------------------------")
         endNumber = int(endNumber)
      print ("\n")
      return startNumber,endNumber


   startTime = time.time()
   username,password = getUserDetails()
   loopbackIp,ipDict,interface = getIpandInterfaceFromUser()
   search = getVlanTaskSelector()
   if search == 'vrange': startNumber,endNumber = getRange()
   else: startNumber,endNumber = None,None

   print (buttonvfinderun(username,password,loopbackIp,ipDict,interface,search,startNumber,endNumber))

   print ("\ncode runtime "+str(round(time.time()-startTime)))
   if raw_input("\nPress any key to exit"): sys.exit()



if __name__=="__main__":
   test()
