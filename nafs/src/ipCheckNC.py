# This code accepts a string input of ipv4 subnet and searches the hosts to find matching subnets and hosts
# The affected hosts are defined in the Basondole Tools device menu and are accessed via ssh using paramiko lib
# AUTHOR: Paul S.I. Basondole

import re
import sys
import time
import ipaddr
import ipaddress
import socket
import getpass
import smtplib
import paramiko
import datetime
import readline
import threading
from IPy import IP

from initial import getIpFromFile



def convertToCidr(key):
   if 'ip route vrf ' in key:
      keystriped= key.strip('ip route vrf ').split()
      pref = keystriped[1]+'/'+keystriped[2]
      pref = keystriped[1]+'/'+str(ipaddress.ip_network(unicode(pref, "utf-8"),strict=False)).split('/')[1]
      vrf = keystriped[0]
      keystriped.remove(keystriped[0])
      keystriped.remove(keystriped[0])
      keystriped.remove(keystriped[0])
      key = 'ip route vrf '+vrf+' '+str(pref)+' '+' '.join(keystriped)
      return key
   elif 'ip route 'in key:
      keystriped= key.strip('ip route ').split()
      pref = keystriped[0]+'/'+keystriped[1]
      pref = keystriped[0]+'/'+str(ipaddress.ip_network(unicode(pref, "utf-8"),strict=False)).split('/')[1]
      keystriped.remove(keystriped[0])
      keystriped.remove(keystriped[0])
      key = 'ip route '+str(pref)+' '+' '.join(keystriped)
      return key
   elif 'ip address ' in key:
      keystriped= key.strip('ip address ').split()
      pref = keystriped[0]+'/'+keystriped[1]
      pref = keystriped[0]+'/'+str(ipaddress.ip_network(unicode(pref, "utf-8"),strict=False)).split('/')[1]
      keystriped.remove(keystriped[0])
      keystriped.remove(keystriped[0])
      key = 'ip address '+str(pref)+' '+' '.join(keystriped)
      return key
   elif 'access-list ' in key:
      keystriped = key.split()
      end = []
      ip = keystriped[-2]
      wildcard = keystriped[-1]
      if re.findall(r'\d\..*\.\d',ip):
         for octate in range(4):
            end.append(str(int(ip.split('.')[octate])+int(wildcard.split('.')[octate])))
         pref = IP(ip+'-'+('.'.join(end)))
         keystriped.remove(keystriped[-1])
         keystriped.remove(keystriped[-1])
         key = ' '.join(keystriped)+' '+str(pref)
      else: key = key+'/32'
      return key
   elif re.findall(r'permit|deny',key):
      keystriped = key.split()
      end = []
      ip = keystriped[-2]
      wildcard = keystriped[-1]
      if re.findall(r'\d\..*\.\d',ip):
         for octate in range(4):
            end.append(str(int(ip.split('.')[octate])+int(wildcard.split('.')[octate])))
         pref = IP(ip+'-'+('.'.join(end)))
         keystriped.remove(keystriped[-1])
         keystriped.remove(keystriped[-1])
         key = ' '.join(keystriped)+' '+str(pref)
      else: key = key+'/32'
      return key
   else: return key


