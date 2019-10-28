
# This code will read and parse data a file and make bandwidth changes on specified interfaces at secified time
# The task scheduler is linux cronjob
# AUTHOR: Paul S.I. Basondole
import re
import time
import sys
import socket
import smtplib
import paramiko
import threading
import os
import getpass
import base64
import random
import Queue
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def getPe(line):
   pe = ((re.findall(r'pe\=(\S+)',line))[0]).strip()
   return pe

def getVlan(line):
   vlan = ((re.findall(r'vlan\=(\S+)',line))[0]).strip()
   return vlan

def getInterface(line):
   interface = ((re.findall(r'interface\=(\S+)',line))[0]).strip()
   return interface

def getBandwidth(line):
   bandwidthDay = ((re.findall(r'daybandwidth\=(\S+)',line))[0]).strip()
   bandwidthNight = ((re.findall(r'nightbandwidth\=(\S+)',line))[0]).strip()
   sixAmToday = ((time.ctime()).split()[0])+" "+((time.ctime()).split()[1])+" "+((time.ctime()).split()[2]).rjust(2)+" "+"06:00:00"+" "+((time.ctime()).split()[4])
   sixPmToday = ((time.ctime()).split()[0])+" "+((time.ctime()).split()[1])+" "+((time.ctime()).split()[2]).rjust(2)+" "+"18:00:00"+" "+((time.ctime()).split()[4])
   if time.ctime()>sixAmToday and time.ctime()<sixPmToday :
      bandwidth = bandwidthDay
   else:
      bandwidth = bandwidthNight
   return bandwidth

def getStartTime(line):
   return ((re.findall(r'starttime\=(\S+)',line))[0]).strip()

def getEndTime(line):
   return ((re.findall(r'endtime\=(\S+)',line))[0]).strip()

def getDays(line):
   return ((re.findall(r'days\=(\S+)',line))[0]).strip()

def getDetails(line):
   interface = getInterface(line)
   vlan = getVlan(line)
   pe = getPe(line)
   bandwidth = getBandwidth(line)
   startTime = getStartTime(line)
   endTime = getEndTime(line)
   days = getDays(line)
   return pe,interface,vlan,bandwidth,startTime,endTime,days


def getIpFromFile(FQP):
   routers = open(FQP,"r")
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

def config(cli,lock,vendor,ip,ipDict,interface,vlan,bandwidth):
   logEntry = ''
   if vendor == 'juniper':
       if len(ipDict[ip])==3: cli.send('edit logical-systems '+str(ipDict[ip][2])+'\n')
       cli.send('edit interfaces '+interface+'.'+vlan+'\n')
       cli.send('set family inet policer input '+bandwidth+'\n')
       cli.send('set family inet policer output '+bandwidth+'\n')
       cli.send('top\n')
       with lock:
          if len(ipDict[ip])==3:
             print time.ctime()+" "+ip+": "+"set logical-systems "+str(ipDict[ip][2])+" interfaces "+interface+" unit "+vlan+" family inet policer input "+bandwidth+" output "+bandwidth
             logEntry =(time.ctime()+" set logical-systems "+str(ipDict[ip][2])+" interface "+interface+" unit "+vlan+" family inet policer input "+bandwidth+" output "+bandwidth+"\n")
          else:
             print time.ctime()+" "+ip+": "+"set interfaces "+interface+" unit "+vlan+" family inet policer input "+bandwidth+" output "+bandwidth
             logEntry =(time.ctime()+" set interface "+interface+" unit "+vlan+" family inet policer input "+bandwidth+" output "+bandwidth+"\n")

   elif vendor == 'cisco':
      if int(vlan) !=0: cli.send("interfaces "+interface+"."+vlan+"\n")
      else: cli.send("interfaces "+interface+"\n")
      cli.send('service-policy input '+bandwidth)
      cli.send('service-policy output '+bandwidth)
      cli.send('exit\n')
      with lock: print time.ctime()+" "+ip+": "+" interfaces "+interface+" unit "+vlan+" service-policy input "+bandwidth+" output "+bandwidth
      logEntry =(time.ctime()+" interface "+interface+" unit "+vlan+" service-policy input "+bandwidth+" output "+bandwidth+"\n")

   return logEntry


