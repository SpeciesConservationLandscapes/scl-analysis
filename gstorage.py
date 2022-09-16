# gstorage.py
# from Dustin Sampson on 9/14/2022

# objective:  push data up or down from Google Cloud Storage

# example call to the functions below
#download_from_cloudstorage(
#    blob_path="ls_stats/Panthera_tigris/canonical/2001-01-01/scl_states.geojson",
#    local_path="c:\\ls_stats\\Panthera_tigris\\canonical\\2001-01-01\\scl_states.geojson",
#    bucket_name="scl-pipeline"
#)



import json
import os
from pathlib import Path
from typing import Optional, Union

from google.cloud.exceptions import NotFound
from google.cloud.storage import Client
from google.oauth2 import service_account

# service key file for SCL bucket
SERVICE_FILE_JSON = r"C:\proj\species\tigers\TCLs v3\google\service.json"


def _get_client():
    with open(SERVICE_FILE_JSON) as f:
        service_account_info = json.loads(f.read())
    storage_credentials = service_account.Credentials.from_service_account_info(
        service_account_info
    )

    return Client(
        project=service_account_info["project_id"], credentials=storage_credentials
    )


def upload_to_cloudstorage(
    local_path: Union[str, Path],
    blob_path: Union[str, Path],
    bucket_name: str = None,
) -> str:
    client = _get_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(str(blob_path))
    blob.upload_from_filename(str(local_path), timeout=3600)
    return f"gs://{bucket_name}/{blob_path}"


def download_from_cloudstorage(
    blob_path: Union[str, Path],
    local_path: Union[str, Path],
    bucket_name: Optional[str] = None,
) -> Union[str, Path]:

    dir_path = Path(local_path).parent
    if dir_path.exists() is False:
        os.makedirs(dir_path)

    client = _get_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(str(blob_path))
    blob.download_to_filename(str(local_path))
    return local_path

# see example:  https://stackoverflow.com/questions/49748910/python-download-entire-directory-from-google-cloud-storage
def download_dir_from_cloudstorage(
    blob_path: Union[str, Path],
    local_path: Union[str, Path],
    bucket_name: Optional[str] = None,
) -> Union[str, Path]:

    dir_path = Path(local_path).parent
    if dir_path.exists() is False:
        os.makedirs(dir_path)
    
    client = _get_client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=blob_path)  # get list of files
    for blob in blobs:
        print("Working on ", blob)
        if blob.name.endswith("/"):
            continue
        file_split = blob.name.split("/")
        directory = "/".join(file_split[0:-1])
        #Path(directory).mkdir(parents=True, exist_ok=True)
        #blob.download_to_filename(blob_name)
        
        # the next three lines are unique to the SCL structure on Windows; don't know how to generalize
        year = file_split[3]
        filename = file_split[4]
        Path(os.path.join(local_path, year, "")).mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(os.path.join(local_path, year, filename)) 
    return local_path

def remove_from_cloudstorage(blob_path: str, bucket_name: Optional[str] = None):
    client = _get_client()
    bucket = client.get_bucket(bucket_name)
    try:  # don't fail entire task if this fails
        bucket.delete_blob(blob_path)
    except NotFound:
        print(f"{blob_path} not found")
