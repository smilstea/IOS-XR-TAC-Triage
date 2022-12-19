#!/usr/bin/env python

__author__     = "Sam Milstead"
__copyright__  = "Copyright 2022 (C) Cisco TAC"
__credits__    = "Sam Milstead"
__version__    = "1.0.1"
__maintainer__ = "Sam Milstead"
__email__      = "smilstea@cisco.com"
__status__     = "alpha"

import pexpect
import os
import sys
import getpass
import re

def task():
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.1"
	###__status__     = "alpha"
	###command line handling, OS / file handling, SSH/telnet calls
	key = 1
	is_error = False
	ssh = False
	memcompare = False
	config = False
	file = ''
	ipv4_addr = ''
	username = ''
	timeout = ''
	pre_file = ''
	post_file = ''
	for index, arg in enumerate(sys.argv):
		if arg in ['--file'] and len(sys.argv) > index + 1:
			file = str(sys.argv[index + 1])
			del sys.argv[index]
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--ipv4addr', '-i'] and len(sys.argv) > index + 1:
			ipv4_addr = str(sys.argv[index + 1])
			del sys.argv[index]
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--username', '-u'] and len(sys.argv) > index + 1:
			username = str(sys.argv[index + 1])
			del sys.argv[index]
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--ssh', '-s']:
			ssh = True
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--timeout', '-t'] and len(sys.argv) > index + 1:
			timeout = int(sys.argv[index + 1])
			del sys.argv[index]
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--memcompare']:
			memcompare = True
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--config']:
			config = True
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--pre'] and len(sys.argv) > index + 1:
			pre_file = str(sys.argv[index + 1])
			del sys.argv[index]
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--post'] and len(sys.argv) > index + 1:
			post_file = str(sys.argv[index + 1])
			del sys.argv[index]
			del sys.argv[index]
			break
	for index, arg in enumerate(sys.argv):
		if arg in ['--help', '-h']:
			print("Usage: python3 {" + sys.argv[0] + "} [--file <filename>][--ipv4addr <ipv4 address>][--username <username>](--ssh)(--timeout <seconds>)")
			print("Usage: python3 {" + sys.argv[0] + "} [--memcompare][--pre <filename>][--post <filename>]")
			print("Usage: python3 {" + sys.argv[0] + "} [--config][--file <filename>]")
			print("\n")
			print("""Current Working Modules:
			| 1 L2VPN
			----| 1 AC Down / Unresolved
			----| 2 AC Traffic Loss
			----| 3 PW Down
			| 3 Install
			----| 1 Failed Install (cXR)
			| 4 Memory
			---- | 1 Memory Leak
			| 5 High CPU
			
			| Memory Leak Comparison Tool
			| Scale Configuration Tool

------------------------------------------------------------

Work In Progress:
			| 2 CEF
			| 3 Install
			----| 1 Failed Install (eXR)""")
			return
	if len(sys.argv) > 1:
		is_error = True
	else:
		for arg in sys.argv:
			if arg.startswith('-'):
				is_error = True

	if is_error:
		print(str(sys.argv))
		print("Usage: python3 {" + sys.argv[0] + "} [--file <filename>][--ipv4addr <ipv4 address>][--username <username>](--ssh)(--timeout <seconds>)")
		print("Usage: python3 {" + sys.argv[0] + "} [--memcompare][--pre <filename>][--post <filename>]")
		print("Usage: python3 {" + sys.argv[0] + "} [--config][--file <filename>]")
		print("\n")
		print("""Current Working Modules:
			| 1 L2VPN
			----| 1 AC Down / Unresolved
			----| 2 AC Traffic Loss
			----| 3 PW Down
			| 3 Install
			----| 1 Failed Install (cXR)
			| 4 Memory
			---- | 1 Memory Leak
			| 5 High CPU
			
			| Memory Leak Comparison Tool
			| Scale Configuration Tool

------------------------------------------------------------

Work In Progress:
			| 2 CEF
			| 3 Install
			----| 1 Failed Install (eXR)""")
		return
	else:
		if memcompare == True:
			if pre_file:
				print("Pre Filename: " + pre_file)
			else:
				print("Please use --pre and select a filename")
				return
			if post_file:
				print("Post Filename: " + post_file)
			else:
				print("Please use --post and select a filename")
				return
		elif config == True:
			if file:
				print("Configuration file: " + file)
			else:
				print("Please use --file and select a filename")
				return
		else:
			if file:
				filename = file
				print("Filename: " + filename)
			elif not file:
				print("Please use --file and select a filename")
				return
			if not username:
				print("Please use --username and enter a username")
				return
			if not ipv4_addr:
				print("Please use --ipv4addr and enter the routers ipv4 address")
				return
			if not timeout:
				print("Timeout of command gathering set to default of 10s")
				timeout = 10
			else:
				if timeout < 1:
					print("Invalid timeout, enter '1' or greater")
					return
				print("Timeout of command gathering set to " + str(timeout))
	if memcompare == True:
		option = input("Which type of XR OS are you using?\n" +
		"1 cXR/32-bit\n" + "2 eXR/XR7/64-bit\n" + "Please enter number: ")
		if option == '1':
			print("Memory comparison results if any with difference +1M or higher or a new/deleted PC address:")
			memoryheapcomparisoncxr(pre_file, post_file)
		elif option == '2':
			print("Memory comparison results if any with difference +1M or higher or a new/deleted PC address:")
			memoryheapcomparisonexr(pre_file, post_file)
		else:
			print("Please enter a valid option")
			return
		return
	if config == True:
		Scale_Configurator(file)
		return
	if ipv4_addr and username:
		if os.path.isfile(filename):
			print("Filename exists, please choose a non-existing filename")
			return
		outfile = open(filename, "a+")
		print("Proceeding with login to router")
		password = getpass.getpass(prompt="Please enter your password:")
		#######
		# SSH #
		#######
		if ssh:
			try:
				sshconnect(ipv4_addr, username, password, outfile, timeout)
			except Exception as e:
				print("SSH error " + str(e))
				return()
		##########
		# Telnet #
		##########
		else:
			try:
				print("Trying telnet")
				telnetconnect(ipv4_addr, username, password, outfile, timeout)
			except Exception as e:
				print("Telnet error " + str(e))
				return
	else:
		print("Field(s) are missing for logging into the router")
		return
def sshconnect(ipv4_addr, username, password, outfile, timeout):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#ssh login and actions
	job_id = ''
	process_high_cpu = []
	job_id_list = []
	connection = pexpect.spawn('ssh %s@%s' % (username, ipv4_addr), timeout=300, maxread=1)
	i = connection.expect (['Permission denied|permission denied', 'Terminal type|terminal type', pexpect.EOF, pexpect.TIMEOUT,'connection closed by remote host', 'continue connecting (yes/no)?', 'assword:', 'Authentication failed'],  timeout=30)
	if i == 0:
		print("permission denied")
		sys.exit(3)
	elif i == 1:
		print("terminal type")
		print(connection.before)
		print(connection.after)
		sys.exit(3)
	elif i == 4:
		print("connection closed by host")
		print(connection.before)
		print(connection.after)
		sys.exit(3)
	elif i == 5:
		connection.sendline('yes')
		connection.expect('.* password:')
	elif i == 7:
		print("Authentication failure")
		sys.exit(3)
	connection.sendline(password)
	i = connection.expect(['Permission denied|permission denied', r'RP\S+#'])
	if i == 0:
		print("permission denied")
		sys.exit(3)
	connection.sendline(b"term len 0")
	connection.expect(r'RP\S+#')
	connection.sendline(b"term width 0")
	connection.expect(r'RP\S+#')
	outfile.write("**********")
	connection.sendline(b"show version")
	connection.expect(r'RP\S+#')
	data = connection.before
	data += connection.after
	data = data.decode('utf-8')
	outfile.write(data)
	if 'cisco ASR9K' in data:
		device = 'asr9k'
	elif 'isco CRS' in data:
		device = 'crs'
	elif 'cisco NCS-5500' in data:
		device = 'ncs5500'
	elif 'cisco NCS-6000' in data:
		device = 'ncs6k'
	if '/opt/cisco/XR/packages/' in data:
		xr_type = 'eXR'
	else:
		xr_type = 'cXR'
	option = input("What would you like to troubleshoot?\n" +
	"1 L2VPN\n" + "2 CEF\n" + "3 Install\n" + "4 Memory\n" +
	"5 High CPU\n" + "Please enter number: ")
	if option == '1':
		commands, sub_option, option_loc, option_int, option_bd, option_pw, option_pw_id = l2vpn()
	elif option == '2':
		commands = cef()
	elif option == '3':
		commands, sub_option, option_id = install()
	elif option == '4':
		commands, sub_option, option_id, option_loc = memory()
	elif option == '5':
		commands, option_loc = high_cpu()
	else:
		print(option)
		print("Invalid option, quitting")
		sys.exit(3)
	commands_len = len(commands)
	i = 0
	print("Beginning stage 1 data collection")
	for command in commands:
		i += 1
		connection.sendline(command.encode('utf-8'))
		data = ""
		n = 1
		while n == 1:
			try:
				data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
			except pexpect.exceptions.TIMEOUT:
				n = 0
		if option == '4':
			if 'show process' in command:
				regex_string = re.compile('Job Id: (\d+)')
				match = regex_string.search(data)
				if match:
					job_id = str(match.group(1))
		elif option == '5':
			if "show process cpu" in command:
				data2 = data.split("\n")
				regex_string = re.compile('^(\d+)\s+([3-9]\d%\s+[2-9]\d%)\s+\d+%\s+(\S+)')
				for line in data2:
					match = regex_string.search(line)
					if match:
						process_high_cpu.append(line)
		outfile.write(data)
		print("Command " + str(i) + " of " + str(commands_len) + " complete")
	i = 0
	outfile.seek(0, 0)	
	pre_commands = {}
	for line in outfile:                   
		try:
			if str(commands[i]) in line:
				print("found " + str(commands[i]))
				command = str(commands[i])
				if command not in pre_commands.keys():
					pre_commands[command] = [command]
				i += 1
			else:
				pre_commands[command].append(line)
		except IndexError:
			pre_commands[command].append(line)
		except Exception as e:
			pass
	else:
		if i == len(commands):
			print("found all commands")
		else:
			i += 1
			print("found " + str(i) + " commands of " + str(len(commands)+1))
	if option == '1':
		l2vpn_parser(commands, sub_option, option_loc, option_int, option_bd, option_pw, option_pw_id, pre_commands)
	elif option == '3':
		install_parser(commands, sub_option, xr_type, pre_commands)
	elif option == '4':
		if sub_option == '1':
			print("Beginning stage 2 of 2 data collection")
			commands = []
			if xr_type == 'cXR':
				commands.append("show memory heap dllname " + job_id + " location " + option_loc)
			elif xr_type == 'eXR':
				commands.append("show memory heap dllname jid " + job_id + " location " + option_loc)
			commands_len = len(commands)
			i = 0
			for command in commands:
				i += 1
				connection.sendline(command.encode('utf-8', 'ignore'))
				data = ""
				n = 1
				while n == 1:
					try:
						data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
					except pexpect.exceptions.TIMEOUT:
						n = 0
				outfile.write(data)
				print("Command " + str(i) + " of " + str(commands_len) + " complete")
			i = 0
			outfile.seek(0, 0)	
			pre_commands = {}
			for line in outfile:                   
				try:
					if str(commands[i]) in line:
						print("found " + str(commands[i]))
						command = str(commands[i])
						if command not in pre_commands.keys():
							pre_commands[command] = [command]
						i += 1
					else:
						pre_commands[command].append(line)
				except IndexError:
					pre_commands[command].append(line)
				except Exception as e:
					pass
			else:
				if i == len(commands):
					print("found all commands")
				else:
					i += 1
					print("found " + str(i) + " commands of " + str(len(commands)+1))
		else:
			memory_parser(commands, sub_option, xr_type, pre_commands)
	elif option == '5':
		commands = []
		if len(process_high_cpu) > 0:
			print("Beginning stage 2 of 3 data collection")
			commands.append('show process blocked location ' + option_loc)
			for i in process_high_cpu:
				regex_string = re.compile('^(\d+)\s+([3-9]\d%\s+[2-9]\d%)\s+\d+%\s+(\S+)')
				match = regex_string.search(i)
				if match:
					process = str(match.group(3))
					pid = str(match.group(1))
					commands.append("show process " + process + ' location ' + option_loc)
					commands.append("follow process " + pid + ' location ' + option_loc)
					if xr_type == 'eXR':
						commands.append("show process memory " + pid + ' location ' + option_loc)
			commands_len = len(commands)
			i = 0
			for command in commands:
				i += 1
				connection.sendline(command.encode('utf-8', 'ignore'))
				data = ""
				n = 1
				while n == 1:
					try:
						data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
					except pexpect.exceptions.TIMEOUT:
						n = 0
				if 'show process' in command:
					regex_string = re.compile('Job Id: (\d+)')
					match = regex_string.search(data)
					if match:
						job_id_list.append(str(match.group(1)))
				outfile.write(data)
				print("Command " + str(i) + " of " + str(commands_len) + " complete")
			i = 0
			outfile.seek(0, 0)	
			pre_commands = {}
			for line in outfile:                   
				try:
					if str(commands[i]) in line:
						print("found " + str(commands[i]))
						command = str(commands[i])
						if command not in pre_commands.keys():
							pre_commands[command] = [command]
						i += 1
					else:
						pre_commands[command].append(line)
				except IndexError:
					pre_commands[command].append(line)
				except Exception as e:
					pass
			else:
				if i == len(commands):
					print("found all commands")
				else:
					i += 1
					print("found " + str(i) + " commands of " + str(len(commands)+1))
			commands = []
			print("Beginning stage 3 of 3 data collection")
			commands.append('show process memory location ' + option_loc)
			for i in job_id_list:
				commands.append("show process file " + i + ' detail location ' + option_loc)
				if xr_type == 'cXR':
					commands.append("show process memory " + i + ' location ' + option_loc)
					commands.append("show memory heap dllname " + i + " location " + option_loc)
				elif xr_type == 'eXR':
					commands.append("show memory heap dllname jid " + i + " location " + option_loc)
			commands_len = len(commands)
			i = 0
			for command in commands:
				i += 1
				connection.sendline(command.encode('utf-8', 'ignore'))
				data = ""
				n = 1
				while n == 1:
					try:
						data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
					except pexpect.exceptions.TIMEOUT:
						n = 0
				outfile.write(data)
				print("Command " + str(i) + " of " + str(commands_len) + " complete")
			i = 0
			outfile.seek(0, 0)	
			pre_commands = {}
			for line in outfile:                   
				try:
					if str(commands[i]) in line:
						print("found " + str(commands[i]))
						command = str(commands[i])
						if command not in pre_commands.keys():
							pre_commands[command] = [command]
						i += 1
					else:
						pre_commands[command].append(line)
				except IndexError:
					pre_commands[command].append(line)
				except Exception as e:
					pass
			else:
				if i == len(commands):
					print("found all commands")
				else:
					i += 1
					print("found " + str(i) + " commands of " + str(len(commands)+1))
		else:
			print("No high CPU found")
	connection.close()
	outfile.close()
