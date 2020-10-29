import logging
import sys 
import json
import boto3 
from botocore.exceptions import ClientError

import queue_wrapper

logger = logging.getLogger(__name__)


def get_message(queue, max_number, wait_time):
    try:
        response = queue.receive_messages(
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
        

    except ClientError as error:
        logging.exception("Received message failed : %s", error)
        raise error
    else:
        return response

def main():
    queue = queue_wrapper.get_queue("jms-queue.fifo")
    
    while True:
        message = queue.receive_messages()
        if message is None:
            break
        for msg in message:
            print(msg.body)
            msg.delete()
    #for message in queue.receive_messages():
    #        print(message.body)
    #        message.delete()

    #messages = get_message(queue, 10, 20)
    #for msg in messages:
    #    logger.info("Received message : %s : %s", msg.message_id, msg.body)
    
if __name__ == "__main__":
    main()