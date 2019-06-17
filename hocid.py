import datetime
import difflib
import time
import paramiko
import threading
import subprocess
import smtplib
import re



class oltconnect():


   def __init__(self,username,password):

      self.session = paramiko.SSHClient()
      self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      self.username = username
      self.password = password

   def getconf(self,HOST):

      self.session.connect(HOST, username=self.username, password=self.password, timeout=10,allow_agent=False,look_for_keys=False)
      self.cli = self.session.invoke_shell()
      time.sleep(1) 

      self.cli.send("scroll\n")
      self.cli.send("\n")
      time.sleep(1)

      tmp = self.cli.recv(65535) # discard the output
      del tmp

      self.cli.send(getlasthourlog()+"\n")
      time.sleep(3)

      userlog = self.cli.recv(65535)
      
      self.cli.send("enable\n")
      time.sleep(1)

      self.cli.send("display current-configuration simple\n")
      self.cli.send("\n")
      time.sleep(300)

      self.cli.send("quit\n")
      self.cli.send("y\n")
      time.sleep(5)

      self.session.close()
      result = ''
      while True:
         output = self.cli.recv(65535)
         if not output: break
         for line in output: result+=str(line)

      return result,userlog

def getlasthourlog():

   cmd = 'display log all '
   cmd += (datetime.datetime.now()-datetime.timedelta(hours=1)).isoformat().replace('T',' ').split(':')[0]+':00:00 - '
   cmd += datetime.datetime.now().isoformat().replace('T',' ').split(':')[0]+':00:00'

   return cmd


def modconfig(output):
   outputList = output.split("\r\n")
   startmark =  '[global-config]'
   endmark = 'return'

   return outputList,startmark,endmark 


def moduserlog(output):
   outputList = output.split("\r\n")
   startmark = outputList[1]
   endmark = outputList[-1]
   
   return outputList,startmark,endmark 


def filemake(HOST,outputList,startmark,endmark):

   stamp = datetime.datetime.now()
   stamp = str(stamp)
   stamp = stamp.replace(':','-')
   stamp = '_'.join(stamp.split())
   filename = HOST+'_'+stamp
   try:
      with open('./backups/'+filename,'w') as _:
         for line in range(outputList.index(startmark),outputList.index(endmark)):
            _.write(outputList[line]+'\n')
   except Exception: return False

   return filename


def previousfile(HOST):

   fl = subprocess.Popen("cd backups/ && /bin/ls "+HOST+"_*"+" -l | /usr/bin/awk '{print $9 }' | /usr/bin/sort -r | awk 'NR==1 {print}'",stdout=subprocess.PIPE,shell=True)        
   for line in fl.stdout: previousfile = str(line.strip())

   return previousfile



def mail(host,message):
   user = 'user-email'
   password = 'user-mail-password'
   mailserver = 'user-mail-server'
   portnumber = 'user-mail-server-port'
   destination = 'mail-recepient'
   barua = postman(user,password,mailserver,portnumber)
   barua.sendMail(destination,message,subject=host+" OLT config differ")



def makedif(previousfile,currentfile):
   _d1 = {} #for previous config file
   _d2 = {} #for current config file

   for line in open(previousfile).readlines():
     line = line.strip('\n')
     if re.match(r'  <',line):
        section = line
        _d1[section]=[]
     else:
        try: _d1[section].append(line)
        except KeyError: _d1[line] = []
        except NameError: _d1[line] = []
        except UnboundLocalError: _d1[line] = []

         
   for line in open(currentfile).readlines():
     line = line.strip('\n')
     if re.match(r'^  <',line):
        section = line
        _d2[section]=[]
     else:
        try: _d2[section].append(line)
        except KeyError: _d2[line] = []
        except NameError: _d2[line] = []
        except UnboundLocalError: _d2[line] = []

         
   _d = list(set(list(_d1.keys()) + list(_d2.keys())))


   tofauti = ''
   for key in _d:
      if key in _d1.keys() and key in _d2.keys():
         mbadala = ''
         for line in difflib.unified_diff(_d1[key],_d2[key]):
            if str(line[0]) in ('+','-'):
               mbadala += ' '+str(line).strip()+'\n\n'
         if mbadala:
            tofauti += key.strip()+'\n'+mbadala+'\n'
         
      elif key in _d1.keys():
         tofauti += '-'+key.strip()+'\n\n'
         for line in difflib.unified_diff(_d1[key],[]):
            if str(line[0]) in ('+','-'):
               tofauti+=' '+str(line).strip()+'\n\n'
      elif key in _d2.keys():
         tofauti += '+'+key.strip()+'\n\n'
         for line in difflib.unified_diff([],_d2[key]):
            if str(line[0]) in ('+','-'):
               tofauti+=' '+str(line).strip()+'\n\n'
   if not tofauti: tofauti+= '\n No record is available'

   return tofauti


def fanyakazi(HOST,username,password,lock=None):

   previous = previousfile(HOST)

   con =  oltconnect(username,password)
   config, userlog = con.getconf(HOST)
   outputList,startmark,endmark = modconfig(config)
   current = filemake(HOST,outputList,startmark,endmark)
   if not current: return

   logList,startmark,endmark = moduserlog(userlog)
   userlog = ''
   for line in range(logList.index(startmark),logList.index(endmark)):
      userlog+=str(logList[line])+'\n'
   
   text1 = './backups/'+previous
   text2 = './backups/'+current

   tofauti = ''
   tofauti+= 'Node: '+HOST+'\n\nUser logs:\n\n'

   tofauti += userlog+'\n\nConfiguration changes:\n'

   tofauti += makedif(text1,text2)

   for key,value in OLTs.items():
       if value == HOST:
          HOST = key
          break

   mail(HOST,tofauti)



def multithread(OLTs,username,password):
   threads = []

   for HOST in OLTs.keys():
         process = threading.Thread(target=fanyakazi, args=(OLTs[HOST],username,password))
         process.start()
         threads.append(process)

   for process in threads:  process.join()



class postman():

    def __init__(self,user,password,mailserver,portnumber):
        self.user = user
        self.password = password
        self.mailserver = mailserver
        self.portnumber = portnumber

        self.mail = smtplib.SMTP(self.mailserver,self.portnumber)
        self.mail.ehlo()    #identify yourself to server
        self.mail.starttls()    #encryption

    def sendMail(self,destination,message,subject=None):

       if not subject: subject=message.split()[0]

       BODY = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(self.user,destination,subject,message)

       self.mail.login(self.user,self.password)
       self.mail.sendmail(self.user,destination,BODY)
       self.mail.close()





if __name__ == '__main__':


   OLTs = {
          'olt-1':'10.2.4.2',
          'olt-2':'10.17.4.218',
          'olt-3':'10.10.5.74',
          'olt-4':'10.13.4.58'
         }


   username = "sshuser"
   password = "sshpassword"

   starttime = time.time()

   multithread(OLTs,username,password)

   print('run-time '+str(time.time()-starttime))
