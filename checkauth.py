from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.compute import ComputeManagementClient
import os

client = get_client_from_auth_file(ComputeManagementClient)
print(os.environ['AZURE_AUTH_LOCATION']['clientId'])