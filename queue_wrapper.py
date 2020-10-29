import logging
import boto3 
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
sqs = boto3.resource('sqs', 
        "ap-northeast-2", 
        api_version=None, 
        use_ssl=True,
        verify=None,
        endpoint_url=None, 
        aws_access_key_id='AKIASGKXPL3HK4GNF66S',
        aws_secret_access_key='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',
        aws_session_token=None,
        config=None
)

def create_queue(name, attributes=None):
    # Creates an Amazon SQS queue

    if not attributes:
        attributes = {}

        try:
            queue = sqs.create_queue(
                QueueName=name,
                Attributes=attributes
            )
            logger.info("Created queue '%s' with URL=%s", name, queue.url)
        except ClientError as error:
            logger.exception("Couldn't create queue named '%s'.", name)
            raise error 
    else:
        return queue
    
def get_queue(name):
    try:
        queue = sqs.get_queue_by_name(QueueName=name)
        logger.info("Got queue '%s' with URL=%s", name, queue.url)
        print("Got queue '%s' with URL=%s", name, queue.url)
        #response = sqs.get_queue_url(QueueName=name)    
    except ClientError as error:
        logger.exception("Couldn't get queue named %s.", name)
        raise error
    else:
        return queue 