def telnetconnect(ipv4_addr, username, password, outfile, timeout):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#telnet login and actions
	job_id = ''
	process_high_cpu = []
	job_id_list = []
	connection = pexpect.spawn('telnet ' + ipv4_addr, timeout=300, maxread=1)
	connection.expect('Username:')
	connection.sendline(username)
	connection.expect('assword:')
	connection.sendline(password)
	i = connection.expect(['Username:', r'RP\S+#'])
	if i == 0:
		print("permission denied")
		sys.exit(3)
	connection.sendline(b"term len 0")
	connection.expect(r'RP\S+#')
	connection.sendline(b"term width 0")
	connection.expect(r'RP\S+#')
	outfile.write("**********")
	connection.sendline(b"show version")
	connection.expect(r'RP\S+#')
	data = connection.before
	data += connection.after
	data = data.decode('utf-8')
	if 'cisco ASR9K' in data:
		device = 'asr9k'
	elif 'isco CRS' in data:
		device = 'crs'
	elif 'cisco NCS-5500' in data:
		device = 'ncs5500'
	elif 'cisco NCS-6000' in data:
		device = 'ncs6k'
	if '/opt/cisco/XR/packages/' in data:
		xr_type = 'eXR'
	else:
		xr_type = 'cXR'
	option = input("What would you like to troubleshoot?\n" +
	"1 L2VPN\n" + "2 CEF\n" + "3 Install\n" + "4 Memory\n" +
	"5 High CPU\n" + "Please enter number: ")
	if option == '1':
		commands, sub_option, option_loc, option_int, option_bd, option_pw, option_pw_id = l2vpn()
	elif option == '2':
		commands = cef()
	elif option == '3':
		commands, sub_option, option_id = install()
	elif option == '4':
		commands, sub_option, option_id, option_loc = memory()
	elif option == '5':
		commands, option_loc = high_cpu()
	else:
		print(option)
		print("Invalid option, quitting")
		sys.exit(3)
	commands_len = len(commands)
	i = 0
	print("Beginning stage 1 data collection")
	for command in commands:
		i += 1
		connection.sendline(command.encode('utf-8'))
		data = ""
		n = 1
		while n == 1:
			try:
				data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
			except pexpect.exceptions.TIMEOUT:
				n = 0
		if option == '4':
			if 'show process' in command:
				regex_string = re.compile('Job Id: (\d+)')
				match = regex_string.search(data)
				if match:
					job_id = str(match.group(1))
		elif option == '5':
			if "show process cpu" in command:
				data2 = data.split("\n")
				regex_string = re.compile('^(\d+)\s+([3-9]\d%\s+[2-9]\d%)\s+\d+%\s+(\S+)')
				for line in data2:
					match = regex_string.search(line)
					if match:
						process_high_cpu.append(line)
		outfile.write(data)
		print("Command " + str(i) + " of " + str(commands_len) + " complete")
	i = 0
	outfile.seek(0, 0)	
	pre_commands = {}
	for line in outfile:                   
		try:
			if str(commands[i]) in line:
				print("found " + str(commands[i]))
				command = str(commands[i])
				if command not in pre_commands.keys():
					pre_commands[command] = [command]
				i += 1
			else:
				pre_commands[command].append(line)
		except IndexError:
			pre_commands[command].append(line)
		except Exception as e:
			pass
	else:
		if i == len(commands):
			print("found all commands")
		else:
			i += 1
			print("found " + str(i) + " commands of " + str(len(commands)+1))
	if option == '1':
		l2vpn_parser(commands, sub_option, option_loc, option_int, option_bd, option_pw, option_pw_id, pre_commands)
	elif option == '3':
		install_parser(commands, sub_option, xr_type, pre_commands)
	elif option == '4':
		if sub_option == '1':
			print("Beginning stage 2 of 2 data collection")
			commands = []
			if xr_type == 'cXR':
				commands.append("show memory heap dllname " + job_id + " location " + option_loc)
			elif xr_type == 'eXR':
				commands.append("show memory heap dllname jid " + job_id + " location " + option_loc)
			commands_len = len(commands)
			i = 0
			for command in commands:
				i += 1
				connection.sendline(command.encode('utf-8', 'ignore'))
				data = ""
				n = 1
				while n == 1:
					try:
						data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
					except pexpect.exceptions.TIMEOUT:
						n = 0
				outfile.write(data)
				print("Command " + str(i) + " of " + str(commands_len) + " complete")
			i = 0
			outfile.seek(0, 0)	
			pre_commands = {}
			for line in outfile:                   
				try:
					if str(commands[i]) in line:
						print("found " + str(commands[i]))
						command = str(commands[i])
						if command not in pre_commands.keys():
							pre_commands[command] = [command]
						i += 1
					else:
						pre_commands[command].append(line)
				except IndexError:
					pre_commands[command].append(line)
				except Exception as e:
					pass
			else:
				if i == len(commands):
					print("found all commands")
				else:
					i += 1
					print("found " + str(i) + " commands of " + str(len(commands)+1))
		else:
			memory_parser(commands, sub_option, xr_type, pre_commands)
	elif option == '5':
		commands = []
		if len(process_high_cpu) > 0:
			print("Beginning stage 2 of 3 data collection")
			commands.append('show process blocked location ' + option_loc)
			for i in process_high_cpu:
				regex_string = re.compile('^(\d+)\s+([3-9]\d%\s+[2-9]\d%)\s+\d+%\s+(\S+)')
				match = regex_string.search(i)
				if match:
					process = str(match.group(3))
					pid = str(match.group(1))
					commands.append("show process " + process + ' location ' + option_loc)
					commands.append("follow process " + pid + ' location ' + option_loc)
					if xr_type == 'eXR':
						commands.append("show process memory " + pid + ' location ' + option_loc)
			commands_len = len(commands)
			i = 0
			for command in commands:
				i += 1
				connection.sendline(command.encode('utf-8', 'ignore'))
				data = ""
				n = 1
				while n == 1:
					try:
						data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
					except pexpect.exceptions.TIMEOUT:
						n = 0
				if 'show process' in command:
					regex_string = re.compile('Job Id: (\d+)')
					match = regex_string.search(data)
					if match:
						job_id_list.append(str(match.group(1)))
				outfile.write(data)
				print("Command " + str(i) + " of " + str(commands_len) + " complete")
			i = 0
			outfile.seek(0, 0)	
			pre_commands = {}
			for line in outfile:                   
				try:
					if str(commands[i]) in line:
						print("found " + str(commands[i]))
						command = str(commands[i])
						if command not in pre_commands.keys():
							pre_commands[command] = [command]
						i += 1
					else:
						pre_commands[command].append(line)
				except IndexError:
					pre_commands[command].append(line)
				except Exception as e:
					pass
			else:
				if i == len(commands):
					print("found all commands")
				else:
					i += 1
					print("found " + str(i) + " commands of " + str(len(commands)+1))
			commands = []
			print("Beginning stage 3 of 3 data collection")
			commands.append('show process memory location ' + option_loc)
			for i in job_id_list:
				commands.append("show process file " + i + ' detail location ' + option_loc)
				if xr_type == 'cXR':
					commands.append("show process memory " + i + ' location ' + option_loc)
					commands.append("show memory heap dllname " + i + " location " + option_loc)
				elif xr_type == 'eXR':
					commands.append("show memory heap dllname jid " + i + " location " + option_loc)
			commands_len = len(commands)
			i = 0
			for command in commands:
				i += 1
				connection.sendline(command.encode('utf-8', 'ignore'))
				data = ""
				n = 1
				while n == 1:
					try:
						data += connection.read_nonblocking(size=999,timeout=timeout).decode('utf-8', 'ignore')
					except pexpect.exceptions.TIMEOUT:
						n = 0
				outfile.write(data)
				print("Command " + str(i) + " of " + str(commands_len) + " complete")
			i = 0
			outfile.seek(0, 0)	
			pre_commands = {}
			for line in outfile:                   
				try:
					if str(commands[i]) in line:
						print("found " + str(commands[i]))
						command = str(commands[i])
						if command not in pre_commands.keys():
							pre_commands[command] = [command]
						i += 1
					else:
						pre_commands[command].append(line)
				except IndexError:
					pre_commands[command].append(line)
				except Exception as e:
					pass
			else:
				if i == len(commands):
					print("found all commands")
				else:
					i += 1
					print("found " + str(i) + " commands of " + str(len(commands)+1))
		else:
			print("No high CPU found")
	connection.close()
	outfile.close()
