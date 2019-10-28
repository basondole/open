# This code accepts two hosts and their respective interface names for input
# and finds common unused vlans from the two hosts' interfaces (as sub-intefaces)
# The affected hosts are accessed via ssh using paramiko lib
# AUTHOR: Paul S.I. Basondole

from __future__ import print_function
import os
import re
import sys
import time
import Queue
import socket
import getpass
import readline
import paramiko
import datetime
import threading
from initial import getIpFromFile



def makePort(interface):
   port = ''
   for x in range(len(re.findall(r'[0-9]',interface))):
      port += re.findall(r'[0-9]',interface)[x]
      if x==0 or x==1: port += '/'
   return port


def LoginGetTerse(loopbackIp,ipDict,interface,username,password,lock):
# commented lines can be uncomment to provide insight during troubleshooting

   global outputvfinderdx
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #with lock: outputvfinderdx+='\n'+ (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp)
   try:
      #with lock: outputvfinderdx+='\n'+ (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         outputvfinderdx+='\n'+(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)

      if authenticated==True:
         #with lock: outputvfinderdx+='\n'+(time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         deviceOutput = ''
         cli = sshClient.invoke_shell()
         #with lock: outputvfinderdx+='\n'+(time.ctime()+" (user = "+username+") Gathering details.... > "+loopbackIp)
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
         sshClient.close
         return deviceOutput
   except socket.error:
      with lock: outputvfinderdx+='\n'+(time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)




def getUsedVlan(loopbackIp,ipDict,interface,deviceOutput):

   global outputvfinderdx
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
         outputvfinderdx+='\n'+ (loopbackIp+': ['+interface+']')
         outputvfinderdx+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")
         return None
      except NameError: pass

   return usedVlans


def findAllFreeVlan(loopbackIp,interface,usedVlans):

   global outputvfinderdx
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
      outputvfinderdx+='\n'+ (loopbackIp+': ['+interface+']')
      outputvfinderdx+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")
   else:
      try:
         counter-=1
      except NameError:
         outputvfinderdx+='\n'+ (loopbackIp+': ['+interface+']')
         outputvfinderdx+='\n'+ ("all Vlans are used, no free Vlan")

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


def vlanFinder(loopbackIp,ipDict,interface,username,password,outputQ,lock):
   global outputvfinderdx
   deviceOutput = LoginGetTerse(loopbackIp,ipDict,interface,username,password,lock)
   usedVlans = getUsedVlan(loopbackIp,ipDict,interface,deviceOutput)
   if usedVlans :
      freeVlans = findAllFreeVlan(loopbackIp,interface,usedVlans)
      outputQ.put(freeVlans)
   else: return None



def makeAllFreeMatchingVlans(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB):
   global outputvfinderdx
   if len(freeVlansFromPeA) == 4094:
      outputvfinderdx+= '\n'+ (loopbackIpPeA+': ['+interfacePeA+']')
      outputvfinderdx+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")

   if len(freeVlansFromPeB) == 4094:
      outputvfinderdx+= '\n'+ (loopbackIpPeB+': ['+interfacePeB+']')
      outputvfinderdx+='\n'+ ("is not tagged, all Vlans are available if you intend to tag\n")

   outputvfinderdx+='\n'
   outputvfinderdx+='\n'+ ("Free Vlans:")
   outputvfinderdx+='\n'+ ("-----------")

   foundMatchingFreeVlans = []

   if len(freeVlansFromPeA) >= len(freeVlansFromPeB):
      for vlan in freeVlansFromPeA:
         if vlan in freeVlansFromPeB:
            foundMatchingFreeVlans.append(vlan)
   else:
      for vlan in freeVlansFromPeB:
         if vlan in freeVlansFromPeA:
            foundMatchingFreeVlans.append(vlan)

   return foundMatchingFreeVlans

def makeAllFreeMatchingVlansList(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB):
   foundMatchingFreeVlans = []
   if len(freeVlansFromPeA) >= len(freeVlansFromPeB):
      for vlan in freeVlansFromPeA:
         if vlan in freeVlansFromPeB:
            foundMatchingFreeVlans.append(vlan)
   else:
      for vlan in freeVlansFromPeB:
         if vlan in freeVlansFromPeA:
            foundMatchingFreeVlans.append(vlan)
   return foundMatchingFreeVlans


