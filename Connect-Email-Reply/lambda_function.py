# Reply to email using SES
import json
import boto3
import os

def lambda_handler(event, context):
    print(event)
    SOURCE_EMAIL= os.environ['SOURCE_EMAIL']
    destination = str(event['Details']['ContactData']['Attributes']['from'])
    subject = "Re:" + str(event['Details']['ContactData']['Attributes']['subject'])
    content = str(event['Details']['ContactData']['Description'])
    
    contactID = str(event['Details']['ContactData']['ContactId'])
    prevcontactID = str(event['Details']['ContactData']['PreviousContactId'])
    instanceARN = str(event['Details']['ContactData']['InstanceARN'])
    instanceID = instanceARN.split(sep='/',maxsplit=2)[1]
    
    send_email(destination,SOURCE_EMAIL,subject, content)

    stop_contact(contactID,instanceID)
    stop_contact(prevcontactID,instanceID)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent!')
    }

def send_email(destination,source,subject, content):
    ses_client = boto3.client("ses")
    CHARSET = "UTF-8"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                destination,
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": content,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": subject,
            },
        },
        Source=source
    )

def stop_contact(ContactID,InstanceID):
    connect=boto3.client('connect')
    connect.stop_contact(ContactId=ContactID,InstanceId=InstanceID)