def parseCiscoOutput(loopbackIp,ipDict,output,subnet):
# commented lines can be uncomment to provide insight during troubleshooting

   global prefixMatch
   intprops = {}
   regex = r'^(interface|ip route|ip prefix-list|access-list|ip access-list)'
   for line in output.split('\n'):
      if re.findall(regex,line):
         intprops[line] = []
         interface = line
         continue
      try: intprops[interface].append(line)
      except UnboundLocalError: reason = 'the key is not an interface it has not values in its hierachy'
      except KeyError: reason = 'key is not in the dictionary'
   subnet = unicode(subnet, "utf-8")
   subnet = ipaddress.ip_network(subnet, strict = False)
   ipregex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}'

   for key in intprops.keys():
      #print key
      if re.findall(r'^ip route',key):
         #print key
         ''' convert doted decimal to cidr '''
         key = convertToCidr(key)
         #print key
         try:
            prefix = re.findall(ipregex,key)[0]
            prefix = unicode(prefix, "utf-8")
            if ipaddress.ip_network(prefix, strict = False).subnet_of(subnet):
              prefixMatch +=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
              prefixMatch +=": "+key+"\n"
         except (IndexError,TypeError): noipaddress = True
      elif 'ip prefix-list' in key:
         #print key
         try:
            prefix = re.findall(ipregex,key)[0]
            prefix = unicode(prefix, "utf-8")
            if ipaddress.ip_network(prefix, strict = False).subnet_of(subnet):
              prefixMatch +=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
              prefixMatch +=": "+key+"\n"
         except (IndexError,TypeError): noipaddress = True
      elif 'access-list' in key:
         if intprops[key]:
            for value in intprops[key]:
               value = convertToCidr(value)
               #print key,value
               try:
                  prefix = re.findall(ipregex,value)[0]
                  prefix = unicode(prefix, "utf-8")
                  if ipaddress.ip_network(prefix, strict = False).subnet_of(subnet):
                     prefixMatch +=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
                     prefixMatch +=": "+key+' '+value+"\n"
               except (IndexError,TypeError): noipaddress = True
         else:
            key = convertToCidr(key)
            #print key
            try:
               prefix = re.findall(ipregex,key)[0]
               prefix = unicode(prefix, "utf-8")
               if ipaddress.ip_network(prefix, strict = False).subnet_of(subnet):
                 #print key
                 prefixMatch +=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
                 prefixMatch +=": "+key+"\n"
            except (IndexError,TypeError): noipaddress = True
      else:
         for value in intprops[key]:
            if 'xconnect' in value or 'peer' in value: continue
            value = convertToCidr(value)
            #print key, value
            try:
               prefix = re.findall(ipregex,value)[0]
               prefix = unicode(prefix, "utf-8")
               #print prefix
               if ipaddress.ip_network(prefix, strict = False).subnet_of(subnet):
                  #print key, value
                  prefixMatch +=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
                  prefixMatch +=": "+key+' '+value+"\n"
            except (IndexError,TypeError): noipaddress = True
   return



def sshCheckSubnets(loopbackIp,ipDict,username,password,subnet,lock):
# commented lines can be uncomment to provide insight during troubleshooting

   global outputicheck
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #with lock: outputicheck+='\n'+ (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp)
   try:
      #with lock: outputicheck+='\n'+ (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password,timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except paramiko.AuthenticationException:
         authenticated = False
         with lock: outputicheck+='\n'+(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)
      if authenticated==True:
         #outputicheck+='\n'+(time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         deviceOutput = ''
         secureCli = sshClient.invoke_shell()
         if ipDict[loopbackIp][0] == 'juniper':
            secureCli.send('set cli screen-length 0 \n')
            secureCli.send('show configuration | display set | match "interfaces.*inet.*address" \n')
            secureCli.send('show configuration | display set | match routing-options.*static \n')
            secureCli.send('show configuration | display set | match policy-options.*route-filter \n')
            secureCli.send('show configuration | display set | match policy-options.*prefix-list |except statement \n')
            secureCli.send('quit\n')
            time.sleep(5)
            while True:
               cliOutput = secureCli.recv(65535)
               if not cliOutput: break
               for line in cliOutput:
                  deviceOutput += line
            sshClient.close
            parseJunosOutput(deviceOutput,ipDict,loopbackIp,subnet)
            #with lock:
               #if loopbackIp == 'put ip here' :print deviceOutput
         elif ipDict[loopbackIp][0] == 'cisco':
            secureCli.send("terminal length 0\n")
            secureCli.send("sh run | se ^interface\n")
            secureCli.send("sh run | se ^ip route\n")
            secureCli.send("sh run | se ^ip prefix-list\n")
            secureCli.send("sh run | se access-list\n")
            time.sleep(4)
            secureCli.send("quit\n")
            time.sleep(5)
            while True:
               cliOutput = secureCli.recv(65535)
               if not cliOutput: break
               for line in cliOutput:
                  deviceOutput += line
            #print deviceOutput
            sshClient.close()
         #with lock:
            #if loopbackIp == 'put ip here' :print deviceOutput
            parseCiscoOutput(loopbackIp,ipDict,deviceOutput,subnet)
            #with lock: print deviceOutput
   except socket.error:
      with lock: outputicheck+='\n'+(time.ctime()+" (user = "+username+") failed connection ip  > "+loopbackIp)


