'''
Send command(s) to network device(s) on the fly
'''

try:
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
    import queue
    from cryptography.fernet import Fernet
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    from Crypto import Random


    __author__ = "Paul S.I. Basondole"
    __credits__ = "Paul S.I. Basondole"
    __version__ = "2.0"
    __maintainer__ = "Paul S.I. Basondole"
    __email__ = "bassosimons@me.com"


    def inputstuff():
       ''' Method to get device(s) ip addresses and command(s)
       This arguments can be literal strings or read from text files
       '''
       
       try: 
          sys.argv.index("-version")
          print('talkToUs')
          print('Version: 2.0')
          print('Developer: Paul S.I. Basondole')
          return [],[]
       except: pass

       try:
          try: commands = sys.argv[sys.argv.index("-commands")+1]
          except IndexError:
             print('Specify commands example: basowilldo -commands "show system users:show system uptime"')
             sys.exit()
       except ValueError:
          try:
             try: commandsFile = sys.argv[sys.argv.index("-commandsFile")+1]
             except IndexError:
                print('Specify commands file example: basowilldo -commandsFile mycommands.txt')
                sys.exit()
          except ValueError:
             print('use [-commandsFile] followed by file name or')
             print('use [-commands] followed by "command1:command2:etc", if more than one, commands are separated by :')
             print('example: basowilldo -commands "show system users:show system uptime"')
             print('example: basowilldo -commandsFile mycommands.txt')
             input('NB: Use cmd to launch this tool with above options')
             sys.exit()

       try: ipaddress = sys.argv[sys.argv.index("-ipaddress")+1].strip()
       except (ValueError,IndexError):
          try:
             ipaddressFile = sys.argv[sys.argv.index("-ipaddressFile")+1]
          except (ValueError,IndexError):         
             print('use [-ipaddress] to specify the host device or')
             print('use [-ipaddressFile] followed by file name')
             print('example: basowilldo -commands "show system users:show system uptime" -ipaddress 10.0.0.1')
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

       
       if ':' in ipaddress: ipList = [ip for ip in ipaddress.split(':') if ip]

       else:
          ipList = []
          try: ipList.append(ipaddress.strip())
          except UnboundLocalError:
             ipFile = open(ipaddressFile,'r')
             for line in ipFile:
                for item in line.split('\n'):
                   if len(item)==0: continue
                   ipList.append(item)


       return commandList,ipList



    def credentials(trial):
       '''Method to get login credentials from user
       Saves issued credential in an encrypted file
       '''

       def createLogin():
          ukey,username,key = encrypt(input('Username: ').encode())
          pkey,password,key = encrypt(getpass.getpass().encode())

          mkfile = open('.basdoin','w')
          mkfile.write(key.decode())
          mkfile.write(' ')
          mkfile.write('ux?/'+username.decode())
          mkfile.write(' ')
          mkfile.write('kx!#'+password.decode())
          mkfile.write(' ')
          mkfile.write('9$x!'+ukey.decode())
          mkfile.write(' ')
          mkfile.write('Z@%*'+pkey.decode())
          mkfile.close()

          return ukey,username,pkey,password
          
       if trial: ukey,username,pkey,password = createLogin()
       else:
          try:
             creds= open('.basdoin','r')

             for line in creds:

                try:
                   username = re.findall(r'ux\?/(\S+)',line)[0].encode()
                   password = re.findall(r'kx\!\#(\S+)',line)[0].encode()
                   ukey = re.findall(r'9\$x\!(\S+)',line)[0].encode()
                   pkey= re.findall(r'Z\@\%\*(\S+)',line)[0].encode()
                   print ('')
                   print ('INFO: username and password auto-retrieved')

                except IndexError: ukey,username,pkey,password = createLogin()

          except IOError: ukey,username,pkey,password = createLogin()
             
       try: ukey,username,pkey,password
       except UnboundLocalError: ukey,username,pkey,password = createLogin()
          
       return ukey,username,pkey,password



    def verifyUser(ipaddress,trial):
       ''' Method to verify the vaidity of the issued credentials'''
       
       global returnQ
       ukey,username,pkey,password = credentials(trial)
       sshClient = paramiko.SSHClient()
       sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

       try:

          try:
             sshClient.connect(ipaddress, username=decrypt(ukey,username), password=decrypt(pkey,password),
                               timeout=10,allow_agent=False,look_for_keys=False)
             authenticated = True
          except (socket.error, paramiko.AuthenticationException):
             authenticated = False
             print(time.ctime()+" (user = "+decrypt(ukey,username).decode()+") failed authentication > "+ipaddress.ljust(15))
             returnQ.put(None)
             
          if authenticated==True:
             sshClient.close()
             returnQ.put('Success')
          return ukey,username,pkey,password
       
       except socket.error:
          print(time.ctime()+" (user = "+decrypt(ukey,username).decode()+") failed to connect > "+ipaddress.ljust(15))
          returnQ.put('Failed connection')
       
          
       
    class job():
       ''' Core operation class
       '''

       def __init__(self,ukey,username,pkey,password):
          global returnQ
          
          self.commandList,ipList = inputstuff()

          threads = []
          lock = threading.Lock()
          
          for ipaddress in ipList:
             t = threading.Thread(target=self.kazi, args=(ukey,username,pkey,password,ipaddress,lock,returnQ))
             t.start()
             threads.append(t)

          for t in threads: t.join()
        

       def kazi(self,ukey,username,pkey,password,ipaddress,lock,returnQ):
          ''' Method to establish ssh connection to device
          '''
          
          commandList = self.commandList
          sshClient = paramiko.SSHClient()
          sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

          try:

             try:
                sshClient.connect(ipaddress, username=decrypt(ukey,username), password=decrypt(pkey,password), 
                                  timeout=10,allow_agent=False,look_for_keys=False)
                authenticated = True
             except (socket.error, paramiko.AuthenticationException):
                authenticated = False
                with lock: print(time.ctime()+" (user = "+decrypt(ukey,username).decode()+") failed authentication > "+ipaddress.ljust(15))


             if authenticated==True: 

                  console_output = ''
                  secureCli = sshClient.invoke_shell()
                  secureCli.send('set cli screen-length 0\n')
                  secureCli.send('set cli screen-width 0\n')
                  secureCli.send('terminal length 0\n')
                  secureCli.send('terminal width 0\n')

                  time.sleep(1)
                  pre_output = secureCli.recv(65535).decode("utf-8")
                  cliprompt = pre_output.split('\n')[-1].strip()
                  del pre_output

                  for line in commandList:
                     line = line.strip()
                     if not line: continue
                     secureCli.send(line)
                     secureCli.send('\n')
                     time.sleep(1)
                  
                  try:
                     secureCli.close()
                  except socket.error: pass # session already Closed
                  time.sleep(5)
                  while True:
                     cli_output = secureCli.recv(65535).decode("utf-8")
                     if not cli_output: break
                     for line in cli_output:  console_output+=str(line)
                  
                  sshClient.close()

                  output_lines = console_output.split('\n')
                  output_lines[0] = cliprompt+str(output_lines[0])
                  if cliprompt == output_lines[-1].strip():
                     output_lines.pop(-1)

                  for index,line in enumerate(output_lines):
                     line = line.rstrip()
                     output_lines[index] = line

                     if re.search(r'^'+cliprompt,line):
                        line = line.split(cliprompt)
                        line = ' '.join(line)

                        head = '\n'
                        head += line.strip() +'\n'+ ''.join(['-' for x in range(len(line.strip()))])
                        output_lines[index] = head


                  output_lines = '\n'.join(output_lines)
                  output_lines = output_lines.split('\n')


                  with lock:
                         print('\n'+ ('['+ipaddress+']'))
                         for line in output_lines:
                            print('\n' + '   '+line,end='')
                         print('\n'+'\n')


          except TypeError:
             returnQ.put(None)


          

    def encrypt(data):

       key = 'eeCCJ-A1Kazl55rohV4V1q0xC0xl1dOewxhHBaXo4DY='
       cipher_suite = Fernet(key)
       result = cipher_suite.encrypt(data)
       key = random.choice("0123456789abcde")+random.choice('*()^%$')+random.choice('ABCDEFGH')
       key = key.encode()
       return key,base64.b64encode(base64.b64encode(data+key)+key)+key,result

    def decrypt(key,data):

       try: base64.b64decode(base64.b64decode(data.split(key)[0]).split(key)[0]).split(key)[0]
       except TypeError:
          try: os.remove('.basdoin')
          except WindowsError: deleted=True
          print('INFO: Auto-retrieved login could not be decrypted, the login file has been tempered with')
          print('INFO: Saved logins will now be destroyed')
          sys.exit('INFO: re-Run the command and enter credentials')
       return base64.b64decode(base64.b64decode(data.split(key)[0]).split(key)[0]).split(key)[0]
     

    if __name__== "__main__":

       returnQ = queue.Queue()
       commands,ipList = inputstuff()

       if not commands or not ipList: sys.exit()

       ukey,username,pkey,password = verifyUser(ipList[0].strip(),None)
       verified = returnQ.get()
       
       while verified==None:
          ukey,username,pkey,password =verifyUser(ipList[0].strip(),'try')
          verified = returnQ.get()
          
       if verified: job(ukey,username,pkey,password)


       print('\nINFO: Developed by Paul S.I. Basondole')
   
except KeyboardInterrupt:
   pass