def kazi(ip,ipDict,cli,lock):
   file = open(clientFilePath, "r")
   logFile = open (LogsDirPath+"\%s-cospa.log" %ip,"a")
   logEntry = ""
   for line in file:
      pe,interface,vlan,bandwidth,startTime,endTime,days = getDetails(line)
      if pe==ip:
         if days == 'weekends':
            if 'Fri' in time.ctime().split()[0] and ' 18:' in time.ctime():
               if ipDict[ip][0] == 'juniper': logEntry =config(cli,lock,'juniper',ip,ipDict,interface,vlan,bandwidth)
               elif ipDict[ip][0] == 'cisco': logEntry =config(cli,lock,'cisco',ip,interface,vlan,bandwidth)
               with lock: logFile.write(logEntry)
            elif 'Mon' in time.ctime().split()[0] and ' 06:' in time.ctime():
               if endTime == '0800' :
                  print time.ctime(),ip,"skipping 0800 package at 0600 >",interface+"."+vlan
                  continue
               else:
                  if ipDict[ip][0] == 'juniper': logEntry =config(cli,lock,'juniper',ip,ipDict,interface,vlan,bandwidth)
                  elif ipDict[ip][0] == 'cisco': logEntry =config(cli,lock,'cisco',ip,interface,vlan,bandwidth)
                  with lock: logFile.write(logEntry)
            elif 'Mon' in time.ctime().split()[0] and ' 08:' in time.ctime():
               if endTime == '0600' :
                  print time.ctime(),ip,"skipping 0600 package at 0800 >",interface+"."+vlan
                  continue
               else:
                  if ipDict[ip][0] == 'juniper': logEntry =config(cli,lock,'juniper',ip,ipDict,interface,vlan,bandwidth)
                  elif ipDict[ip][0] == 'cisco': logEntry =config(cli,lock,'cisco',ip,interface,vlan,bandwidth)
                  with lock: logFile.write(logEntry)
            elif 'S' in time.ctime().split()[0]:
               print time.ctime(),ip,"no change weekend package on weekends >",interface+"."+vlan
               continue
            else:
               print time.ctime(),ip,"skipping weekends package on weekdays >",interface+"."+vlan
            continue
         if days == 'weekdays' and 'S' in time.ctime().split()[0]:
            if 'Sat' in time.ctime().split()[0] and ' 06:' in time.ctime():
               if endTime == '0800' :
                  print time.ctime(),ip,"skipping 0800 package at 0600 >",interface+"."+vlan
                  continue
               else:
                  if ipDict[ip][0] == 'juniper': logEntry =config(cli,lock,'juniper',ip,ipDict,interface,vlan,bandwidth)
                  elif ipDict[ip][0] == 'cisco': logEntry =config(cli,lock,'cisco',ip,interface,vlan,bandwidth)
                  with lock: logFile.write(logEntry)
            elif 'Sat' in time.ctime().split()[0] and ' 08:' in time.ctime():
               if endTime == '0600' :
                  print time.ctime(),ip,"skipping 0600 package at 0800 >",interface+"."+vlan
                  continue
               else:
                  if ipDict[ip][0] == 'juniper': logEntry =config(cli,lock,'juniper',ip,ipDict,interface,vlan,bandwidth)
                  elif ipDict[ip][0] == 'cisco': logEntry =config(cli,lock,'cisco',ip,ipDict,interface,vlan,bandwidth)
                  with lock: logFile.write(logEntry)
            else:
               print time.ctime(),ip,"skipping weekdays package on weekends >",interface+"."+vlan
            continue
         if endTime == '0800' and ' 06:' in time.ctime():
            print time.ctime(),ip,"skipping 0800 package at 0600 >",interface+"."+vlan
            continue
         elif endTime == '0600' and ' 08:' in time.ctime():
            print time.ctime(),ip,"skipping 0600 package at 0800 >",interface+"."+vlan
            continue
         else:
            if ipDict[ip][0] == 'juniper': logEntry =config(cli,lock,'juniper',ip,ipDict,interface,vlan,bandwidth)
            elif ipDict[ip][0] == 'cisco': logEntry =config(cli,lock,'cisco',ip,interface,vlan,bandwidth)
            with lock: logFile.write(logEntry)

   logFile.close()

