from getpass import getpass
import netmiko
import re
import difflib
import sys

def make_connection (ip, username, password):
		return netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)

def get_ip (input):
	return(re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))

def get_ips (file_name):
	for line in open(file_name, 'r').readlines():
		line = get_ip(line)
		for ip in line:
			ips.append(ip)
# This will be the list of commands we will use
commands_list = []

# Get the commands from commands.txt and append to our list
with open('commands.txt', 'r') as f:
	for line in f:
		commands_list.append(line)


def to_doc_a(file_name, varable):
	f=open(file_name, 'a')
	f.write(varable)
	f.write('\n')
	f.close()


def to_doc_w(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()

#This will be a list of the devices we want to SSH to
ips = []

#Pull the IPs.txt is a list of the IPs we want to connect to
#This function pulls those IPs out of the txt file and puts them into a list
get_ips("IPs.txt")
print("TVT Commands, if incorrect, logout now")
for commands in commands_list:
	print(commands)

#Prompt user for account info
username = input("Username: ")
password = getpass()
#Where we are storing our output
file_name = input("Is this a Before.txt of After.txt TVT: ")
#Clearing all the old info out of the results.csv file
to_doc_w(file_name, "")
#Commands To Use


#Make a for loop to hit all the devices, for this we will be looking at the IOS it's running
for ip in ips:
	#Connect to a device
	net_connect = make_connection(ip, username, password)
	#Run all our commands and append to our file_name
	for commands in commands_list:
		output = net_connect.send_command_expect(commands)
		results = output + '\n'
        #Next we will append the output to the results file
		to_doc_a(file_name, results)

if file_name == "Before.txt":
	print('Completed')
elif file_name == "After.txt":
	fromfile = "Before.txt"
	tofile = "After.txt"
	fromlines = open(fromfile, 'U').readlines()
	tolines = open(tofile, 'U').readlines()
#	diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())
	diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile)
	f = open("changes.html", "w")
	f.write(diff)
	f.close
#	print(diff)
#	print(''.join(diff),)
else:
	print('Before or After not detected')
