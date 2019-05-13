# This module is part of the core Basondole Tools
# This code accepts a dictionary with host ip as key and commands to be sent to the host as values for input
# The code then sends the commands (dictionary values) to the host (dictionary key) via ssh then displays the output
# Can work with different shells but it is further optimised for JunoS, Cisco IOS and IOS XE and Debian
# AUTHOR: Paul S.I. Basondole

import paramiko
import Tkinter
import threading
import socket
from ClassOutput import outputWin
import sys
import time
import re


class ClassSendCommand():

    def execute(self,parent,confDict,user,key,extra=None):
        self.output = ''
        self.breakpoint = False
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
                 if confDict[ipaddress][0] == 'juniper':
                     secureCli.send('set cli screen-length 0\n')
                     secureCli.send('set cli screen-width 0\n')
                     for line in confDict[ipaddress][2]:
                        secureCli.send(line)
                        secureCli.send('\n')
                     try:
                        secureCli.send('quit\n')
                        #two line below to ignore uncomitted changes in junos
                        secureCli.send('\n')
                        secureCli.send('quit\n')
                     except socket.error: sessionClosed=True

                 elif confDict[ipaddress][0] == 'cisco':
                     secureCli.send('terminal length 0\n')
                     secureCli.send('terminal width 0\n')
                     for line in confDict[ipaddress][2]:
                        secureCli.send(line)
                        secureCli.send('\n')
                        time.sleep(.2)
                     # for ping to complete in cisco and take the next command
                     # avoid buffer waiting forever due to exit command issued below being droped
                     time.sleep(2)
                     secureCli.send('exit\n')
                     try:  secureCli.send('exit\n')
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
                 with lock: self.output+= '\n'+ ('['+ipaddress+']')
                 CISCOEXEC = '#'#+commandList[0]
                 CISCOUSER = '>'#+commandList[0]
                 JUNIPEROP = '> '#+commandList[0][0]+commandList[0][1]
                 LINUXUSER = '$ '#+commandList[0]
                 LINUXROOT = '# '#+commandList[0]
                 start = None
                 end = None
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
                    if re.findall(r'[>#$].?(quit|exit)',line):
                       end = (line)

                 if start==None:
                    with lock: self.output+= '\n'+ 'Device is up but taking too long to respond'

                 else:
                    for line in range(outputList.index(start),outputList.index(end)):
                       with lock: self.output+= '\n' + '   '+outputList[line]
                       if re.findall(r'^error',outputList[line]):
                          self.breakpoint = True
                          continue
                       if self.breakpoint: break

           except:
              self.output+= '\n [' + ipaddress+'] ' + str(sys.exc_info()[1])


        username,password = user,key
        threads = []
        lock = threading.Lock()

        for ipaddress in confDict.keys():
           t = threading.Thread(target=kazi, args=(username,password,ipaddress,lock))
           t.start()
           threads.append(t)
        for t in threads:
           t.join()

        self.devices, self.commands = [],[]

        if extra: self.output+= '\n[Scheduled operation]\n' + str(extra)

        output = outputWin()
        output.TB2('Commands',self.output,parent,None)
        parent.attributes('-disabled', True)
        return self.breakpoint



def test():
    user = 'fisi'
    key = 'fisi123'
    parent = Tkinter.Tk()
    confdict = {'192.168.56.36':['juniper','virtual-machine',['sh sys up']],
                '192.168.56.57':['juniper','virtual-machine',['show configuration interface em1.999','conf pri','set interface em1.999 vlan-id 999','show | compare', 'commit and-quit','show configuration interface em1.999']]}

    d = ClassSendCommand()
    d.execute(parent,confdict,user,key)
    parent.mainloop()


if __name__ == '__main__':
    test()
