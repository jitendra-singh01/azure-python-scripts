from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters
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
print('\nCreate Resource Group')
resource_client = get_client_from_auth_file(ResourceManagementClient)  
storage_client = get_client_from_auth_file(StorageManagementClient)
resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})

storage_async_operation = storage_client.storage_accounts.create(
    GROUP_NAME,
    Haikunator().haikunate(delimiter=''),
    StorageAccountCreateParameters(
        sku=Sku(name=SkuName.standard_ragrs),
        kind=Kind.storage,
        location=LOCATION
    )
)
storage_account = storage_async_operation.result()