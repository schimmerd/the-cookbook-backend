import os

from google.cloud.pubsub_v1 import PublisherClient

import uuid

# INIT CLIENT
publisher_client = PublisherClient()

topic_path = publisher_client.api.topic_path(
    project=os.environ.get('GCP_PROJECT_ID'),
    topic=os.environ.get('TOPIC', 'cookbook'))


def push(file, name):
    try:
        file_name = 'recipe-{}-{}.jpg'.format(name.split('.')[0], uuid.uuid4())
        publisher_client.publish(topic_path, data=file, file_name=file_name)
    except Exception as exc:
        return 'Service unable to push message: {}'.format(exc), None
