try:
	import pprint
	import getpass
	import threading
	import datetime
	import time
	import paramiko
	import importlib
	import re
	import sys
	import os
	from napalm import (junos,
						ios)
	from napalm.base.utils import py23_compat
	from colorama import Fore, Style, init


	__author__ = "Paul S.I. Basondole"
	__version__ = "1.0"
	__maintainer__ = "Paul S.I. Basondole"
	__email__ = "bassosimons@me.com"


	init(autoreset=True, strip=False)

	def start():
		global username,password,_db,failed,result

		try:
			if not os.path.exists('backup'):
				os.makedirs('backup')
		except:
			result = 'You do not have permission to create a folder in this directory'
			sys.exit()

		try:
			with open('devices.txt') as _db:
				db = _db.readlines()
		except FileNotFoundError:
			result = '''
Create a file "devices.txt" in this directory in which you list the ip address of device
and the respective operating software such as:

ios 10.10.1.100
junos 10.10.1.200
ios 10.1.1.1'''

			sys.exit()


		_db = {line.split()[1]:line.split()[0]
				for line in db if line.strip() and not re.search(r'^#',line)}
		print('\n')
		title = ('Config will be extracted from these boxes')
		msg = "{}".format(title)
		print("{}{}{}".format(Style.BRIGHT, Fore.GREEN, msg))
		print('\n')

		print('+-----+----------------------+----------+')
		print('| %s| %s| %s|'%('No'.ljust(4),'DEVICE IP'.ljust(21),'SOFTWARE'.ljust(9)))
		print('+-----+----------------------+----------+')
		dev_no = 1
		for device in sorted(_db.items(), key=lambda x: x[1], reverse=True):
			print('| %s| %s| %s|'%(str(dev_no).ljust(4),device[0].ljust(21),device[1].ljust(9)))
			print('+-----+----------------------+----------+')
			dev_no+=1
		
		print('\n')

		print("{}{}{}{}{}".format(Style.BRIGHT, Fore.CYAN, 'SSH LOGIN','\n',
								'-----------------------------------------'))
		username = input('USERNAME: ')
		password = getpass.getpass('PASSWORD: ')
		failed = []



	def getconf(ip,username,password,_db,failed,data,lock):
		if _db[ip] == 'junos':
			dev = junos.JunOSDriver(ip, username, password)

		elif _db[ip] == 'ios':
			dev = ios.IOSDriver(ip, username, password)

		try:
			dev.open()
			try:
				facts = dev.get_facts(interfaces=False)
			except: pass
			config = dev.get_config()
			dev.close()
		except Exception as e:
			if str(py23_compat.text_type(e)) != 'None':
				failed.append({ip:[_db[ip],py23_compat.text_type(e)]})
			else:
				failed.append({ip:[_db[ip],e]})

			return

		try: facts
		except:
			if _db[ip] == 'junos':
				sshClient = paramiko.SSHClient()
				sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				try:
					sshClient.connect(ip, username=username, password=password,
									timeout=10,allow_agent=False,look_for_keys=False)
					secureCli = sshClient.invoke_shell()
					secureCli.send('set cli screen-length 0\n')
					secureCli.send('set cli screen-width 0\n')
					time.sleep(5)
					secureCli.recv(65535)
					secureCli.send('\n')
					time.sleep(.5)
					sshClient.close()
					hostname = secureCli.recv(65535).decode()
					facts = {}
					facts['hostname'] = hostname.strip().split('@')[1].split('>')[0]

					facts['vendor'] = 'Juniper'
					facts['model'] = '-'
					facts['serial_number'] = '-'
					facts['os_version'] = '-'
					facts['uptime'] = '-'

				except Exception as _:
					if str(py23_compat.text_type(_)) != 'None':
						failed.append({ip:[_db[ip],py23_compat.text_type(_)]})
					else:
						failed.append({ip:[_db[ip],_]})
					return


		conf_exist = True


		if not config['running'].strip():

			if _db[ip] == 'junos': # for junos ['os_version'] < 11
				try:
					sshClient = paramiko.SSHClient()
					sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					sshClient.connect(ip, username=username, password=password,
									timeout=10,allow_agent=False,look_for_keys=False)
					secureCli = sshClient.invoke_shell()
					secureCli.send('set cli screen-length 0\n')
					secureCli.send('set cli screen-width 0\n')
					time.sleep(5)
					secureCli.recv(65535)
					secureCli.send('show configuration\n')
					time.sleep(30)
					sshClient.close()

					console_output = ''

					while True:
						try: cli_output = secureCli.recv(65535).decode()
						except:
							failed.append({ip:[_db[ip],'BROKEN CONFIG']})
							return
						if not cli_output: break
						for line in cli_output:
							console_output+=str(line)


					conf = console_output.split('\n')
					conf.pop(0)
					conf.pop(-1)
					config = {'startup':'','running':'','candidate':''}
					config['running'] = ''.join(conf)

				except:
					conf_exist = False


		if not config['startup'].strip() and not config['running'].strip() and not config['candidate'].strip():
			failed.append({ip:[_db[ip],'NO CONF']})
			conf_exist = False


		if conf_exist:
			with lock:
				print('Completed collecting config from %s [%s]'%(ip.ljust(15),facts['hostname']))

				data[facts['hostname']] = {'ip':ip,
										   'vendor':facts['vendor'],
										   'model':facts['model'],
										   'serial':facts['serial_number'],
										   'software':facts['os_version'],
										   'uptime':facts['uptime']}

				if _db[ip] == 'ios':
					# _type = re.search(r'(\S+) Software',data[facts['hostname']]['software']).group(0)
					# _vers = re.search(r'Version (\S+)',data[facts['hostname']]['software']).group(0)
					# data[facts['hostname']]['software'] = _type+' '+_vers.replace('Version','')

					_remove = re.search(r'\((\S+)\)',data[facts['hostname']]['software']).group(0)
					_vers = data[facts['hostname']]['software'].replace(_remove,'').replace('Version','')
					data[facts['hostname']]['software'] = _vers.replace('  ','')[:_vers.rfind(',')].replace(',','')

			saa = datetime.datetime.now().isoformat().replace(':','-')[:-10]
			with open('%s/%s_%s_%s.conf'%('backup',ip,facts['hostname'],saa),'w') as _:
				for line in config['running'].split('\n'):
					try: _.write('%s\n'%line)
					except Exception as e:
						with lock:
							print('\n')
							print('%s [%s]\n%s'%(ip,facts['hostname'],py23_compat.text_type(e)))
							print('Found a line that has a non standard unicode character (non printable)')
							print('The offending character will be replaced by a character code instead')
							print('-%s' %line)
							print('+%s' %line.encode('unicode-escape').decode('utf-8'))
							print('\n')
						_.write('%s\n' %line.encode('unicode-escape').decode('utf-8'))



	def doit():
		
		global username,password,_db,failed,result,anza

		data = {}

		start()

		print('')
		print("{}{}{}".format(Style.BRIGHT, Fore.CYAN, 'Please wait...'))
		print('')

		anza = time.time()

		threads = []
		lock = threading.Lock()

		for ip in _db:
			t = threading.Thread(target=getconf, args=(ip,username,password,_db,failed,data,lock))
			t.start()
			threads.append(t)

		for t in threads: t.join()

		global failed_con
		failed_con = []
		failed_conf = []

		for item in failed:
			# item is a dict
			key = list(item.keys())[0]
			value = item[key]

			if value[1]=='NO CONF':
				failed_conf.append(item)
			elif value[1]=='BROKEN CONFIG':
				failed_conf.append(item)
			else:
				failed_con.append(item)

		if failed_con:
			print('\n')
			msg = 'FAILED CONNECTIONS'
			msg+= '\n'

			print("{}{}{}".format(Style.BRIGHT, Fore.RED, msg))

			msg =('+-----+----------------------+%s+'%('-'*101))
			msg+= '\n'
			msg+=('| %s| %s| %s|'%('No'.ljust(4),'DEVICE IP'.ljust(21),'ERROR'.ljust(100)))
			msg+= '\n'
			msg+=('+-----+----------------------+%s+'%('-'*101))
			print("{}{}{}".format(Style.BRIGHT, Fore.RED, msg))

			dev_no = 1
			for device in failed_con:
				for ip,error in device.items():
					msg =('| %s| %s| %s|'%(str(dev_no).ljust(4),ip.ljust(21),str(error).ljust(100)))
					msg+= '\n'
					msg+=('+-----+----------------------+%s+'%('-'*101))
					
					print("{}{}{}".format(Style.BRIGHT, Fore.RED, msg))
					
					dev_no+=1
		

		if failed_conf:
			print('\n')
			msg = 'FAILED CONFIG ACQUISITION'
			msg+= '\n'

			print("{}{}{}".format(Style.BRIGHT, Fore.YELLOW, msg))

			msg =('+-----+----------------------+%s+'%('-'*101))
			msg+= '\n'
			msg+=('| %s| %s| %s|'%('No'.ljust(4),'DEVICE IP'.ljust(21),'ERROR'.ljust(100)))
			msg+= '\n'
			msg+=('+-----+----------------------+%s+'%('-'*101))
			print("{}{}{}".format(Style.BRIGHT, Fore.YELLOW, msg))

			dev_no = 1
			for device in failed_conf:
				for ip,error in device.items():
					msg =('| %s| %s| %s|'%(str(dev_no).ljust(4),ip.ljust(21),str(error).ljust(100)))
					msg+= '\n'
					msg+=('+-----+----------------------+%s+'%('-'*101))
					
					print("{}{}{}".format(Style.BRIGHT, Fore.YELLOW, msg))
					
					dev_no+=1

	

		print('\n')


		if (len(_db)-len(failed)) > 0:

			msg = 'RECAP'
			msg+= '\n'

			print("{}{}{}".format(Style.BRIGHT, Fore.GREEN, msg))

			msg =('+----------------------+-----------------')
			msg+=('+------------+-----------------')
			msg+=('+---------------+-----------------------------')
			msg+=('+------------+')
			msg+=('\n')
			msg+=('| %s| %s'%('HOSTNAME'.ljust(21),'DEVICE IP'.ljust(16)))
			msg+=('| %s| %s'%('VENDOR'.ljust(11),'MODEL'.ljust(16)))
			msg+=('| %s| %s'%('SERIAL'.ljust(14),'SOFTWARE'.ljust(28)[:28]))
			msg+=('| %s|'%('UPTIME (s)'.ljust(11)))
			msg+=('\n')
			msg+=('+----------------------+-----------------')
			msg+=('+------------+-----------------')
			msg+=('+---------------+-----------------------------')
			msg+=('+------------+')

			print("{}{}{}".format(Style.BRIGHT, Fore.GREEN, msg))

			for device in sorted(data.keys()):

				msg =('| %s| %s'%(device.ljust(21),data[device]['ip'].ljust(16)))
				msg+=('| %s| %s'%(data[device]['vendor'].ljust(11),data[device]['model'].ljust(16)))
				msg+=('| %s| %s'%(data[device]['serial'].ljust(14),data[device]['software'].ljust(28)[:28]))
				msg+=('| %s|'%(str(data[device]['uptime']).ljust(11)))
				msg+=('\n')
				msg+=('+----------------------+-----------------')
				msg+=('+------------+-----------------')
				msg+=('+---------------+-----------------------------')
				msg+=('+------------+')

				print("{}{}{}".format(Style.BRIGHT, Fore.GREEN, msg))

		print('\n')


		result = 'Collected config files: %d/%d'%((len(_db)-len(failed)),len(_db))



	if __name__ == '__main__': doit()


		