class DictDiffer(object):
	"""
	Calculate the difference between two dictionaries as:
	(1) items added
	(2) items removed
	(3) keys same in both but changed values
	(4) keys same in both and unchanged values
	"""
	def __init__(self, current_dict, past_dict):
		self.current_dict, self.past_dict = current_dict, past_dict
		self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
		self.intersect = self.set_current.intersection(self.set_past)
	def added(self):
		return self.set_current - self.intersect 
	def removed(self):
		return self.set_past - self.intersect 
	def changed(self):
		return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
	def unchanged(self):
		return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
def get_changes(the_diffs, my_set, my_set2 = None):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2020 (C) Cisco TAC"
	###__version__    = "1.0.1"
	###__status__     = "alpha"
	#Here we need to see if we have a dictionary inside of a dictionary
	#or a flat dictionary and then check for diffs
	diff_info = []
	if not the_diffs:
		diff_info.append('None\n')
	elif not my_set2:
		for entry in the_diffs:
			diff_info.append("{}: ".format(entry))
			try:
				for key, value in my_set[entry].items():
					try:
						diff_info.append("'{}: {}' ".format(key, value))
					except Exception as e:
						pass
			except Exception as e:
				diff_info.append(str(my_set[entry]) + " ")
	else:
		for entry in the_diffs:
			diff_info.append("\nBefore:\n {}: ".format(entry))
			try:
				for key, value in my_set[entry].items():
					value3 = my_set[entry][key]
					try:
						value2 = my_set2[entry][key]
						if value2 != value3:
							diff_info.append("'{}: {}' ".format(key, value))
					except Exception as e:
						diff_info.append("'{}: {}' ".format(key, value))
			except Exception as e:
				diff_info.append(str(my_set[entry]) + " ")
			diff_info.append("\nAfter:\n {}: ".format(entry))
			try:
				for key, value in my_set2[entry].items():
					value3 = my_set2[entry][key]
					try:
						value2=my_set[entry][key]
						if value2 != value3:
							diff_info.append("'{}: {}' ".format(key, value))
					except Exception as e:
						diff_info.append("'{}: {}' ".format(key, value))
			except Exception as e:
				diff_info.append(str(my_set2[entry]) + " ")
	return diff_info