def parseJunosOutput(output,ipDict,loopbackIp,subnet):
   global prefixMatch
   intprops = {}
   regex = r'inet address|static route|route-filter|prefix-list'
   for line in output.split('\n'):
      if re.findall(regex,line):
         intprops[line.strip('set ')] = []
         interface = line.strip('set ')
         continue
      try: intprops[interface].append(line)
      except UnboundLocalError: reason = 'the key is not an interface it has not values in its hierachy'
      except KeyError: reason = 'not sure, bumped into it during testing'

   subnet = unicode(subnet, "utf-8")
   subnet = ipaddress.ip_network(subnet, strict = False)
   ipregex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}'

   for key in intprops.keys():
      try:
         prefix = re.findall(ipregex,key)[0]
         prefix = unicode(prefix, "utf-8")
         if prefix:
            if ipaddress.ip_network(prefix, strict = False).subnet_of(subnet):
              prefixMatch +=((ipDict[loopbackIp])[1]+'.'+(loopbackIp.split('.'))[-1]).ljust(20)
              prefixMatch +=": "+key+"\n"
      except IndexError: noipaddress = True

def ipCheck(username,password,subnet,ipDict):
      global outputicheck
      threads = []
      lock = threading.Lock()
      startTime = time.time()
      for loopbackIp in ipDict:
         loopbackIp=loopbackIp.strip()
         if not loopbackIp: continue
         process = threading.Thread(target=sshCheckSubnets, args=(loopbackIp,ipDict,username,password,subnet,lock))
         process.start()
         threads.append(process)
      for process in threads:
         process.join()
      outputicheck+= '\n'
      if not prefixMatch: outputicheck+='\n'+ "-----------------------------------------\nno match found subnet can be used"
      if prefixMatch:
         outputicheck+='\n'+ "Found used ipv4 addresses:\n--------------------------"
         intList = prefixMatch.split('\n')
         intList.sort()
         for item in intList: outputicheck+='\n'+item


def buttonicheck(username,password,ipDict,subnet):
   global outputicheck, prefixMatch
   prefixMatch = ''
   outputicheck = ''
   ipCheck(username,password,subnet,ipDict)
   buttonicheck = outputicheck
   prefixMatch = ''
   outputicheck = ''
   return buttonicheck



def test():

   def getUserDetails():
      alias = raw_input("Username: ")
      keylock = getpass.getpass()
      loopbackIp = "192.168.56.57"
      sshClient = paramiko.SSHClient()
      sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      try:
         sshClient.connect(loopbackIp, username=alias, password=keylock, timeout=10,allow_agent=False,look_for_keys=False)
         sshClient.close()
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
      print "-----------------------------------------"
      return alias, keylock

   def getSubnet():
      # below loop for verifying the input to be an ip address, there are better methods
      subnetValid = False
      while not subnetValid:
         try:
            subnet = raw_input("Enter Subnet: ")
            ip = unicode(subnet, "utf-8")
            ip = ipaddress.ip_network(ip, strict = False)
            subnetValid = True
         except ValueError: pass

      subnetmask = subnet.split(".")[3].split("/")[-1]
      prefix =subnet.split(".")[0]+"."+subnet.split(".")[1]+"."+subnet.split(".")[2]
      return subnet,prefix


   startTime = time.time()
   username,password = getUserDetails()
   subnet, prefix= getSubnet()
   ipDict = getIpFromFile(path='C:\Users\u\Desktop\PACOM')

   found = buttonicheck(username,password,ipDict,subnet)
   print found

   print ("\ncode runtime "+str(round(time.time()-startTime)))
   if raw_input("\nPress any key to exit"): sys.exit()


if __name__=='__main__':
   test()