except KeyboardInterrupt:
	
	result = 'Exiting on user request'

finally:

	print('\n')
	
	try:

		msg = 'SUMMARY'
		msg+= '\n'
		msg+= '-------'
		msg+= '\n'
		msg+= '\n'
		msg+= ' ! Failed connections: %d'%len(failed_con)
		msg+= '\n'
		msg+= " ! {}\n\n {}".format(result,'[Finished in %ds] ' %(time.time() - anza))
		print("{}{}{}".format(Style.BRIGHT, Fore.MAGENTA, msg))
		print('\n')
		print('\n')

		greetings = 'Support the developer'
		greetings+= '\n'
		greetings+= 'Cut cheque: bassosimons@me.com'
		print("{}{}{}".format(Style.BRIGHT, Fore.CYAN, greetings))
		
		greetings = 'Buy coffee: 255 (0)68 960 7406'
		greetings+= '\n'
		greetings+= 'Copyrightâ„—: Paul S.I.Basondole'
		print("{}{}{}".format(Style.BRIGHT, Fore.CYAN, greetings))
		print('\n')
		print('\n')

	except:
		try:
			print(result)
			print('\n')
			print('Support the developer bassosimons@me.com')
			print('\n')
			print('\n')
		except Exception as e:
			print('Error: %s'%e)
			sys.exit()
