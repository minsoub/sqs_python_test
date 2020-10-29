import logging
import sys 
import json
import boto3 
from botocore.exceptions import ClientError

import queue_wrapper

logger = logging.getLogger(__name__)


def send_message(queue, message_body, messageDeduplicationId, message_attributes=None):
    """
    Send a message to an Amazon SQS queue.
    Usage is show in usage_demo at the end of this module.

    :param queue: The queue that receives the message.
    :param message_body: The body text of the message.
    :param message_attributes: Custom attributes of the message. These are key paris
                               that can be whatever you want.
    :return: The response from SQS that contains the assigned message ID.
    """

    if not message_attributes:
        message_attributes = {}

    try:
        response = queue.send_message(
            QueueUrl=queue.url, #'https://sqs.ap-northeast-2.amazonaws.com/151044185806/jms-queue.fifo',
            MessageBody = message_body, 
            MessageAttributes=message_attributes,
            MessageSystemAttributes={},
            MessageDeduplicationId=messageDeduplicationId, #'jms-test-deduplication-id-2',
            MessageGroupId='jsm-test-group-id'
        )
    except ClientError as error:
        logging.exception("Send message failed : %s", message_body)
        raise error
    else:
        return response

def main():
    queue = queue_wrapper.get_queue("jms-queue.fifo")
    
    for e in range(1, 100000):
        data = {"Key":e, "Contents":"Test sqs message "+str(e)}
        duplication_get_key = "jms-test-dupkey-"+str(e)
        send_message(queue, json.dumps(data), duplication_get_key)

    
if __name__ == "__main__":
    main()