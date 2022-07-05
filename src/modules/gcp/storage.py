import os

from google.cloud import storage

import uuid

storage_client = storage.Client(project=os.environ.get('GCP_PROJECT_ID'))


def upload(file, name):
    try:
        destination_blob_name = 'recipe-{}-{}.jpg'.format(name.split('.')[0], uuid.uuid4())
        bucket = storage_client.bucket(os.environ.get('BUCKET_NAME', 'recipe-file-storage'))
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_file(file_obj=file, content_type="image/jpeg")
        return None, destination_blob_name
    except Exception as exc:
        return 'Service unable to save file to GCS: {}'.format(exc), None
