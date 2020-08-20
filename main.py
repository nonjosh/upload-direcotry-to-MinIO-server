

from pathlib import Path
# Import MinIO library.
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists
from progress import Progress

mypath = '/mnt/d/Downloads/setaside'

endpoint = "localhost:9001"
access_key = "minio"
secret_key = "minio123"
bucket_name = "setaside"

# get full paths for all files in the folder
filepath_full = list(Path(mypath).rglob("*"))
filepath_full = [str(f) for f in filepath_full if not f.is_dir()]

# rename file paths
filepath = [f.replace(mypath, '').lstrip('/') for f in filepath_full]


# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio(
    endpoint, access_key=access_key, secret_key=secret_key, secure=False,
)

progress = Progress()
# Put an object with contents
for filepath in filepath_full:
    object_name = filepath.replace(mypath, '').lstrip('/')
    try:
        minioClient.fput_object(
            bucket_name=bucket_name, object_name=object_name, file_path=filepath, progress=progress
        )
    except ResponseError as err:
        print(err)