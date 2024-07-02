import getpass
import pprint
import json

from napalm import get_network_driver

DRIVER = get_network_driver("ce")

def read_devices(file_path: str):
    fp = open(file_path, "rb")
    devices = json.load(fp)
    fp.close()
    return devices

def connect_and_exec(host, user, password):
    device = DRIVER(hostname=host, username=user, password=password, optional_args = {'port': 22})
    device.open()

    facts = device.get_facts()
    print("###")
    print(f"FACTS FOR {host}")
    pprint.pprint(facts)
    print("###")

    device.close()

device_dict = read_devices("switches.json")
switch_ip = [r["ip"] for r in device_dict["switches"]]
user = input("Username: ")
password = getpass.getpass(prompt=f"type password: ")

for switch in switch_ip:
    host = switch
    connect_and_exec(host, user, password)

