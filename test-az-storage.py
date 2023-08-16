# pip install azure-storage-blob
# pip install azure-identity

from azure.storage.blob import (
	BlobServiceClient,
	generate_account_sas,
	ResourceTypes,
	AccountSasPermissions,
	)
from azure.core.exceptions import ResourceExistsError, HttpResponseError

from azure.identity import DefaultAzureCredential
import os
import re
import logging

logger = logging.getLogger('azure')
logger.setLevel(logging.DEBUG)
token_credential = DefaultAzureCredential()

account_url = "https://gsgdaltests.blob.core.windows.net/"

blob_service_client = BlobServiceClient(
                account_url=account_url, credential=token_credential
            )
storage_name = "test"

local_path = "/tmp/azure_test"
os.mkdir(local_path)

# Create a file in the local data directory to upload and download
local_file_name = "test_azure_upload.txt"
upload_file_path = os.path.join(local_path, local_file_name)

# Write text to the file
file = open(file=upload_file_path, mode='w')
file.write("Hello, World!")
file.close()
#
blob_client = blob_service_client.get_blob_client(container=storage_name, blob=local_file_name)

print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

# Upload the created file
with open(file=upload_file_path, mode="rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# We will download the file
# Download the blob to a local file
# Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
container_client = blob_service_client.get_container_client(container=storage_name)
print("\nDownloading blob to \n\t" + download_file_path)

with open(file=download_file_path, mode="wb") as download_file:
 download_file.write(container_client.download_blob(local_file_name).readall())

print("\nfile downloaded \n\t" + download_file_path)
