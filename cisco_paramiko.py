import sys
import pprint
import json
import time

from getpass import getpass
import paramiko


def read_devices(file_path: str):
    fp = open(file_path, "rb")
    devices = json.load(fp)
    fp.close()
    return devices


device_dict = read_devices("switches.json")


# Check if the correct number of command line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 cisco_paramiko.py <file_path>")
    sys.exit(1)

# Get the file path from the command line arguments
file_config = sys.argv[1]

username = input("Username: ")
password = getpass()
pp = pprint.PrettyPrinter(indent=4)

with open(file_config) as f:
    config_list = f.readlines()
pp.pprint(config_list)
switch_ip = [r["ip"] for r in device_dict["switches"]]
pp.pprint(switch_ip)


for switch in switch_ip:
    try:
        ip = switch
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip,port=22,username=username,password=password)
        print(ip + " " +'login succesfully')
        cli = ssh.invoke_shell()
        cli.send('terminal length 0\n')
        time.sleep(0.5)
        for i in config_list:
            cli.send(i)
            time.sleep(0.5)
        dis_this = cli.recv(9999999).decode() 
        print(dis_this)
        ssh.close()
    except (paramiko.ssh_exception.NoValidConnectionsError):
        print ('no asnwer form device ' + switch)
        continue
    except (paramiko.ssh_exception.AuthenticationException):
        print ('authentification failed for device ' + switch)
        continue
    except Exception as e:
        print(e)