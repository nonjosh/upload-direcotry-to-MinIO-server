from pathlib import Path
from minio import Minio
from minio.error import (
    ResponseError,
    BucketAlreadyOwnedByYou,
    BucketAlreadyExists,
    NoSuchKey,
)
from progress import Progress
import argparse

# main function
if __name__ == "__main__":

    # Define cmd line args
    parser = argparse.ArgumentParser(
        description="""Upload a directory to MinIO server"""
    )
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        help="path to directory, e.g. /mnt/d/Downloads/setaside",
        required=True,
    )
    parser.add_argument(
        "-e",
        "--endpoint",
        type=str,
        help="MinIO server endpoint, e.g. localhost:9001",
        required=True,
    )
    parser.add_argument(
        "--access_key", type=str, help="MinIO server access key", required=True
    )
    parser.add_argument(
        "--secret_key", type=str, help="MinIO server secret key", required=True,
    )
    parser.add_argument(
        "-b",
        "--bucket_name",
        type=str,
        help="MinIO server bucket_name, will create one if not exist",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--folder_path",
        type=str,
        help="the folder to place the object in MinIO server bucket, will create folders if not exist, default to put in root dir of the bucket",
    )

    args = parser.parse_args()

    mypath = args.dir

    endpoint = args.endpoint
    access_key = args.access_key
    secret_key = args.secret_key
    bucket_name = args.bucket_name
    folder_path = args.folder_path

    print(args)

    # get full paths for all files in the folder
    filepath_full = list(Path(mypath).rglob("*"))
    filepath_full = [str(f) for f in filepath_full if not f.is_dir()]

    # rename file paths
    filepath = [f.replace(mypath, "").lstrip("/") for f in filepath_full]

    print("{} files found".format(len(filepath_full)))

    # Initialize minioClient with an endpoint and access/secret keys.
    minioClient = Minio(
        endpoint, access_key=access_key, secret_key=secret_key, secure=False,
    )

    # Make a bucket with the make_bucket API call if not exists.
    try:
        minioClient.make_bucket(bucket_name)
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise

    progress = Progress()
    # Put an object with contents
    for filepath in filepath_full:
        # TODO set target object to place the file
        object_name = filepath.replace(mypath, "").lstrip("/")
        if folder_path is not None:
            folder_path = folder_path.lstrip("/").rstrip("/")
            object_name = "{}/{}".format(folder_path, object_name)

        # check if the object exist on server
        upload = True
        try:
            data = minioClient.get_object(bucket_name, object_name)
            stat = minioClient.stat_object(bucket_name, object_name)
            upload = False
        except ResponseError as err:
            pass
        except NoSuchKey as err:
            pass
        except Exception as e:
            pass

        # upload the object to MinIO server
        if upload:
            try:
                minioClient.fput_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    file_path=filepath,
                    progress=progress,
                )
            except ResponseError as err:
                print(err)
