import yaml
import sys
from panos.firewall import Firewall
from panos.network import Interface, Subinterface, Zone
from panos.objects import AddressObject
from panos.policies import SecurityRule
from panos.errors import PanDeviceError

from getpass import getpass

# Define your device details
hostname = input("MGMT IP address of the firewall: ")
username = input("Username: ")
password = getpass()

# Check if the correct number of command line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 panos_create-interface.py <file_path>")
    sys.exit(1)

# Get the file path from the command line arguments
file_config = sys.argv[1]

# Load interface configuration from YAML file
with open(file_config) as file:
    config = yaml.safe_load(file)

interfaces_config = config.get('interfaces', {})

try:
    # Connect to the device and authenticate
    device = Firewall(hostname, api_username=username, api_password=password)

    # Create a tree structure to associate the device with
    device.refresh_system_info()

    # Create zones
    for interface_name, interface_data in interfaces_config.items():
        zone_name = interface_data.get('zone')
        if zone_name:
            zone = Zone(zone_name)
            device.add(zone)
            print(f"Zone '{zone_name}' created successfully.")

#    # Loop through the interfaces and create them
#    for interface_name, interface_data in interfaces_config.items():
#        interface = Interface(interface_name)
#        interface.comment = interface_data.get('comment', '')
#
#        # Configure IP address
#        ip_address = interface_data.get('ip_address')
#        if ip_address:
#            interface.set_ipv4(ip_address)
#
#        # Configure virtual router
#        virtual_router = interface_data.get('virtual_router')
#        if virtual_router:
#            interface.virtual_router = virtual_router
#
#        # Configure zone
#        zone_name = interface_data.get('zone')
#        if zone_name:
#            interface.zone = zone_name
#
#        # Configure management profile
#        management_profile = interface_data.get('management_profile')
#        if management_profile:
#            interface.management_profile = management_profile
#
#        try:
#            device.add(interface)
#            interface.create()
#            print(f"Interface {interface_name} created successfully.")
#
#            # Create subinterfaces
#            subinterfaces_data = interface_data.get('subinterfaces', [])
#            for subiface_data in subinterfaces_data:
#                vlan_id = subiface_data.get('vlan_id')
#                vlan_tag = subiface_data.get('vlan_tag')
#
#                subinterface = Subinterface(vlan_id, vlan_tag)
#                subinterface.comment = f"Subinterface VLAN {vlan_id} with tag {vlan_tag}"
#
#                interface.add_subinterface(subinterface)
#                subinterface.create()
#
#                print(f"Subinterface VLAN {vlan_id} with tag {vlan_tag} created successfully.")
#                
#        except PanDeviceError as e:
#            print(f"Failed to create interface {interface_name}: {str(e)}")

    # Commit the changes
    device.commit()
    print("Changes committed successfully.")

except PanDeviceError as e:
    print(f"Failed to connect to device: {str(e)}")