def AllFreeVlans(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB):
   global outputvfinderdx
   foundMatchingFreeVlans = makeAllFreeMatchingVlans(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB)
   formatedRangeVlan, formatedNoRangeVlan = groupVlans(foundMatchingFreeVlans)
   outputvfinderdx+='\n'+ (formatedNoRangeVlan)
   outputvfinderdx+='\n'+ ("")
   outputvfinderdx+='\n'+ (formatedRangeVlan)
   total = len(foundMatchingFreeVlans)
   if total > 4094: total = 4094
   outputvfinderdx+='\n'+ ("\n\nTotal number of unused VLANS is "+str(total))



def FreeVlanInRange(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB,startNumber,endNumber):

   global outputvfinderdx
   foundMatchingFreeVlans = makeAllFreeMatchingVlans(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB)
   vlanCount = []
   for vlan in foundMatchingFreeVlans:
      if vlan in range(startNumber,endNumber+1):
         vlanCount.append(vlan)
   formatedRangeVlan, formatedNoRangeVlan = groupVlans(vlanCount)

   outputvfinderdx+='\n'+ (formatedNoRangeVlan)
   outputvfinderdx+='\n'+ ("")
   outputvfinderdx+='\n'+ (formatedRangeVlan)

   if len(vlanCount)==0:
      outputvfinderdx+='\n'+'\n'+("none")

   outputvfinderdx+='\n'+ ("\n\nTotal number of unused VLANS in range "+str(len(vlanCount)))


def vlanFinderDualPes(username, password,loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB, ipDict,search,startNumber,endNumber):

      outputQA = Queue.Queue()
      outputQB = Queue.Queue()
      loopbacks = {1:loopbackIpPeA,
                   2:loopbackIpPeB}
      threads = []
      lock = threading.Lock()
      for key in loopbacks.keys():
         if key == 1:
            loopbackIp = loopbacks[key]
            interface = interfacePeA
            outputQ = outputQA
         if key == 2:
            loopbackIp = loopbacks[key]
            interface = interfacePeB
            outputQ = outputQB
         t = threading.Thread(target=vlanFinder, args=(loopbackIp,ipDict,interface,username,password,outputQ,lock,))
         t.start()
         threads.append(t)
      for t in threads:
         t.join()
      if outputQA and outputQB:
         freeVlansFromPeA = outputQA.get()
         freeVlansFromPeB = outputQB.get()
         if search == 'list':
            freevlans = makeAllFreeMatchingVlansList(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB)
            return freevlans
         if search == 'vall': AllFreeVlans(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB)
         elif search == 'vrange': FreeVlanInRange(loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB,freeVlansFromPeA,freeVlansFromPeB,startNumber,endNumber)


def buttonvfinderdx(username, password,loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB, ipDict,search,startNumber,endNumber):
   global outputvfinderdx
   outputvfinderdx = ''
   vlanFinderDualPes(username, password,loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB, ipDict,search,startNumber,endNumber)
   buttonvfinderdx = outputvfinderdx
   outputvfinderdx = ''
   return buttonvfinderdx



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


   def getDetailsForBothPes():
      print ("\n-------------------------------------------------------")
      print ("Enter the details for point A")
      loopbackIpPeA,ipDict,interfacePeA = getIpandInterfaceFromUser()
      print ("\n")
      print ("Enter the details for point B")
      loopbackIpPeB,ipDict,interfacePeB =  getIpandInterfaceFromUser()
      return loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB, ipDict


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
   username, password = getUserDetails()
   loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB, ipDict = getDetailsForBothPes()
   search = getVlanTaskSelector()
   if search == 'vrange': startNumber,endNumber = getRange()
   else: startNumber,endNumber = None,None
   print (buttonvfinderdx(username, password,loopbackIpPeA, interfacePeA, loopbackIpPeB, interfacePeB, ipDict,search,startNumber,endNumber))

   print ("\ncode runtime "+str(round(time.time()-startTime)))
   if raw_input("\nPress any key to exit"): sys.exit()



if __name__=="__main__":
    test()
