import sys
import pprint
import json

from getpass import getpass
from netmiko import ConnectHandler


def read_devices(file_path: str):
    fp = open(file_path, "rb")
    devices = json.load(fp)
    fp.close()
    return devices


device_dict = read_devices("switches.json")


# Check if the correct number of command line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 huawei_netmiko.py <file_path>")
    sys.exit(1)

# Get the file path from the command line arguments
file_config = sys.argv[1]

username = input("Username: ")
password = getpass()
pp = pprint.PrettyPrinter(indent=4)

with open(file_config) as f:
    config_lines = f.read().splitlines()
pp.pprint(config_lines)

switch_ip = [r["ip"] for r in device_dict["switches"]]
pp.pprint(switch_ip)


for switch in switch_ip:
    ip_address_of_device = switch
    CE = {
        'device_type': 'huawei',
        'ip': ip_address_of_device,
        'username': username,
        'password': password
    }

    ssh_connect = ConnectHandler(**CE)
    output = ssh_connect.send_config_set(config_lines, delay_factor=2)
    print(f"\n\n-------------- CE_{CE['ip']} --------------")
    print(output)
    print("-------------------- End -------------------")

    ssh_connect.disconnect()
