# This module is part of the core Basondole Tools
# This is an initializing module used to gather data about hosts and verify user credentials

import re
import time
import socket
import paramiko
import threading

def getIpFromFile(path=None):
   if path: routers = open(path+"\devices.bas","r")
   else:
      routers = open("devices.bas","r")
   ipDict={}
   for line in routers:
      try:
         ipDict[(re.findall(r'ipv4\=(\S+)',line))[0].strip()] = [(re.findall(r'vendor\=(\S+)',line))[0].strip(),
                                                                 (re.findall(r'hostname\=(\S+)',line))[0].strip()]
         if re.findall(r'logicalsys\=(\S+)',line):
            ipDict[(re.findall(r'ipv4\=(\S+)',line))[0].strip()].append(re.findall(r'logicalsys\=(\S+)',line)[0].strip())
      except IndexError: pass
   routers.close()
   return ipDict

def delEmptyLine(file):
   list = []
   list = file.split('\n')
   list.sort()
   cleanFile = ''
   for item in list:
     if item == '' : continue
     else: cleanFile+=item.strip()+'\n'
   return cleanFile.strip()

def verifyUser(username,password,server=None):
# commented lines can be uncommented to provide insight during debugging
    if server: loopbackIp = server
    else: loopbackIp = '192.168.56.57'  # used private server for testing
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #print (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp.rjust(15))
    try:
      #print (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp.rjust(15))
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         print(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp.rjust(15))
         return None
      if authenticated==True:
         #print(time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp.rjust(15))
         sshClient.close()
         return username,password
    except socket.error:
        print(time.ctime()+" (user = "+username+") failed to connect > "+loopbackIp.rjust(15))
        return None


def showInterfaces(username,password,ipDict):
# commented lines can be uncommented to provide insight during debugging
    intDict = {}
    def kazi(username,password,loopbackIp,ipDict,lock):
       sshClient = paramiko.SSHClient()
       sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       #with lock: print (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp.rjust(15))
       try:
         #with lock: print (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp.rjust(15))
         try:
            sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
            authenticated = True
         except (socket.error, paramiko.AuthenticationException):
            authenticated = False
            with lock: print(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp.rjust(15))
            with lock: intDict[loopbackIp] = ['Null']
         if authenticated==True:
            deviceOutput = ''
            #with lock: print(time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp.rjust(15))
            secureCli = sshClient.invoke_shell()
            if ipDict[loopbackIp][0] == 'juniper':
               secureCli.send('set cli screen-length 0\n')
               secureCli.send('set cli screen-width 0\n')
               secureCli.send('show interfaces terse | except "\.|^ "\nquit\n')
            elif ipDict[loopbackIp][0] == 'cisco':
               secureCli.send('terminal length 0\n')
               secureCli.send('terminal width 0\n')
               secureCli.send('show interfaces description | exclude \.\nquit\n')
            time.sleep(5)
            while True:
               output = secureCli.recv(65535)
               if not output: break
               for line in output: deviceOutput+=line
            #with lock: print deviceOutput
            with lock: confDict = {loopbackIp:[ipDict[loopbackIp][0],ipDict[loopbackIp][1],['show']]}
            with lock: intDict[loopbackIp]= (prepInt(username,modOutput(deviceOutput,confDict,loopbackIp)))
            sshClient.close()
       except socket.error:
           with lock: print(time.ctime()+" (user = "+username+") failed to connect > "+loopbackIp.rjust(15))
           with lock: intDict[loopbackIp] = ['Null']

    threads = []
    lock = threading.Lock()
    for loopbackIp in ipDict.keys():
         process = threading.Thread(target=kazi, args=(username,password,loopbackIp,ipDict,lock))
         process.start()
         threads.append(process)
    for process in threads:
         process.join()
    return intDict