def sendMail(message):
   mail = smtplib.SMTP('basonation.org',25)
   #identify yourself to server
   mail.ehlo()
   #encryption
   mail.starttls()
   mail.login('basondole@basonation.org','password')
   mail.sendmail('cospa@basonation.org','basondole@basonation.org',message)
   mail.close()

def sshSetBandwidth(loopbackIp,ipDict,username,password,lock):
   log = open (LogsDirPath+"\%s-cli.log" %loopbackIp,"a")
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   try:
      with lock: print (time.ctime()+" (user = "+username+") authentication starting " + loopbackIp)
      try:
         sshClient.connect(loopbackIp, username=username, password=password, timeout=10,allow_agent=False,look_for_keys=False)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False

      if authenticated==False:
         with lock:print(time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp)
         sendMail("Subject: Cospa failed authentication report\n\n"+time.ctime()+" (user = "+username+") failed authentication > "+loopbackIp+"\n\n")
      elif authenticated==True:
         with lock:  print(time.ctime()+" (user = "+username+") passed authentication > "+loopbackIp)
         cli = sshClient.invoke_shell()
         if ipDict[loopbackIp][0] == 'juniper':
            cli.send("show system uptime | match current.time\n")
            cli.send("set cli screen-length 0\n")
            cli.send("set cli screen-width 0\n")
            cli.send("set cli complete-on-space off\n")
            cli.send("configure private\n")
         elif ipDict[loopbackIp][0] == 'cisco':
            cli.send("show clock\n")
            cli.send("terminal length 0\n")
            cli.send("terminal width 0\n")
            cli.send("configure terminal\n")

         kazi(loopbackIp,ipDict,cli,lock)

         if ipDict[loopbackIp][0] == 'juniper':
            cli.send("top\n")
            cli.send("commit and-quit\n")
            cli.send("quit\n")
         elif ipDict[loopbackIp][0] == 'cisco':
            cli.send("end\n")
            cli.send("write memory\n")
            cli.send("quit\n")

         time.sleep(5)
         with lock: log.write(time.ctime())
         with lock: log.write("\n----------------------------\n\n")

         cliOutput = cli.recv(65536)
         for line in cliOutput:
            with lock: log.write(line)
         sshClient.close()

         with lock: log.write("\n----------------------------\n")

      log.close()
   except socket.error:
      with lock: print(time.ctime()+" (user = "+username+") failed to connect > "+loopbackIp)
      sendMail("Subject: Cospa failed connetion report\n\n"+time.ctime()+" (user = "+username+") failed to connect > "+loopbackIp+"\n\n")


def runMultiThreads(ipDict):
   threads = []
   lock = threading.Lock()
   for ip in ipDict.keys():
      process = threading.Thread(target=sshSetBandwidth, args=(ip,ipDict,username,password,lock))
      process.start()
      threads.append(process)
   for process in threads:
      process.join()



def filePath():

   try:  credDirPath = sys.argv[sys.argv.index("-creddir")+1]
   except IndexError:
      print 'Specify the full path to directory that will contain credential file eg: -creddir "/home/docs/"'
      sys.exit()
   except ValueError:
      print 'Specify the full path to directory that will contain credential file eg: -creddir "/home/docs/"'
      sys.exit()

   try:
      ip = sys.argv[sys.argv.index("-testip")+1]
      if ip:
         if testCredential(ip,credDirPath): print 'Credential saved successfully'
         else: print 'There was a problem'
         sys.exit()
   except IndexError:
      pass
   except ValueError:
      pass


   try: ipFilePath = sys.argv[sys.argv.index("-ipdb")+1]
   except IndexError:
      print 'Specify full path of the ip database eg: -ipdb "/home/docs/routers.bas"'
      sys.exit()
   except ValueError:
      print 'Specify full path of the ip database eg: -ipdb "/home/docs/routers.bas"'
      sys.exit()

   try: clientFilePath = sys.argv[sys.argv.index("-clientdb")+1].strip()
   except ValueError:
         print 'Specify full path of the clients database eg: -clientdb "/home/docs/clients.db"'
         sys.exit()
   except IndexError:
         print 'Specify full path of the ip database eg: -clientdb "/home/docs/clients.db"'
         sys.exit()

   try: LogsDirPath = sys.argv[sys.argv.index("-logdir")+1].strip()
   except ValueError:
         print 'Specify full path of the log directory eg: -logdir "/home/Logs/"'
         sys.exit()
   except IndexError:
         print 'Specify full path of the log directory eg: -logdir "/home/Logs/"'
         sys.exit()

   return ipFilePath,clientFilePath,LogsDirPath,credDirPath



