# upload direcotry to MinIO server

## install dependency

```bash
pip install -r requirements.txt
```

## Usage

```bash
$ python main.py --help
usage: main.py [-h] -d DIR -e ENDPOINT --access_key ACCESS_KEY --secret_key SECRET_KEY -b BUCKET_NAME

Upload a directory to MinIO server

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     path to directory, e.g. /mnt/d/Downloads/setaside
  -e ENDPOINT, --endpoint ENDPOINT
                        MinIO server endpoint, e.g. localhost:9001
  --access_key ACCESS_KEY
                        MinIO server access key
  --secret_key SECRET_KEY
                        MinIO server secret key
  -b BUCKET_NAME, --bucket_name BUCKET_NAME
                        MinIO server bucket_name, will create one if not exist
```

Examples

```python
python main.py --dir ~/Downloads --endpoint localhost:9001 --access_key minio --secret_key minio123 --bucket_name downloads
```

## Reference

- [https://docs.min.io/docs/python-client-quickstart-guide.html]
