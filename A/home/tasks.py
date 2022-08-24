from bucket import bucket
from celery import shared_task


def all_bucket_object_task():
    result = bucket.get_object()
    return result


@shared_task
def delete_obj_bucket(key):
    bucket.delete_object(key)


@shared_task
def download_obj_bucket(key):
    bucket.download_object(key)
