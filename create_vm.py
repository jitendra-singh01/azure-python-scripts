from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
import os
import traceback
USERNAME = "ubuntu"
# Resource Group
GROUP_NAME = 'azure-sample-group-virtual-machinest'

# Network
VNET_NAME = 'azure-sample-vnett'
VM_NAME = "azureusest2"
SUBNET_NAME = 'azure-sample-subnett'
LOCATION = "eastus"

IP_CONFIG_NAME = 'azure-sample-ip-config'
NIC_NAME = 'azure-sample-nic'

def create_nic(network_client):
    """Create a Network Interface for a VM.
    """
    # Create VNet
    print('\nCreate Vnet')
    async_vnet_creation = network_client.virtual_networks.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        {
            'location': LOCATION,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    )
    async_vnet_creation.wait()

    # Create Subnet
    print('\nCreate Subnet')
    async_subnet_creation = network_client.subnets.create_or_update(
        GROUP_NAME,
        VNET_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    )
    subnet_info = async_subnet_creation.result()

    # Create NIC
    print('\nCreate NIC')
    async_nic_creation = network_client.network_interfaces.create_or_update(
        GROUP_NAME,
        NIC_NAME,
        {
            'location': LOCATION,
            'ip_configurations': [{
                'name': IP_CONFIG_NAME,
                'subnet': {
                    'id': subnet_info.id
                }
            }]
        }
    )
    return async_nic_creation.result()

def create_vm(compute_client):
    print('\nCreating VM')
    VM_PARAMETERS={
        'location': LOCATION,
        'os_profile': {
            'computer_name': VM_NAME,
            'admin_username': 'ubuntu',
            'linux_configuration': {
                "disable_password_authentication": True,
                "ssh": {
                    "public_keys": [{
                        "path": "/home/{}/.ssh/authorized_keys".format(USERNAME),
                        "key_data": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDeuojy8n1Covi3Hv4VQ0NQPGeRaEaQfXdiMdpFVVCsZPzN243bbEo0x3xhcODBDl8BR7NB6917cGBdT6dETUBdeqL6gjeAMia56utwLoUfIsFX5c4gKvara31LkbTGcbSXhtO8DECSzhQiY9zdkBtabqseRaCByFQ7wKM3I5YTyimuAUPdMZDZ/eNEM5exKnYS+uVmadFoLmSngeDpmZPe/vnGueDbAVCrAKVKbaHUHsll3NUkM9/iFp89ij140aC74L4wTbaE2Wnp7gowcqpON6QgKB9E9OcZ2pfrWP7Nv9CA7ndaxEPU8FM1fOt+IqYk8wr9Sk2YFhlbo3IB9wj5 jayantjainco@penguin"
                    }]
                 }
            }
        },
        'storage_profile': {
            'image_reference': {
                'publisher': 'Canonical',
                'offer': 'UbuntuServer',
                'sku': '16.04.0-LTS',
                'version': 'latest'
            },
        },
        'hardware_profile': {
            'vm_size': 'Standard_DS1_v2'
        },
        'network_profile': {
            'network_interfaces': [{
                'id': '/subscriptions/a9e7f5b3-273a-4ebf-8ea5-81dec14515ee/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkInterfaces/test1ss372',
            }]
        },
    }
    compute_vm = compute_client.virtual_machines.create_or_update(GROUP_NAME, VM_NAME, VM_PARAMETERS)
    return compute_vm.result()

print('\nCreate Resource Group')
resource_client = get_client_from_auth_file(ResourceManagementClient)  
compute_client = get_client_from_auth_file(ComputeManagementClient)
resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})
network_client = get_client_from_auth_file(NetworkManagementClient)
nic = create_nic(network_client)
async_vm_creation = create_vm(compute_client)
# Tag the VM
print('\nTag Virtual Machine')
async_vm_update = compute_client.virtual_machines.create_or_update(GROUP_NAME,VM_NAME,{'location': LOCATION,'tags': {'who-rocks': 'python','where': 'on azure'}})
async_vm_update.wait()