def showPolicer(username,password,ipDict):
# commented lines can be uncommented to provide insight during debugging
    policerDict = {}
    def kazi(username,password,loopbackIp,ipDict,lock):
       sshClient = paramiko.SSHClient()
       sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       #with lock: print (time.ctime()+" (user = "+username+") initializing connection "+loopbackIp.rjust(15))
       try:
         #with lock: print (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp.rjust(15))
         try:
            sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
            authenticated = True
         except (socket.error, paramiko.AuthenticationException):
            authenticated = False
            with lock: print(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp.rjust(15))
            with lock: policerDict[loopbackIp] = ['Null']

         if authenticated==True:
            deviceOutput = ''
            #with lock: print(time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp.rjust(15))
            secureCli = sshClient.invoke_shell()
            if ipDict[loopbackIp][0] == 'juniper':
               secureCli.send('set cli screen-length 0\n')
               secureCli.send('set cli screen-width 0\n')
               try: secureCli.send('show configuration logical-system '+ipDict[loopbackIp][2]+' firewall | match ^policer\nquit\n')
               except IndexError: secureCli.send('show configuration firewall | match ^policer\nquit\n')
            elif ipDict[loopbackIp][0] == 'cisco':
               secureCli.send('set terminal length 0\n')
               secureCli.send('set terminal width 0\n')
               secureCli.send('show running-config | include ^policy-map\nquit\n')
            time.sleep(5)
            while True:
               output = secureCli.recv(65535)
               if not output: break
               for line in output: deviceOutput+=line
            #with lock: print deviceOutput
            with lock: confDict = {loopbackIp:[ipDict[loopbackIp][0],ipDict[loopbackIp][1],['show']]}
            with lock: policerDict[loopbackIp]= prepPolicer(ipDict,loopbackIp,modOutput(deviceOutput,confDict,loopbackIp))
            sshClient.close()
       except socket.error:
           with lock: print(time.ctime()+" (user = "+username+") failed to connect > "+loopbackIp.rjust(15))
           with lock: policerDict[loopbackIp] = ['Null']

    threads = []
    lock = threading.Lock()
    for loopbackIp in ipDict.keys():
         process = threading.Thread(target=kazi, args=(username,password,loopbackIp,ipDict,lock))
         process.start()
         threads.append(process)
    for process in threads:
         process.join()
    return policerDict


def prepInt(username,output):
    output.remove(output[0])
    output.remove(output[0])
    output.remove(output[-1])
    intList = []
    for interface in output: intList.append(interface.split()[0])
    return intList

def prepPolicer(ipDict,ip,output):
   policerList = []
   if ipDict[ip][0]== 'cisco': regex = r'^policy-map'
   if ipDict[ip][0]== 'juniper': regex = r'^policer'
   for item in output:
         if re.findall(regex,item):
            policerList.append(item.split()[1])
   return policerList


def modOutput(output,confDict,ipaddress):
# commented lines can be uncommented to provide insight during debugging
     newoutput = []
     CISCOEXEC = '#'#+commandList[0]
     CISCOUSER = '>'#+commandList[0]
     JUNIPEROP = '> '#+commandList[0][0]+commandList[0][1]
     LINUXUSER = '$ '#+commandList[0]
     LINUXROOT = '# '#+commandList[0]
     start = None
     end = None
     #print output
     outputList = output.split('\n')
     commandList = confDict[ipaddress][2]
     if confDict[ipaddress][0] == 'cisco':
        for line in outputList:
            if CISCOEXEC in line and commandList[0] in line:
               start=(line)
               break
            if CISCOUSER in line and commandList[0] in line:
               start=(line)
               break
     elif confDict[ipaddress][0] == 'juniper':
        for line in outputList:
            if JUNIPEROP in line and (commandList[0].split())[0] in line:
               start=(line)
               break
     elif confDict[ipaddress][0] == 'linux':
        for line in outputList:
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
     for line in range(outputList.index(start),outputList.index(end)):
        newoutput.append(outputList[line])
     return newoutput


def test():
   username = 'fisi'
   password = 'fisi123'
   ipDict = {'192.168.56.57':['juniper','hostname1'],'192.168.56.56':['cisco','hostname2']}
   if verifyUser(username,password):
        start = time.time()
        print showInterfaces(username,password,getIpFromFile())
        print showPolicer(username,password,getIpFromFile())
        print 'run-time', time.time()-start


if __name__=='__main__':
   test()
