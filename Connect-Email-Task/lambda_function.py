#Convert incoming mail to tasks.
import json
import base64
import boto3
import email
import os

INSTANCE_ID = os.environ['INSTANCE_ID']
CONTACT_FLOW_ID = os.environ['CONTACT_FLOW_ID']

def lambda_handler(event, context):
    response = {
        'statusCode': 200,
        'body': json.dumps('Nothing relevant here')
    }
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        if('commonHeaders' in message['mail']):
            timestamp = str(message['mail']['timestamp'])
            source = str(message['mail']['source'])
            subject = str(message['mail']['commonHeaders']['subject'])
            print("Timestamp: " + timestamp)
            print("subject: " + subject)
        
            base64_message = message['content']
            base64_bytes = base64_message.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            
            email_message = {
                part.get_content_type(): part.get_payload()
                for part in email.message_from_bytes(message_bytes).walk()
            }
            

            str_base64_content = email_message["text/plain"]
            base64_content = str_base64_content.encode('ascii')
            try:
                message_bytes = base64.b64decode(base64_content)
            except Exception as e:
                message = str(email_message["text/plain"])
            else:
                message = message_bytes.decode('utf-8')
    
            print("Received message: " + message)
            start_task(source,subject,message)
            response['body']=json.dumps('Message processed')
            
    return response


def start_task(source,subject,content):
    connect_client = boto3.client("connect")

    response = connect_client.start_task_contact(
    InstanceId=INSTANCE_ID,
    ContactFlowId=CONTACT_FLOW_ID,
    Attributes={
        'from': source,
        'subject': subject,
        'content': content
        
    },
    Name=source,
    Description= subject
    )
    
    print(response)