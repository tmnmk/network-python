import sys
import pprint
import json
import time

from getpass import getpass
import paramiko



# Check if the correct number of command line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 huawei_paramiko_byip.py <file_path>")
    sys.exit(1)

# Get the file path from the command line arguments
file_config = sys.argv[1]

print("Please type switch IP address ")
ip = input("IP Address: ")
username = input("Username: ")
password = getpass()
pp = pprint.PrettyPrinter(indent=4)

with open(file_config) as f:
    config_list = f.readlines()
pp.pprint(config_list)

ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip,port=22,username=username,password=password)
print(ip + " " +'login succesfully')
cli = ssh.invoke_shell()
cli.send('screen-length 0 temporary\n')
time.sleep(0.5)
cli.send('system-view\n')
time.sleep(0.5)
for i in config_list:
    cli.send(i)
    time.sleep(0.5)
dis_this = cli.recv(9999999).decode() 
print(dis_this)
ssh.close()
