from azure.storage.blob import BlobServiceClient
import os

connect_str = 'YOUR_AZURE_STORAGE_CONNECTION_STRING'


container_url = 'https://internaiextraction.blob.core.windows.net/internaiextractionblob'
file_path = 'C:\\Users\\abura\\Downloads\\event_epl (1).csv'
 
blob_name = 'events.csv' 

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

container_client = blob_service_client.get_container_client(container_url)


try:
    container_client.get_container_properties()
except Exception as e:
    container_client.create_container()


blob_client = blob_service_client.get_blob_client(container=container_url, blob=blob_name)


with open(file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(f"File {file_path} uploaded to {container_url}/{blob_name}")