def encrypt(data):
   key = 'eeCCJ-A1Kazl55rohV4V1q0xC0xl1dOewxhHBaXo4DY='
   cipher_suite = Fernet(key)
   result = cipher_suite.encrypt(data)
   key=random.choice("0123456789abcde")+random.choice('*()^%$')+random.choice('ABCDEFGH')
   return key,base64.b64encode(base64.b64encode(data+key)+key)+key,result

def decrypt(key,data):
   try: base64.b64decode(base64.b64decode(data.split(key)[0]).split(key)[0]).split(key)[0]
   except TypeError:
      try: os.remove(credDirPath+'.baslogin')
      except WindowsError: deleted=True
      print 'INFO: Auto-retrieved login could not be decrypted, the login file has been tempered with'
      print 'INFO: Saved logins will now be destroyed'
      sys.exit('INFO: re-Run the command and enter credentials')
   return base64.b64decode(base64.b64decode(data.split(key)[0]).split(key)[0]).split(key)[0]

def credentials(credDirPath,trial):
   def createLogin():
      ukey,username,key = encrypt(raw_input('Username: '))
      pkey,password,key = encrypt(getpass.getpass())
      mkfile = open(credDirPath+'\.baslogin','w')
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
         creds= open(credDirPath+'\.baslogin','r')
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


def verifyUser(credDirPath,ipaddress,returnQ,trial):
   ukey,username,pkey,password = credentials(credDirPath,trial)
   sshClient = paramiko.SSHClient()
   sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

   print (time.ctime()+" (user = "+decrypt(ukey,username)+") initializing connection "+ipaddress.rjust(15))
   try:
      print (time.ctime()+" (user = "+decrypt(ukey,username)+") authentication starting " + ipaddress.ljust(15))
      try:
         sshClient.connect(ipaddress, username=decrypt(ukey,username), password=decrypt(pkey,password), timeout=2)
         authenticated = True
      except (socket.error, paramiko.AuthenticationException):
         authenticated = False
         print(time.ctime()+" (user = "+decrypt(ukey,username)+") failed authentication > "+ipaddress.ljust(15))
         returnQ.put(None)
      if authenticated==True:
         print(time.ctime()+" (user = "+decrypt(ukey,username)+") passed authentication > "+ipaddress.ljust(15))
         sshClient.close()
         returnQ.put('Success')
      return ukey,username,pkey,password
   except socket.error:
      print(time.ctime()+" (user = "+decrypt(ukey,username)+") failed to connect > "+ipaddress.ljust(15))
      returnQ.put('Failed connection')

def testCredential(ip,credDirPath):
   returnQ = Queue.Queue()
   ukey,username,pkey,password = verifyUser(credDirPath,ip,returnQ,None)
   verified = returnQ.get()
   while verified==None:
      ukey,username,pkey,password =verifyUser(credDirPath,ip,returnQ,'try')
      verified = returnQ.get()
   if verified: return True


def test():
   startTime = time.time()

   username,password = "fisi", "fisi123"
   ipFilePath = "C:\Users\u\Desktop\PACOM\%s" %'routers.bas'
   clientFilePath = "C:\Users\u\Desktop\PACOM\%s" %'burstclients.txt'
   LogsDirPath = "C:\Users\u\Desktop\PACOM\Logs\\"

   ipFilePath = "/home/basondole/PACOM/burstmanager/routers.txt"
   clientFilePath = "/home/basondole/PACOM/burstmanager/burstclients.baso"
   LogsDirPath = "/home/basondole/PACOM/Logs/"

   ipFilePath,clientFilePath,LogsDirPath,credDirPath = filePath()

   ukey, user, pkey, word = credentials(credDirPath,None)
   username,password = decrypt(ukey,user),decrypt(pkey,word)

   print ipFilePath
   print clientFilePath
   print LogsDirPath

   ipDict = getIpFromFile(ipFilePath)

   print ipDict
   sys.exit()

   runMultiThreads(ipDict)

   print "\ncode run-time:",round(time.time()-startTime),"\n"
   raw_input("\nPress any key to exit")
   sys.exit()

if __name__ == "__main__":
   test()
