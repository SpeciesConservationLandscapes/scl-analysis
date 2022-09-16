# scl_download_google_cloud.py
# ews 9/14/2022

# Objective:  download geo.json files from Google Cloud

# Reminders for Eric about local environment
# 1.  Start Anaconda prompt
# 2.  Activate scl environmen:  (base) C:\Users\esanderson>conda activate scl
# 3.  Change directory to scripts:  (scl) C:\Users\esanderson>cd C:\_data\SCRIPTS\scl-analysis
# 4.  If needed, check list of packages:  (scl) C:\_data\SCRIPTS\scl-analysis>conda list
# 5.  set environment variable to key:  set GOOGLE_APPLICATION_CREDENTIALS=C:\proj\species\tigers\TCLs v3\google\.env

# To get this particular script working, I needed to
# a. Install Google Cloud CLI Setup -- need for authentication of our account
# ...


# The URL for online access to our Google Cloud bucket for the SCL work is 
#https://console.cloud.google.com/storage/browser/scl-pipeline/ls_stats/Panthera_tigris/canonical?project=scl3-244715&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false


# some imports
import os
import gstorage as gs  # code from Dustin Sampson to import/export from/to Google storage

# set environment variable in windows [note:  this is also set in gstorage.py"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\proj\\species\\tigers\\TCLs v3\\google\\service.json"

# some set up
local_path = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_09142022"

# example calls using Dustin's script

"""
# download single file; note need to specify local filename
gs.download_from_cloudstorage(
    blob_path="ls_stats/Panthera_tigris/canonical/2001-01-01/scl_states.geojson",
    local_path = r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_09142022\scl_states.geojson",
    bucket_name="scl-pipeline"
    )
"""

gs.download_dir_from_cloudstorage(
    blob_path= "ls_stats/Panthera_tigris/canonical",
    local_path= r"C:\proj\species\tigers\TCLs v3\TCL delineation\scl_stats_09142022",
    bucket_name="scl-pipeline"
    )


"""

# initialize client and bucket
client = storage.Client()
bucket = client.get_bucket("scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01")
blobs = client.loist_blobs(bucket_or_name=bucket, prefix='path/to/files')



# see what we've got
for blob in blogs:
    print(f"{blob.name} last updated at: {blob.updated}")


gsutil -m cp \
  "gs://scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01/scl_restoration.geojson" \
  "gs://scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01/scl_restoration_fragment.geojson" \
  "gs://scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01/scl_species.geojson" \
  "gs://scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01/scl_species_fragment.geojson" \
  "gs://scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01/scl_states.geojson" \
  "gs://scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01/scl_survey.geojson" \
  "gs://scl-pipeline/ls_stats/Panthera_tigris/canonical/2020-01-01/scl_survey_fragment.geojson" \
  .
  
"""
