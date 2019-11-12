from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.storage import StorageManagementClient
from azure.storage import CloudStorageAccount
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters
from azure.storage.blob import BlockBlobService, PageBlobService, AppendBlobService
from haikunator import Haikunator
import os
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    StorageAccountUpdateParameters,
    Sku,
    SkuName,
    Kind
)
import traceback
GROUP_NAME = 'azure-group-storage'
STORAGE_ACCOUNT_NAME = "azure-storage-tt"
LOCATION = "eastus"
resource_client = get_client_from_auth_file(ResourceManagementClient)  
storage_client = get_client_from_auth_file(StorageManagementClient)
account = get_client_from_auth_file(CloudStorageAccount)

blockblob_service = storage_client.create_block_blob_service()

print('List storage accounts by resource group')
for item in storage_client.storage_accounts.list_by_resource_group(GROUP_NAME):
    print(item.name)
    storage_account = storage_client.storage_accounts.get_properties(
        GROUP_NAME, item.name)
    print(storage_account)