def memoryheapcomparisoncxr(pre_file, post_file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.1"
	###__status__     = "maintenance"
	#calculate any memory changes 1M+ in cXR
	regexp = re.compile(r"(0x[\da-f]+)\s(0x[\da-f]+)\s(0x[\da-f]+)\s(.*)")
	dict1 = {}
	with open(pre_file) as f:
		for line in f:
			match = regexp.match(line)
			if match:
				dict1[match.group(4)] = int(match.group(2), 16) // (1024*1024)
	dict2 = {}
	with open(post_file) as f:
		for line in f:
			match = regexp.match(line)
			if match:
				dict2[match.group(4)] = int(match.group(2), 16) // (1024*1024)
	the_diffs = DictDiffer(dict2, dict1)
	print("PC Address and Fuction Name                   Size in MB\n")
	print('\nThe following items were added:\n')
	added = (get_changes(the_diffs.added(), dict2))
	j =0
	for i in added:
		if j == 1:
			print(temp + i)
			j = 0
		else:
			j = 1
			temp = i
	print('\nThe following items were deleted:\n')
	deleted = (get_changes(the_diffs.removed(), dict1))
	j =0
	for i in deleted:
		if j == 1:
			print(temp + i)
			j = 0
		else:
			j = 1
			temp = i
	print("\nThe changed items were:\n")
	changed = (get_changes(the_diffs.changed(), dict1, dict2))
	j =0
	for i in changed:
		if j == 1:
			print(temp + i)
			j = 0
		else:
			j = 1
			temp = i
	return
def memoryheapcomparisonexr(pre_file, post_file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.1"
	###__status__     = "maintenance"
	#calculate any memory changes 1M+ in eXR/XR7
	regexp = re.compile(r"(0x[\da-f]+)\s+(\d+)\s+(\d+)\s(.*)")
	dict1 = {}
	with open(pre_file) as f:
		for line in f:
			match = regexp.match(line)
			if match:
				dict1[match.group(1) + ' ' + match.group(4)] = int(match.group(3)) // (1024 * 1024)
	dict2 = {}
	with open(post_file) as f:
		for line in f:
			match = regexp.match(line)
			if match:
				dict2[match.group(1) + ' ' + match.group(4)] = int(match.group(3)) // (1024 * 1024)
	the_diffs = DictDiffer(dict2, dict1)
	print("PC Address and Fuction Name                   Size in MB\n")
	print('\nThe following items were added:\n')
	added = (get_changes(the_diffs.added(), dict2))
	j =0
	for i in added:
		if j == 1:
			print(temp + i)
			j = 0
		else:
			j = 1
			temp = i
	print('\nThe following items were deleted:\n')
	deleted = (get_changes(the_diffs.removed(), dict1))
	j =0
	for i in deleted:
		if j == 1:
			print(temp + i)
			j = 0
		else:
			j = 1
			temp = i
	print("\nThe changed items were:\n")
	changed = (get_changes(the_diffs.changed(), dict1, dict2))
	j =0
	for i in changed:
		if j == 1:
			print(temp + i)
			j = 0
		else:
			j = 1
			temp = i
	return     
def Scale_Configurator(file):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.2"
	###__status__     = "alpha"
	#generate configuration file
	"""This script is designed to generate scale configurations.
		
		1. For numbers
		Ranges such as [10-50] will automatically increment by 1.
		For a different multiplier use a ',' such as [10-50,5].
		
		2. For hex
		Ranges such as {0-a} or {0-A} will automatically increment by 1.
		For a different multiplier use a ',' such as {0-A,5}.
		Case insensitive
		
		3. For letters
		Ranges such as (a-g) or (A-G) will automatically increment by 1.
		For a different multiplier use a ',' such as (a-g,5).
		Case sensitive
		
		Returns:
		- Scale config to terminal.

		###Example###
		Example Times to Run: 3

		Example File:
		interface GigabitEthernet0/0/0/13.[1-200] l2transport
		 vrf vrf(a-e,3)
		 encapsulation dot1Q [1-200] second-dot1q [30-35,3] exact
		 ipv6 address 2001::{0-f,7}/26
		 no shut
		!

		Example Output:
		interface GigabitEthernet0/0/0/13.1 l2transport
		 vrf vrfa
		 encapsulation dot1Q 1 second-dot1q 30 exact
		 ipv6 address 2001::0/26
		 no shut
		!
		interface GigabitEthernet0/0/0/13.2 l2transport
		 vrf vrfd
		 encapsulation dot1Q 2 second-dot1q 33 exact
		 ipv6 address 2001::7/26
		 no shut
		!
		interface GigabitEthernet0/0/0/13.3 l2transport
		 vrf vrfb
		 encapsulation dot1Q 3 second-dot1q 30 exact
		 ipv6 address 2001::E/26
		 no shut
		!
		"""
	option = int(input("How many times would you like to iterate through the configuration\n" + "Please enter number: "))
	if option < 1:
		print("Enter a valid number of times to run")
		return
	else:
		timestorun = option
	with open(file, "r") as myfile:
		textarea = myfile.read()
	# Call the function to do the parsing
	parse(textarea, timestorun)
def parse(textarea, timestorun):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.2"
	###__status__     = "alpha"
	"""
		Create the finaloutput list, parse line by line for the number of times specified
		and return final output
				##################################################
				#initalsplit is used to split the string into two#
				#list values before the '[' and after '['        #
				##################################################
					##############################################
					#From the second part of this array we set   #
					#bracketsandend to give us the value inside  #
					#the []s and then the outer string as [1]    #
					##############################################
						###################################################
						#Next we need to do one more split. This allows us#
						#to get the value before the - and the value after#
						###################################################
							#########################################################
							#Finally we check if there is a ',' and split this again#
							#so that bracket[1] is changed to increment[0] for      #
							#the end value and increment[1] for the x value         #
							#########################################################
	"""
	x = 0
	# This is where all the magic happens
	while (x < timestorun):
		# Parse line by line
		for line in textarea.split("\n"):
			# Check if any manipulation needs to be done
			if "[" and "]" in line:
				line = parse_numbers(line, x)
			if "{" and "}" in line:
				line = parse_hex(line, x)
			if "(" and ")" in line:
				line = parse_letters(line, x)
			print(line)
		x += 1
	return
def parse_numbers(line, x):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.2"
	###__status__     = "alpha"
	"""
	This is for incrementing base 10
	"""
	increment = 1
	regex_int = re.compile('\[\d+-\d+,?\d+?\]')
	match = re.findall(regex_int, line)
	for i in match:
		match2 = re.search(r'(\[(\d+)-(\d+),?(\d+)?\])',line)
		if match2.group(4):
			increment = int(match2.group(4))
		temp = int(match2.group(2))+(x*increment)
		while temp > int(match2.group(3)):
			temp += int(match2.group(2)) - int(match2.group(3)) -1
		line = re.sub('(\[(\d+)-(\d+),?(\d+)?\])', str(temp), str(line), count=1)
	return line
def parse_hex(line, x):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.2"
	###__status__     = "alpha"
	"""
	This is for incrementing in hex
	"""
	increment = 1
	regex_hex = re.compile('\{[0-9a-fA-F]+-[0-9a-fA-F]+,?\d+?\}')
	match = re.findall(regex_hex, line)
	for i in match:
		match2 = re.search(r'(\{([0-9a-fA-F])+-([0-9a-fA-F])+,?(\d+)?\})', line)
		if match2.group(4):
			increment = int(match2.group(4))
		starthex = int(match2.group(2), 16)
		endhex = int(match2.group(3), 16)
		temp = starthex +(x*increment)
		while temp > endhex:
			temp += starthex - endhex - 1
		temp = '{:X}'.format(temp)
		line = re.sub('(\{([0-9a-fA-F])+-([0-9a-fA-F])+,?(\d+)?\})', str(temp), str(line), count=1)
	return line
def parse_letters(line, x):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.2"
	###__status__     = "alpha"
	"""
	This is for incrementing letters, we must use the ASCII
	representation to do this
	"""
	increment = 1
	regex_letter = re.compile('\([a-zA-Z]+-[a-zA-Z]+,?\d+?\)')
	match = re.findall(regex_letter, line)
	for i in match:
		match2 = re.search(r'(\(([a-zA-Z])+-([a-zA-Z])+,?(\d+)?\))', line)
		startletter = ord(match2.group(2))
		endletter = ord(match2.group(3))
		if match2.group(4):
			increment = int(match2.group(4))
		temp = startletter +(x*increment)
		while temp > endletter:
			temp += startletter - endletter - 1
		temp = str(chr(temp))
		line = re.sub('(\(([a-zA-Z])+-([a-zA-Z])+,?(\d+)?\))', str(temp), str(line), count=1)
	return line
def l2vpn():
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#generate l2vpn commands
	commands = []
	option = ''
	option_loc = ''
	option_int = ''
	option_bd = ''
	option_pw = ''
	option_pw_id = ''
	option = input("Please select how you want to troubleshoot.\n" +
	"1 AC Down / Unresolved\n" + "2 Traffic Loss / Forwarding Verification\n" +
	"3 PW Down\n" + "Please enter the corresponding number: ")
	if option == '1':
		option_int = input("What is the long-form name for the interface? Eg. TenGigE0/4/0/19.1 NOT Te0/4/0/19.1: ")
		option_loc = input("What LC do we want to troubleshoot? Please use the full name such as 0/0/cpu0: ")
		commands.append("show l2vpn database ac interface " + option_int)
		commands.append("show process l2vpn_mgr txgroup peer all detail")
		commands.append("show l2vpn database node")
		commands.append("show proc vlan_ma txgroup peer all detail location " + option_loc)
		commands.append("show ethernet infra internal ether-ma global location " + option_loc)
		commands.append("show ethernet infra internal vlan-ma global location " + option_loc)
	elif option == '2':
		option_int = input("What is the long-form name for the interface? Eg. TenGigE0/4/0/19.1 NOT Te0/4/0/19.1: ")
		option_loc = input("What LC do we want to troubleshoot? Please use the full name such as 0/0/cpu0: ")
		option_bd = input("Please enter the bridge-domain name or press enter for no bridge-domain: ")
		commands.append("show l2vpn forwarding detail loc " + option_loc)
		commands.append("show l2vpn forwarding private loc " + option_loc)
		commands.append("show adjacency loc " + option_loc + " | i " + option_int)
		if '.' in option_int:
			commands.append("show ethernet infra internal vlan-ma subs " + option_int + " loc " + option_loc)
			regex_string = re.compile('(\S+)\.\S+')
			match = regex_string.search(option_int)
			if match:
				commands.append("show ethernet infra internal vlan-ma trunks " + match.group(1) + " loc " + option_loc)
		else:
			commands.append("show ethernet infra internal ether-ma trunks " + option_int + " loc " + option_loc)
		if option_bd != '':
			commands.append("show l2vpn bridge-domain bd-name " + option_bd + " detail")
			option_pw = input("Please enter the PW neighbor IP address or press enter for no PW: ")
	elif option == '3':
		option_pw = input("Please enter the PW neighbor IP address: ")
		option_pw_id = input("Please enter the PW-ID: ")
		option_xc_bd = input("Please select how to troubleshoot.\n" +
			"1 p2p xconnect PW\n" + "2 Bridge-domain PW\n")
		if option_xc_bd == '1':
			commands.append("show l2vpn xconnect pw-id " + option_pw_id + " detail")
			commands.append("show l2vpn xconnect pw-id " + option_pw_id + " private")
		elif option_xc_bd == '2':
			commands.append("show l2vpn bridge-domain pw-id " + option_pw_id + " detail")
			commands.append("show l2vpn bridge-domain pw-id " + option_pw_id + " private")
		else:
			print("Invalid selection, quitting")
			sys.exit(3)
	else:
		print("Invalid option, quitting")
		sys.exit(3)
	return(commands, option, option_loc, option_int, option_bd, option_pw, option_pw_id)
def install(option_id, option_loc):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#generate install commands
	commands = []
	option = ''
	option_id = ''
	option = input("Please select how you want to troubleshoot.\n" +
	"1 Failed Install\n" + "Please enter the corresponding number: ")
	if option == '1':
		option_id = input("What is the install 'ID' that failed? ")
		commands.append("show install log " + option_id + " detail")
	else:
		print("Invalid option, quitting")
		sys.exit(3)
	return(commands, option, option_id)
def memory():
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#generate memory commands
	commands = []
	option = ''
	option_id = ''
	option = input("Please select how you want to troubleshoot.\n" +
	"1 Memory Leak\n" + "Please enter the corresponding number: ")
	if option == '1':
		option_id = input("What is the process name? ")
		option_loc = input("What is the RP/LC location the process is hosted on? IE 0/RP0/CPU0: ")
		commands.append("show process " + option_id + " location " + option_loc)
	else:
		print("Invalid option, quitting")
		sys.exit(3)
	return(commands, option, option_id, option_loc)
def high_cpu():
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#generate commands to check for high cpu
	commands = []
	option_loc = input("What is the RP/LC location showing high CPU? IE 0/RP0/CPU0: ")
	commands.append("show process cpu location " + option_loc)
	return(commands, option_loc)
def l2vpn_parser(commands, sub_option, option_loc, option_int, option_bd, option_pw, option_pw_id, command_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse l2vpn commands	
	option_loc_cap = option_loc.upper()
	for command in commands:
		pre_list = []
		result = ''
		response = ''
		try:
			for value in command_dict[command]:
				pre_list.append(value)
		except Exception as e:
			continue	
		if sub_option == '1':
			if 'show l2vpn database ac' in command:
				show_l2vpn_database_ac(pre_list)
			elif 'show process l2vpn_mgr txgroup peer all detail' in command:
				show_process_l2vpn_mgr_txgroup_peer_all_detail(option_loc_cap, pre_list)
			elif 'show l2vpn database node' in command:
				show_l2vpn_database_node(option_loc_cap, pre_list)
			elif 'show proc vlan_ma txgroup peer all detail' in command:
				show_proc_vlan_ma_txgroup_peer_all_detail_loc(option_loc_cap, pre_list)
			elif 'show ethernet infra internal ether-ma global location' in command:
				show_ethernet_infra_internal_ether_ma_global_loc(pre_list)
			elif 'show ethernet infra internal vlan-ma global location' in command:
				show_ethernet_infra_internal_vlan_ma_global_loc(pre_list)
		elif sub_option == '2':
			if 'show l2vpn forwarding detail loc' in command:
				print("[INFO] AC interface is: " + option_int)
				print("[INFO] Location is: " + option_loc)
				xconnect_id = show_l2vpn_forwarding_detail_loc(option_int, pre_list)
			elif 'show l2vpn forwarding private loc' in command:
				show_l2vpn_forwarding_private_loc(xconnect_id, pre_list)
			elif 'show adjacency loc' in command:
				show_adjacency_loc(pre_list)
			elif 'show ethernet infra internal vlan-ma subs loc' in command:
				show_ethernet_infra_internal_vlan_ma_subs_loc(pre_list)
			elif 'show ethernet infra internal vlan-ma trunks loc' in command:
				show_ethernet_infra_internal_vlan_ma_trunks_loc(pre_list)
			elif 'show ethernet infra internal ether-ma trunks loc' in command:
				show_ethernet_infra_internal_ether_ma_trunks_loc(pre_list)
			elif 'show l2vpn bridge-domain' in command:
				show_l2vpn_bridge_domain(option_int, xconnect_id, option_pw, pre_list)
		elif sub_option == '3':
			if ('show l2vpn xconnect pw-id' in command) and ('private' in command):
				show_l2vpn_xconnect_pw_id_private(option_pw, option_pw_id, pre_list)
			elif ('show l2vpn xonnect pw-id' in command) and ('detail' in command):
				show_l2vpn_xconnect_pw_id_detail(option_pw, option_pw_id, pre_list)
			elif ('show l2vpn bridge-domain pw-id' in command) and ('private' in command):
				show_l2vpn_bridge_domain_pw_id_private(option_pw, option_pw_id, pre_list)
			elif ('show l2vpn bridge-domain pw-id' in command) and (' detail' in command):
				show_l2vpn_bridge_domain_pw_id_detail(option_pw, option_pw_id, pre_list)
	return
def install_parser(commands, sub_option, xr_type, command_dict):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse install commands	
	for command in commands:
		pre_list = []
		result = ''
		response = ''
		try:
			for value in command_dict[command]:
				pre_list.append(value)
		except Exception as e:
			continue	
		if sub_option == 1:
			if 'show install log' in command:
				if xr_type == 'eXR':
					show_install_log_exr(pre_list)
				elif xr_type == 'cXR':
					show_install_log_cxr(pre_list)
	return
def show_adjacency_loc(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show adjacency
	for line in pre_list:
		line = line.strip()
		regex_string = re.compile('\S+\s+\S+\s+\d+\s+\d+\(.*\s+(\S+$)')
		match = regex_string.search(line)
		if match:
			ac_adj = match.group(1)
			print("[INFO] AC Adjacency Type: " + str(ac_adj))
	return
def show_ethernet_infra_internal_ether_ma_global_loc(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show ethernet infra internal ether-ma global loc
	for line in pre_list:
		regex_string = re.compile('Conn is up:\s+(\S+)')
		match = regex_string.search(line)
		if match:
			if 'Yes' in match.group(1):
				print("[INFO] L2VPN connection is up")
			else:
				print("[WARNING] L2VPN connection is not up, it is " + match.group(1))
		regex_string = re.compile('First Sync pending:\s+(\S+)')
		match = regex_string.search(line)
		if match:
			if 'No' in match.group(1):
				print("[INFO] First sync is complete")
			else:
				print("[WARNING] L2VPN first sync is pending")
	return
def show_ethernet_infra_internal_ether_ma_trunks_loc(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show ethernet infra internal ether-ma trunks loc
	for line in pre_list:
		regex_string = re.compile('interface_ready: (\S+)')
		match = regex_string.search(line)
		if match:
			ether_ready = match.group(1)
			print("Ether Interface Ready: " + ether_ready)
		regex_string = re.compile('Internal Interface State: (.*$)')
		match = regex_string.search(line)
		if match:
			internal_int_state = match.group(1)
			if 'Up' in internal_int_state:
				print("[INFO] Internal Interface State: " + internal_int_state)
			else:
				print("[WARNING] Internal Interface State: " + internal_int_state)
	return
def show_ethernet_infra_internal_vlan_ma_global_loc(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show ethernet infra internal vlan-ma global loc
	init_sync_found = False
	for line in pre_list:
		regex_string = re.compile('VLAN MA is Active:\s+(\S+)')
		match = regex_string.search(line)
		if match:
			if 'Yes' in match.group(1):
				print("[INFO] VLAN MA is active")
			else:
				print("[WARNING] VLAN MA is not active")
		regex_string = re.compile('VLAN MA has reached initial synchronization')
		match = regex_string.search(line)
		if match:
			print("[INFO] VLAN MA has reached initial sync")
			init_sync_found = True
		regex_string = re.compile('L2VPN Mgr connection is (\S+)')
		match = regex_string.search(line)
		if match:
			if 'UP' in match.group(1):
				print("[INFO] L2VPN mgr connection is UP")
			else:
				print("[WARNING] L2VPN mgr connection is " + match.group(1))
		regex_string = re.compile('ERROR')
		match = regex_string.search(line)
		if match:
			print("[WARNING] Error found: " + line)		
	if init_sync_found == False:
		print("[WARNING] VLAN MA has not reached initial sync")
	return
def show_ethernet_infra_internal_vlan_ma_subs_loc(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show ethernet infra internal vlan-ma subs loc
	for line in pre_list:
		regex_string = re.compile('sub\.admin_up: (\S+)')
		match = regex_string.search(line)
		if match:
			sub_admin = match.group(1)
			print("AC Sub Admin State: " + sub_admin)
	return
def show_ethernet_infra_internal_vlan_ma_trunks_loc(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show ethernet infra internal vlan-ma trunks loc
	for line in pre_list:
		regex_string = re.compile('State is (\S+)')
		match = regex_string.search(line)
		if match:
			trunk_state = match.group(1)
			if 'up' in match.group(1):
				print("[INFO] Trunk State: " + trunk_state)
			else:
				print("[WARNING] Trunk State: " + trunk_state)
	return
def show_l2vpn_bridge_domain(option_int, xconnect_id, option_pw, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn bridge domain    			
	ac_found = False
	pw_found = False
	pw_tlv_found = False
	incoming_tlv = False
	outgoing_tlv = False
	for line in pre_list:
		regex_string = re.compile('AC: %s, state is (.*$)' % (option_int))
		match = regex_string.search(line)
		if match:
			ac_state = match.group(1)
			if 'up' in ac_state:
				print("[INFO] AC State: " + ac_state)
			else:
				print("[WARNING] AC State: " + ac_state)
			ac_found = True
		else:
			regex_string = re.compile('AC:')
			match = regex_string.search(line)
			if match:
				ac_found = False
		if ac_found == True:
			regex_string = re.compile('MTU \d+; XC ID (\S+);')
			match = regex_string.search(line)
			if match:
				if match.group(1) == xconnect_id:
					print("[INFO] Xconnect ID matches")
				else:
					print("[WARNING] Xconnect ID in hardware (" + xconnect_id + ") does not match xconnect ID in software (" + match.group(1) + ")")
			regex_string = re.compile('Error: (.*$)')
			match = regex_string.search(line)
			if match:
				print("[ERROR] Error on AC detected " + match.group(1))
		regex_string = re.compile('PW: neighbor %s, PW ID \S+, state is (.*)' % (option_pw))
		match = regex_string.search(line)
		if match:
			pw_state = match.group(1)
			if 'up' in pw_state:
				print("[INFO] PW State: " + str(pw_state))
			else:
				print("[WARNING] PW State: " + str(pw_state))
			pw_found = True
		else:
			regex_string = re.compile('PW: neighbor \S+, PW ID \S+, state is (.*)')
			match = regex_string.search(line)
			if match:
				pw_found = False
				pw_tlv_found = False
				incoming_tlv = False
				outgoing_tlv = False
		if pw_found == True:
			#need to find the equivalent XC ID from PD command, already getting AC above
			regex_string = re.compile('XC ID (\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1) == xconnect_id:
					print("[INFO] Xconnect ID matches")
				else:
					print("[WARNING] Xconnect ID in hardware (" + xconnect_id + ") does not match xconnect ID in software (" + match.group(1) + ")")
			regex_string = re.compile('PW Status TLV')
			match = regex_string.search(line)
			if match:
				pw_tlv_found = True
			if pw_tlv_found == True:
				regex_string = re.compile('Label\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1).isnumeric() == True:
						print("[INFO] Local label assigned: " + match.group(1))
					else:
						print("[WARNING] Local label is not valid: " + match.group(1))
					if match.group(2).isnumeric() == True:
						print("[INFO] Remote label assigned: " + match.group(2))
					else:
						print("[WARNING] Remote label is not valid: " + match.group(2))
				regex_string = re.compile('MTU\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1).isnumeric() == True:
						print("[INFO] Local MTU assigned: " + match.group(1))
					else:
						print("[WARNING] Local MTU is not valid")
					if match.group(2).isnumeric() == True:
						print("[INFO] Remote MTU assigned: " + match.group(2))
					else:
						print("[WARNING] Remote MTU is not valid")
					if match.group(1) == match.group(2):
						print("[INFO] MTU matches on PW")
					else:
						print("[WARNING] MTU does not match, needs to match.")
				regex_string = re.compile('Control word\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1) == match.group(2):
						print("[INFO] Control-word matches: " + match.group(1))
					else:
						print("[WARNING] Control-word does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
				regex_string = re.compile('PW type\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1) == match.group(2):
						print("[INFO] PW-type matches: " + match.group(1))
					else:
						print("[WARNING] PW-type does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
				regex_string = re.compile('Error: (.*$)')
				match = regex_string.search(line)
				if match:
					print("[ERROR] Error on PW detected " + match.group(1))
				regex_string = re.compile('Incoming Status')
				match = regex_string.search(line)
				if match:
					incoming_tlv = True
				if incoming_tlv == True:
					regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
					match = regex_string.search(line)
					if match:
						incoming_tlv = False
						if '0x0 (Up)' in match.group(1):
							print("[INFO] Incoming TLV status code is 'up'")
						else:
							print("[WARNING] Incoming TLV status code is not good: " + match.group(1))
				regex_string = re.compile('Outgoing Status')
				match = regex_string.search(line)
				if match:
					outgoing_tlv = True
				if outgoing_tlv == True:
					regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
					match = regex_string.search(line)
					if match:
						if '0x0 (Up)' in match.group(1):
							print("[INFO] Outgoing TLV status code is 'up'")
						else:
							print("[WARNING] Outgoing TLV status code is not good: " + match.group(1))   					
	return
def show_l2vpn_bridge_domain_pw_id_detail(option_pw, option_pw_id, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn bridge domain pw-id detail   			
	pw_found = False
	pw_tlv_found = False
	incoming_tlv = False
	outgoing_tlv = False
	for line in pre_list:
		regex_string = re.compile('PW: neighbor %s, PW ID %s, state is (.*)' % (option_pw, option_pw_id))
		match = regex_string.search(line)
		if match:
			pw_state = match.group(1)
			if 'up' in pw_state:
				print("[INFO] PW State: " + str(pw_state))
			else:
				print("[WARNING] PW State: " + str(pw_state))
			pw_found = True
		if pw_found == True:
			#need to find the equivalent XC ID from PD command, already getting AC above
			#regex_string = re.compile('XC ID (\S+)')
			#match = regex_string.search(line)
			#if match:
			#	if match.group(1) == xconnect_id:
			#		print("[INFO] Xconnect ID matches")
			#	else:
			#		print("[WARNING] Xconnect ID in hardware (" + xconnect_id + ") does not match xconnect ID in software (" + match.group(1) + ")")
			regex_string = re.compile('PW Status TLV')
			match = regex_string.search(line)
			if match:
				pw_tlv_found = True
			if pw_tlv_found == True:
				regex_string = re.compile('Label\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1).isnumeric() == True:
						print("[INFO] Local label assigned: " + match.group(1))
					else:
						print("[WARNING] Local label is not valid: " + match.group(1))
					if match.group(2).isnumeric() == True:
						print("[INFO] Remote label assigned: " + match.group(2))
					else:
						print("[WARNING] Remote label is not valid: " + match.group(2))
				regex_string = re.compile('MTU\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1).isnumeric() == True:
						print("[INFO] Local MTU assigned: " + match.group(1))
					else:
						print("[WARNING] Local MTU is not valid")
					if match.group(2).isnumeric() == True:
						print("[INFO] Remote MTU assigned: " + match.group(2))
					else:
						print("[WARNING] Remote MTU is not valid")
					if match.group(1) == match.group(2):
						print("[INFO] MTU matches on PW")
					else:
						print("[WARNING] MTU does not match, needs to match.")
				regex_string = re.compile('Control word\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1) == match.group(2):
						print("[INFO] Control-word matches: " + match.group(1))
					else:
						print("[WARNING] Control-word does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
				regex_string = re.compile('PW type\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1) == match.group(2):
						print("[INFO] PW-type matches: " + match.group(1))
					else:
						print("[WARNING] PW-type does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
				regex_string = re.compile('Error: (.*$)')
				match = regex_string.search(line)
				if match:
					print("[ERROR] Error on PW detected " + match.group(1))
				regex_string = re.compile('Incoming Status')
				match = regex_string.search(line)
				if match:
					incoming_tlv = True
				if incoming_tlv == True:
					regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
					match = regex_string.search(line)
					if match:
						incoming_tlv = False
						if '0x0 (Up)' in match.group(1):
							print("[INFO] Incoming TLV status code is 'up'")
						else:
							print("[WARNING] Incoming TLV status code is not good: " + match.group(1))
				regex_string = re.compile('Outgoing Status')
				match = regex_string.search(line)
				if match:
					outgoing_tlv = True
				if outgoing_tlv == True:
					regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
					match = regex_string.search(line)
					if match:
						if '0x0 (Up)' in match.group(1):
							print("[INFO] Outgoing TLV status code is 'up'")
						else:
							print("[WARNING] Outgoing TLV status code is not good: " + match.group(1))   					
	return
def show_l2vpn_bridge_domain_pw_id_private(option_pw, option_pw_id, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn bridge domain pw-id private  			
	pw_found = False
	pw_tlv_found = False
	incoming_tlv = False
	outgoing_tlv = False
	bridge_port_trace_history = False
	tx_lbl_map = ''
	rx_lbl_map = ''
	tx_lbl_req = ''
	rx_lbl_req = ''
	for line in pre_list:
		regex_string = re.compile('PW: neighbor %s, PW ID %s, state is (.*)' % (option_pw, option_pw_id))
		match = regex_string.search(line)
		if match:
			pw_state = match.group(1)
			if 'up' in pw_state:
				print("[INFO] PW State: " + str(pw_state))
			else:
				print("[WARNING] PW State: " + str(pw_state))
			pw_found = True
		if pw_found == True:
			#need to find the equivalent XC ID from PD command, already getting AC above
			#regex_string = re.compile('XC ID (\S+)')
			#match = regex_string.search(line)
			#if match:
			#	if match.group(1) == xconnect_id:
			#		print("[INFO] Xconnect ID matches")
			#	else:
			#		print("[WARNING] Xconnect ID in hardware (" + xconnect_id + ") does not match xconnect ID in software (" + match.group(1) + ")")
			regex_string = re.compile("LSP : (.+)")
			match = regex_string.search(line)
			if match:
				lsp_state = match.group(1)
				#need to add logic here for expected states
				if lsp_state == 'Up':
					print("[INFO] LSP state is Up")
				elif lsp_state == 'Down':
					print("[WARNING] LSP state is Down")
				else:
					print("[WARNING] LSP state is " + lsp_state)
					regex_string = re.compile('PW Status TLV')
			match = regex_string.search(line)
			if match:
				pw_tlv_found = True
			if pw_tlv_found == True:
				regex_string = re.compile('Label\s+\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1).isnumeric() == True:
						print("[INFO] Local label assigned: " + match.group(1))
					else:
						print("[WARNING] Local label is not valid: " + match.group(1))
					if match.group(2).isnumeric() == True:
						print("[INFO] Remote label assigned: " + match.group(2))
					else:
						print("[WARNING] Remote label is not valid: " + match.group(2))
				regex_string = re.compile('MTU\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1).isnumeric() == True:
						print("[INFO] Local MTU assigned: " + match.group(1))
					else:
						print("[WARNING] Local MTU is not valid")
					if match.group(2).isnumeric() == True:
						print("[INFO] Remote MTU assigned: " + match.group(2))
					else:
						print("[WARNING] Remote MTU is not valid")
					if match.group(1) == match.group(2):
						print("[INFO] MTU matches on PW")
					else:
						print("[WARNING] MTU does not match, needs to match.")
				regex_string = re.compile('Control word\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1) == match.group(2):
						print("[INFO] Control-word matches: " + match.group(1))
					else:
						print("[WARNING] Control-word does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
				regex_string = re.compile('PW type\s+(\S+)\s+(\S+)')
				match = regex_string.search(line)
				if match:
					if match.group(1) == match.group(2):
						print("[INFO] PW-type matches: " + match.group(1))
					else:
						print("[WARNING] PW-type does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
				regex_string = re.compile('Error: (.*$)')
				match = regex_string.search(line)
				if match:
					print("[ERROR] Error on PW detected " + match.group(1))
				regex_string = re.compile('Incoming Status')
				match = regex_string.search(line)
				if match:
					incoming_tlv = True
				if incoming_tlv == True:
					regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
					match = regex_string.search(line)
					if match:
						incoming_tlv = False
						if '0x0 (Up)' in match.group(1):
							print("[INFO] Incoming TLV status code is 'up'")
						else:
							print("[WARNING] Incoming TLV status code is not good: " + match.group(1))
				regex_string = re.compile('Outgoing Status')
				match = regex_string.search(line)
				if match:
					outgoing_tlv = True
				if outgoing_tlv == True:
					regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
					match = regex_string.search(line)
					if match:
						if '0x0 (Up)' in match.group(1):
							print("[INFO] Outgoing TLV status code is 'up'")
						else:
							print("[WARNING] Outgoing TLV status code is not good: " + match.group(1))   	
				regex_string = re.compile('Local PW Status: (\S+); Remote PW Status: (\S+)')
				match = regex_string.search(line)
				if match:
					local_pw_status = match.group(1)
					remote_pw_status = match.group(2)
					print("Local PW Status: " + local_pw_status)
					print("Remote Pw Status: " + remote_pw_status)
				regex_string = re.compile('LDP session state: (\S+)')
				match = regex_string.search(line)
				if match:
					ldp_session_state = match.group(1)
					if ldp_session_state == 'up':
						print("[INFO] LDP Session State is up")
					elif ldp_session_state == 'down':
						print("[WARNING] LDP Session State is down")
					else:
						print("[WARNING] LDP Session State is " + ldp_session_state)
				regex_string = re.compile('Registered with ITAL: (\S+)')
				match = regex_string.search(line)
				if match:
					ital_reg = match.group(1)
					if ital_reg == 'Yes':
						print("[INFO] Registered with ITAL? Yes")
					elif ital_reg == 'No':
						print("[WARNING] Registered with ITAL? No")
					else:
						print("[WARNING] Registered with ITAL? " + ital_reg)
				regex_string = re.compile('Peer state: (\S+)')
				match = regex_string.search(line)
				if match:
					peer_state = match.group(1)
					if peer_state == 'up':
						print("[INFO] Peer state is: up")
					elif peer_state == 'down':
						print("[WARNING] Peer state is: down")
					else:
						print("[WARNING] Peer state is: " + peer_state)
				regex_string = re.compile('Transport LSP down: (\S+)')
				match = regex_string.search(line)
				if match:
					transport_lsd_down = match.group(1)
					if transport_lsd_down == 'No':
						print("[INFO] Transport LSP is up")
					elif transport_lsd_down == 'Yes':
						print("[WARNING] Transport LSP is down")
					else:
						print("[WARNING] Transport LSP is " + transport_lsd_down)
				regex_string = re.compile('Advertised label to LDP: (\S+)')
				match = regex_string.search(line)
				if match:
					ldp_advertised_label = match.group(1)
					if ldp_advertised_label == 'Yes':
						print("[INFO] Label has been advertised to LDP")
					elif ldp_advertised_label == 'No':
						print("[WARNING] Label has NOT been advertised to LDP")
					else:
						print("[WARNING] Label has been advertised to LDP? " + ldp_advertised_label)
				regex_string = re.compile('Received a label from LSD: (\S+)')
				match = regex_string.search(line)
				if match:
					lsd_label_received = match.group(1)
					if lsd_label_received == 'Yes':
						print("[INFO] Received a label from LSD? Yes")
					elif lsd_label_received == 'No':
						print("[WARNING] Received a label from LSD? No")
					else:
						print("[WARNING] Received a label from LSD? " + lsd_label_received)
				regex_string = re.compile('Detailed segment state: (\S+)')
				match = regex_string.search(line)
				if match:
					segment_state = match.group(1)
					if segment_state == 'up':
						print("[INFO] Segment is up")
					elif segment_state == 'down':
						print("[WARNING] Segment is down")
					elif segment_state == 'connected':
						print("[WARNING] Segment is connected")
					else:
						print("[WARNING] Segment is " + segment_state)   
				regex_string = re.compile('Tx lbl map')
				match = regex_string.search(line)
				if match:
					tx_lbl_map = line
				regex_string = re.compile('Rx lbl map')
				match = regex_string.search(line)
				if match:
					rx_lbl_map = line
				regex_string = re.compile('Tx lbl req')
				match = regex_string.search(line)
				if match:
					tx_lbl_req = line
				regex_string = re.compile('Rx lbl req')
				match = regex_string.search(line)
				if match:
					rx_lbl_req = line
				regex_string = re.compile('Bridge-port trace history')
				match = regex_string.search(line)
				if match:
					bridge_port_trace_history = True
			if bridge_port_trace_history == True:
				if tx_lbl_req != '' and tx_lbl_map != '' and rx_lbl_req != '' and rx_lbl_map != '':
					print("[INFO] All label requests and mappings are present for PW.")
					print("[INFO] Tx label request: " + tx_lbl_req)
					print("[INFO] Tx label mapping: " + tx_lbl_map)
					print("[INFO] Rx label request: " + rx_lbl_req)
					print("[INFO] Rx label mapping: " + rx_lbl_map)
				else:
					print("[WARNING] Not all label requests or mappings are present for PW.")
					if tx_lbl_req != '':
						print("[INFO] Tx label request: " + tx_lbl_req)
					else:
						print("[WARNING] No Tx label request seen for PW")
					if tx_lbl_map != '':
						print("[INFO] Tx label mapping: " + tx_lbl_map)
					else:
						print("[WARNING] No Tx label mapping seen for PW")
					if rx_lbl_req != '':
						print("[INFO] Rx label request: " + rx_lbl_req)
					else:
						print("[WARNING] No Rx label request seen for PW")
					if rx_lbl_map != '':
						print("[INFO] Rx label mapping: " + rx_lbl_map)
					else:
						print("[WARNING] No Rx label mapping seen for PW")
				bridge_port_trace_history = False

	return
def show_l2vpn_database_ac(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn database ac
	ac_found = False
	for line in pre_list:
		regex_string = re.compile('(\S+:)')
		match = regex_string.search(line)
		if match:
			ac_found = True
	if ac_found == True:
		print("[INFO] AC found in database successfully")
	else:
		print("[WARNING] AC not found in database")
	return
def show_l2vpn_database_node(option_loc_cap, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn database node
	node_found = False
	for line in pre_list:
		regex_string = re.compile('Node ID.+\(%s\)' % (option_loc_cap))
		match = regex_string.search(line)
		if match:
			node_found = True
		else:
			regex_string = re.compile('Node ID.+\(\S+\)')
			match = regex_string.search(line)
			if match:
				node_found = False
		if node_found == True:
			regex_string = re.compile('MA:\s+vlan_ma\s+inited:\d+,\s+flags:(.+),\s+circuits:\d+')
			match = regex_string.search(line)
			if match:
				vlan_ma_flags = match.group(1)
				if '0x 2' in vlan_ma_flags:
					print("[INFO] vlan_ma flags look good with '0x 2'")
				else:
					print("[WARNING] vlan_ma flags are not good with " + vlan_ma_flags)
			regex_string = re.compile('MA:\s+ether_ma\s+inited:\d+,\s+flags:(.+),\s+circuits:\d+')
			match = regex_string.search(line)
			if match:
				ether_ma_flags = match.group(1)
				if '0x 2' in ether_ma_flags:
					print("[INFO] ether_ma flags look good with '0x 2'")
				else:
					print("[WARNING] ether_ma flags are not good with " + ether_ma_flags)
	return
def show_l2vpn_forwarding_detail_loc(option_int, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn forwarding detail loc
	xconnect_found = False
	for line in pre_list:
		regex_string = re.compile('Local interface: (\S+),\s+Xconnect id:\s(\S+),\s+Status:\s+(\S+)')
		match = regex_string.search(line)
		if match:
			if option_int in line:
				xconnect_id = match.group(2)
				xconnect_status = match.group(3)
				xconnect_found = True
				print("[INFO] Xconnect ID is: " + xconnect_id)
				if xconnect_status == 'up':
					print("[INFO] Xconnect Status is: " + xconnect_status)
				else:
					print("[WARNING] Xconnect Status is: " + xconnect_status)
		if xconnect_found == True:
			regex_string = re.compile('AC,\s+(\S+),\s+status:\s+(.*)')
			match = regex_string.search(line)
			if match:
				ac_status = match.group(2)
				if ac_status == 'Bound':
					print("[INFO] AC Status is: " + ac_status)
				else:
					print("[WARNING] AC Status is: " + ac_status)
			regex_string = re.compile('Bridge id:\s+(\S+),\s+Split horizon group id:\s+(\S+), status:\s+(.*)')
			match = regex_string.search(line)
			if match:
				bridge_status = match.group(3)
				print("Bridge Status is: " + bridge_status)
				break
	return(xconnect_id)
def show_l2vpn_forwarding_private_loc(xconnect_id, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn forwarding private loc
	xconnect_found = False
	programming_found = False
	for line in pre_list:
		regex_string = re.compile('Xconnect ID ' + xconnect_id)
		match = regex_string.search(line)
		if match:
			xconnect_found = True
		if xconnect_found == True:
			regex_string = re.compile('xcon_bound=(\S+),')
			match = regex_string.search(line)
			if match:
				xcon_bound = match.group(1)
				if xcon_bound == 'TRUE':
					print("[INFO] Xconnect Bound Status: " + xcon_bound)
				else:
					print("[WARNING] Xconnect Bound Status: " + xcon_bound)
			regex_string = re.compile('adj_valid=(\S+),')
			match = regex_string.search(line)
			if match:
				adj_valid = match.group(1)
				if adj_valid == 'TRUE':
					print("[INFO] Adjacency Valid Status: " + adj_valid)
				else:
					print("[WARNING] Adjacency Valid Status: " + adj_valid)
			regex_string = re.compile('----------')
			match = regex_string.search(line)
			if match:
				programming_found = True
			if programming_found == True:
				if 'Modify Event History' in line:
					break
				regex_string = re.compile('(.*(Modify|PD bind|PD unbind).*)')
				match = regex_string.search(line)
				if match:
					event = match.group(1)
					print("[WARNING] Interesting L2VPN Programming Event Found: " + event)
	return
def show_l2vpn_xconnect_pw_id_detail(option_pw, option_pw_id, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn xconnect pw-id detail
	pw_tlv_found = False
	incoming_tlv = False
	outgoing_tlv = False
	for line in pre_list:
		regex_string = re.compile("Group \S+, XC \S+ state is (.+);")
		match = regex_string.search(line)
		if match:
			xc_state = match.group(1)
			#need to add logic here for expected states
			print("Overall XC state is: " + xc_state)
		regex_string = re.compile("AC: (\S+), state is (.+)")
		match = regex_string.search(line)
		if match:
			ac_int = match.group(1)
			ac_state = match.group(2)
			#need to add logic here for expected states
			print("Found AC: " + ac_int + " With state: " + ac_state)
		regex_string = re.compile("PW: neighbor %s, PW ID %s, state is (.+)" % (option_pw, option_pw_id))
		match = regex_string.search(line)
		if match:
			pw_state = match.group(1)
			#need to add logic here for expected states
			print("Found PW for neighbor: " + option_pw + " With PW ID: " + option_pw_id + " And state: " + pw_state)
		regex_string = re.compile("LSP : (.+)")
		match = regex_string.search(line)
		if match:
			lsp_state = match.group(1)
			#need to add logic here for expected states
			if lsp_state == 'Up':
				print("[INFO] LSP state is Up")
			elif lsp_state == 'Down':
				print("[WARNING] LSP state is Down")
			else:
				print("[WARNING] LSP state is " + lsp_state)
		regex_string = re.compile('PW Status TLV')
		match = regex_string.search(line)
		if match:
			pw_tlv_found = True
		if pw_tlv_found == True:
			regex_string = re.compile('Label\s+\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1).isnumeric() == True:
					print("[INFO] Local label assigned: " + match.group(1))
				else:
					print("[WARNING] Local label is not valid: " + match.group(1))
				if match.group(2).isnumeric() == True:
					print("[INFO] Remote label assigned: " + match.group(2))
				else:
					print("[WARNING] Remote label is not valid: " + match.group(2))
			regex_string = re.compile('MTU\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1).isnumeric() == True:
					print("[INFO] Local MTU assigned: " + match.group(1))
				else:
					print("[WARNING] Local MTU is not valid")
				if match.group(2).isnumeric() == True:
					print("[INFO] Remote MTU assigned: " + match.group(2))
				else:
					print("[WARNING] Remote MTU is not valid")
				if match.group(1) == match.group(2):
					print("[INFO] MTU matches on PW")
				else:
					print("[WARNING] MTU does not match, needs to match.")
			regex_string = re.compile('Control word\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1) == match.group(2):
					print("[INFO] Control-word matches: " + match.group(1))
				else:
					print("[WARNING] Control-word does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
			regex_string = re.compile('PW type\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1) == match.group(2):
					print("[INFO] PW-type matches: " + match.group(1))
				else:
					print("[WARNING] PW-type does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
			regex_string = re.compile('Error: (.*$)')
			match = regex_string.search(line)
			if match:
				print("[ERROR] Error on PW detected " + match.group(1))
			regex_string = re.compile('Incoming Status')
			match = regex_string.search(line)
			if match:
				incoming_tlv = True
			if incoming_tlv == True:
				regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
				match = regex_string.search(line)
				if match:
					incoming_tlv = False
					if '0x0 (Up)' in match.group(1):
						print("[INFO] Incoming TLV status code is 'up'")
					else:
						print("[WARNING] Incoming TLV status code is not good: " + match.group(1))
			regex_string = re.compile('Outgoing Status')
			match = regex_string.search(line)
			if match:
				outgoing_tlv = True
			if outgoing_tlv == True:
				regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
				match = regex_string.search(line)
				if match:
					if '0x0 (Up)' in match.group(1):
						print("[INFO] Outgoing TLV status code is 'up'")
					else:
						print("[WARNING] Outgoing TLV status code is not good: " + match.group(1))   
	return
def show_l2vpn_xconnect_pw_id_private(option_pw, option_pw_id, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show l2vpn xconnect pw-id private
	pw_tlv_found = False
	incoming_tlv = False
	outgoing_tlv = False
	segment = ''
	for line in pre_list:
		regex_string = re.compile("Segment (\d+)")
		match = regex_string.search(line)
		if match:
			segment = match.group(1)
		regex_string = re.compile("Group \S+, XC \S+ state is (.+);")
		match = regex_string.search(line)
		if match:
			xc_state = match.group(1)
			#need to add logic here for expected states
			print("Overall XC state is: " + xc_state)
		regex_string = re.compile("AC: (\S+), state is (.+)")
		match = regex_string.search(line)
		if match:
			ac_int = match.group(1)
			ac_state = match.group(2)
			#need to add logic here for expected states
			print("Found AC: " + ac_int + " With state: " + ac_state)
		regex_string = re.compile("PW: neighbor %s, PW ID %s, state is (.+)" % (option_pw, option_pw_id))
		match = regex_string.search(line)
		if match:
			pw_state = match.group(1)
			#need to add logic here for expected states
			print("Found PW for neighbor: " + option_pw + " With PW ID: " + option_pw_id + " And state: " + pw_state)
		regex_string = re.compile("LSP : (.+)")
		match = regex_string.search(line)
		if match:
			lsp_state = match.group(1)
			#need to add logic here for expected states
			if lsp_state == 'Up':
				print("[INFO] LSP state is Up")
			elif lsp_state == 'Down':
				print("[WARNING] LSP state is Down")
			else:
				print("[WARNING] LSP state is " + lsp_state)
		regex_string = re.compile('PW Status TLV')
		match = regex_string.search(line)
		if match:
			pw_tlv_found = True
		if pw_tlv_found == True:
			regex_string = re.compile('Label\s+\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1).isnumeric() == True:
					print("[INFO] Local label assigned: " + match.group(1))
				else:
					print("[WARNING] Local label is not valid: " + match.group(1))
				if match.group(2).isnumeric() == True:
					print("[INFO] Remote label assigned: " + match.group(2))
				else:
					print("[WARNING] Remote label is not valid: " + match.group(2))
			regex_string = re.compile('MTU\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1).isnumeric() == True:
					print("[INFO] Local MTU assigned: " + match.group(1))
				else:
					print("[WARNING] Local MTU is not valid")
				if match.group(2).isnumeric() == True:
					print("[INFO] Remote MTU assigned: " + match.group(2))
				else:
					print("[WARNING] Remote MTU is not valid")
				if match.group(1) == match.group(2):
					print("[INFO] MTU matches on PW")
				else:
					print("[WARNING] MTU does not match, needs to match.")
			regex_string = re.compile('Control word\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1) == match.group(2):
					print("[INFO] Control-word matches: " + match.group(1))
				else:
					print("[WARNING] Control-word does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
			regex_string = re.compile('PW type\s+(\S+)\s+(\S+)')
			match = regex_string.search(line)
			if match:
				if match.group(1) == match.group(2):
					print("[INFO] PW-type matches: " + match.group(1))
				else:
					print("[WARNING] PW-type does not match, needs to match. Local value: " + match.group(1) + " Remote value: " + match.group(2))
			regex_string = re.compile('Error: (.*$)')
			match = regex_string.search(line)
			if match:
				print("[ERROR] Error on PW detected " + match.group(1))
			regex_string = re.compile('Incoming Status')
			match = regex_string.search(line)
			if match:
				incoming_tlv = True
			if incoming_tlv == True:
				regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
				match = regex_string.search(line)
				if match:
					incoming_tlv = False
					if '0x0 (Up)' in match.group(1):
						print("[INFO] Incoming TLV status code is 'up'")
					else:
						print("[WARNING] Incoming TLV status code is not good: " + match.group(1))
			regex_string = re.compile('Outgoing Status')
			match = regex_string.search(line)
			if match:
				outgoing_tlv = True
			if outgoing_tlv == True:
				regex_string = re.compile('Status code: (0x\d+\s+\(.+\))')
				match = regex_string.search(line)
				if match:
					if '0x0 (Up)' in match.group(1):
						print("[INFO] Outgoing TLV status code is 'up'")
					else:
						print("[WARNING] Outgoing TLV status code is not good: " + match.group(1))   
			regex_string = re.compile('Local PW Status: (\S+); Remote PW Status: (\S+)')
			match = regex_string.search(line)
			if match:
				local_pw_status = match.group(1)
				remote_pw_status = match.group(2)
				print("Local PW Status: " + local_pw_status)
				print("Remote Pw Status: " + remote_pw_status)
			regex_string = re.compile('LDP session state: (\S+)')
			match = regex_string.search(line)
			if match:
				ldp_session_state = match.group(1)
				if ldp_session_state == 'up':
					print("[INFO] LDP Session State is up")
				elif ldp_session_state == 'down':
					print("[WARNING] LDP Session State is down")
				else:
					print("[WARNING] LDP Session State is " + ldp_session_state)
			regex_string = re.compile('Registered with ITAL: (\S+)')
			match = regex_string.search(line)
			if match:
				ital_reg = match.group(1)
				if ital_reg == 'Yes':
					print("[INFO] Registered with ITAL? Yes")
				elif ital_reg == 'No':
					print("[WARNING] Registered with ITAL? No")
				else:
					print("[WARNING] Registered with ITAL? " + ital_reg)
			regex_string = re.compile('Peer state: (\S+)')
			match = regex_string.search(line)
			if match:
				peer_state = match.group(1)
				if peer_state == 'up':
					print("[INFO] Peer state: is up")
				elif peer_state == 'down':
					print("[WARNING] Peer state: is down")
				else:
					print("[WARNING] Peer state: is " + peer_state)
			regex_string = re.compile('Transport LSP down: (\S+)')
			match = regex_string.search(line)
			if match:
				transport_lsd_down = match.group(1)
				if transport_lsd_down == 'No':
					print("[INFO] Transport LSP is up")
				elif transport_lsd_down == 'Yes':
					print("[WARNING] Transport LSP is down")
				else:
					print("[WARNING] Transport LSP is " + transport_lsd_down)
			regex_string = re.compile('Advertised label to LDP: (\S+)')
			match = regex_string.search(line)
			if match:
				ldp_advertised_label = match.group(1)
				if ldp_advertised_label == 'Yes':
					print("[INFO] Label has been advertised to LDP")
				elif ldp_advertised_label == 'No':
					print("[WARNING] Label has NOT been advertised to LDP")
				else:
					print("[WARNING] Label has been advertised to LDP? " + ldp_advertised_label)
			regex_string = re.compile('Received a label from LSD: (\S+)')
			match = regex_string.search(line)
			if match:
				lsd_label_received = match.group(1)
				if lsd_label_received == 'Yes':
					print("[INFO] Received a label from LSD? Yes")
				elif lsd_label_received == 'No':
					print("[WARNING] Received a label from LSD? No")
				else:
					print("[WARNING] Received a label from LSD? " + lsd_label_received)
		regex_string = re.compile('Detailed segment state: (\S+)')
		match = regex_string.search(line)
		if match:
			segment_state = match.group(1)
			if segment_state == 'up':
				print("[INFO] Segment is up")
			elif segment_state == 'connected':
				print("[INFO] Segment is connected")
			elif segment_state == 'down':
				print("[WARNING] Segment is down")
			else:
				print("[WARNING] Segment is " + segment_state)             
	return
def show_process_l2vpn_mgr_txgroup_peer_all_detail(option_loc_cap, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show process l2vpn_mgr txgroup peer all detail
	peer_found = False
	aipc_create_found = False
	object_found = False
	ma_found = False
	ac_create_cb = False
	for line in pre_list:
		regex_string = re.compile("^PEER-ID.+'(AIPC-pub L2VPN-AC-PH1)'")
		match = regex_string.search(line)
		if match:
			peer_found = True
		else:
			regex_string = re.compile("^PEER-ID.+")
			match = regex_string.search(line)
			if match:
				peer_found = False
		if peer_found == True:
			regex_string = re.compile('(create_peer)\s+(\d+)\s+(\d+)\s+(.+$)')
			match = regex_string.search(line)
			if match:
				aipc_create_found = True
				peer_interval_cnt = match.group(2)
				peer_total_cnt = match.group(3)
				peer_create_time = match.group(4)
		regex_string = re.compile("^PEER-ID.+%s, vlan_ma" % (option_loc_cap))
		match = regex_string.search(line)
		if match:
			ma_found = True
		else:
			regex_string = re.compile("^PEER-ID.+")
			match = regex_string.search(line)
			if match:
				ma_found = False
		if ma_found == True:
			regex_string = re.compile('ac_create_cb')
			match = regex_string.search(line)
			if match:
				ac_create_cb = True
				print("[INFO] ac_create_cb message found for L2VPN_mgr going to vlan_ma on requested LC. Please check that this value was updated when the AC was created: " + line)
	if ac_create_cb == False:
		print("[WARNING] L2VPN_mgr ac_create_cb message going to vlan_ma on LC not seen.")
	if aipc_create_found == True:
		print("[INFO] AIPC create create_peer entry found in l2vpn_mgr")
		try:
			peer_interval_cnt = int(peer_interval_cnt)
			if peer_interval_cnt > 1:
				print("[WARNING] Interval for AIPC create_peer is higher than 1, please double check this. Value is " + peer_interval_cnt)
			elif peer_interval_cnt == 1:
				print("[INFO] Interval for AIPC create_peer is 1")
			else:
				print("[WARNING] Interval for AIPC create_peer is not right, please double check this. Value is " + peer_interval_cnt)
		except Exception as e:
				print("[WARNING] Interval for AIPC create_peer is not right, please double check this. Value is " + peer_interval_cnt)
		try:
			peer_total_cnt = int(peer_total_cnt)
			if peer_total_cnt > 1:
				print("[WARNING] Total for AIPC create_peer is higher than 1, please double check this. Value is " + peer_interval_cnt)
			elif peer_interval_cnt == 1:
				print("[INFO] Total for AIPC create_peer is 1")
			else:
				print("[WARNING] Total for AIPC create_peer is not right, please double check this. Value is " + peer_interval_cnt)
		except Exception as e:
			print("[WARNING] Total for AIPC create_peer is not right, please double check this. Value is " + peer_interval_cnt)
		print("[WARNING] Please check peer_create timestamp to see if it is recent / expected. Value is " + peer_create_time)
	else:
		print("[WARNING] L2VPN-AC-PH1 create_peer from AIPC not seen")
	return
def show_proc_vlan_ma_txgroup_peer_all_detail_loc(option_loc_cap, pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show proc vlan_ma txgroup peer all detail loc
	peer_found = False
	ac_create_found = False
	ac_update_found = False
	for line in pre_list:
		regex_string = re.compile('error')
		match = regex_string.search(line)
		if match:
			print("[WARNING] There are error(s) in the TXSend library: " + line)
		regex_string = re.compile('pause')
		match = regex_string.search(line)
		if match:
			print("[WARNING] There is a pause message in the TXSend library, please verify if this event is related: " + line)
		
		regex_string = re.compile('^PEER-ID.+%s, vlan_ma.+' % (option_loc_cap))
		match = regex_string.search(line)
		if match:
			peer_found = True
		else:
			regex_string = re.compile("^PEER-ID.+")
			match = regex_string.search(line)
			if match:
				peer_found = False
		if peer_found == True:
			regex_string = re.compile('ac_create')
			match = regex_string.search(line)
			if match:
				ac_create_found = True
				print("[INFO] ac_create seen from MA, please verify timestamp lines up with AC creation time: " + line)
			regex_string = re.compile('ac_update')
			match = regex_string.search(line)
			if match:
				ac_update_found = True
				print("[INFO] ac_update seen from MA, please verify timestamp lines up with AC update time: " + line)
	if ac_create_found == False:
		print("[WARNING] no ac_create message seen from MA on LC")
	if ac_update_found == False:
		print("[WARNING] no ac_update message seen from MA on LC")	
	return
def show_install_log_exr(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show install log for a given install ID for eXR specific issues
	print("Not implemented yet")
	return
def show_install_log_cxr(pre_list):
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#parse show install log for a given install ID for cXR specific issues
	package_incompatibility = 0
	missing_package = 0
	ens = 0
	corruption = 0
	sysdb = 0
	insthelper_operation = 0
	insthelper_write = 0
	prepare_ack = 0
	disk_space = 0
	disk_check = 0
	disk = ''
	affected_node = ''
	for line in pre_list:
		regex_string = re.compile('package incompatibilities')
		match = regex_string.search(line)
		if match:
			package_incompatibility = 1
		regex_string = re.compile('activate or deactivate the specified packages on the specified nodes')
		match = regex_string.search(line)
		if match:
			missing_package = 1
		regex_string = re.compile('has been downloading packages via ENS for a period of time')
		match = regex_string.search(line)
		if match:
			ens = 1
		regex_string = re.compile('AFFECTED NODE\(S\): (.+)')
		match = regex_string.search(line)
		if match:
			affected_node = match.group(1)
		regex_string = re.compile('details: \'Package Library\' detected the \'fatal\' condition \'file I/O error\':')
		match = regex_string.search(line)
		if match:
			corruption = 1
		regex_string = re.compile('A SysDB client tried to access a nonexistent item or list an empty directory')
		match = regex_string.search(line)
		if match:
			sysdb = 1
		regex_string = re.compile('ERROR: Process \'insthelper\' has been performing an operation for a period of time so that the node failed to')
		match = regex_string.search(line)
		if match:
			insthelper_operation = 1
		regex_string = re.compile('Process \'insthelper\' has been writing to disk for a period')
		match = regex_string.search(line)
		if match:
			insthelper_write = 1
		regex_string = re.compile('Error:\s+(\d+.+(CPU0|SP)) \(No \'prepare ack\' response received\)')
		match = regex_string.search(line)
		if match:
			affected_node = match.group(1)
			prepare_ack = 1
		regex_string = re.compile('Error:\s+- (\d+.+(CPU0|SP)): (.+:).+bytes required')
		match = regex_string.search(line)
		if match:
			affected_node = match.group(1)
			disk_space = 1
			disk = match.group(3)
		regex_string = re.compile('ERROR: Node failed to respond when completing the disk checks.')
		match = regex_string.search(line)
		if match:
			disk_check = 1
	if missing_package == 1 and package_incompatibility == 1:
		print("[WARNING] When upgrading all active packages must be upgraded at the same time. IE if you have the mini, doc, and mpls package and try to upgrade mini, and mpls it will fail because doc is required. In some releases the FPD package is part of mini, in others it is not.")
	elif affected_node != '':
		if ens == 1:
			print("[WARNING] The affected node " + affected_node + " is unable to write to bootflash. In a CRS fabric card we can use the 'bootflash reclaim' command to get space for writing. For other cards we can check on free space or try shutting down the card and proceeding with the upgrade without the card and bringing it back in service later.")
		elif insthelper_operation == 1:
			print("[WARNING] Insthelper process is run on every node in the system to handle install requests, upgrades, booting, etc. When stuck this can prevent an entire upgrade. Restart the insthelper process for " + affected_node + " and the install should run to completion now.")
		elif insthelper_write == 1:
			print("[WARNING] Insthelper process is run on every node in the system to handle install requests, upgrades, booting, etc. When stuck this can prevent an entire upgrade. Restart the insthelper process for " + affected_node + " and the install should run to completion now.")
		elif prepare_ack == 1:
			print("[WARNING] Insthelper process is run on every node in the system to handle install requests, upgrades, booting, etc. Insthelper is blocked on other processes (eg, cfgmgr, disk write) or some function call on " + affected_node + ". Please check show processes blocked for the impacted location during install operation or show install trace insthelper for the location for clues.")
		elif disk_space == 1:
			print("[WARNING] The error message is indicating that we need a certain amount of free space on the partition " + disk + ' of node ' + affected_node + '. Please check Show media and Show filesystem for this location to see how much free space there is and try clearing out old files or removing old packages with install remove inactive.')
		elif disk_check == 1:
			print("[WARNING] There are several issues which can cause this. 1) A truncated package file or an actual disk check issue. 2) Try checking the admin show install pie-info <filename> detail' to see if it is a valid package. 3) Try restarting instdir and insthelper processes on  " + affected_node)
		else:
			print("[WARNING] There is an error with node " + affected_node + " but the error is not caught by this script. Please report the error to smilstea@cisco.com for update to script. To correct try verifying disk space, any errors with the node, stuck processes or blocked processes, restart insthelper on the node or instdir on the node if its a mgmt node or on the primary RP.")
	elif corruption == 1:
		print("[WARNING] Please contact Cisco TAC as their is possible disk or filesystem corruption. Please collect a 'fsck' for disk0: on the impacted node to see if there is any corruption, further verification steps to be performed by TAC.")
	elif sysdb == 1:
		print("[WARNING] If show commands are not responding and displaying a sysdb error then it can be one of two things, sysdb or installdir process. If no other commands are exhibiting an issue then try a process restart of instdir. It should not be impacting as installdir is only used for show commands, install operations, and card bootups.")
	return
def cef():
	###__author__     = "Sam Milstead"
	###__copyright__  = "Copyright 2022 (C) Cisco TAC"
	###__version__    = "1.0.0"
	###__status__     = "alpha"
	#generate cef commands
	return
if __name__ == '__main__':
	task()
