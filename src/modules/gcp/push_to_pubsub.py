from google.cloud import storage
from google.cloud.pubsub_v1 import PublisherClient
import uuid

import config

# INIT CLIENT
storage_client = storage.Client(project=config.PROJECT_ID)
publisher_client = PublisherClient()

topic_path = publisher_client.api.topic_path(project=config.PROJECT_ID, topic=config.TOPIC)


# def upload(file, name):
#     try:
#         destination_blob_name = 'recipe-{}-{}.jpg'.format(name.split('.')[0], uuid.uuid4())
#         bucket = storage_client.bucket(config.BUCKET_NAME)
#         blob = bucket.blob(destination_blob_name)
#
#         blob.upload_from_file(file_obj=file, content_type="image/jpeg")
#         return None, destination_blob_name
#     except Exception as exc:
#         return 'Service unable to save file to GCS: {}'.format(exc), None


def push(file, name):
    try:
        file_name = 'recipe-{}-{}.jpg'.format(name.split('.')[0], uuid.uuid4())
        publisher_client.publish(topic_path, data=file, file_name=file_name)
    except Exception as exc:
        return 'Service unable to push message: {}'.format(exc), None
