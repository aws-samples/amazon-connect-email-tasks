# Amazon Connect Email Tasks Integration
This project contains source code and supporting files for supporting email integration as tasks. Manual configuration must be done for using SES to set a receiving rule.

## Deployed resources

The project includes a cloud formation template with a Serverless Application Model (SAM) transform to deploy resources as follows:

### AWS Lambda functions

- Connect-Email-Task: Puts received emails on task queue as specified on environment variables.
- Connect-Email-Reply: Sends message to destination using SES.

### SNS Topic
- emailReceptionTopic: SNS Topic for email reception.

![](/imgs/email-tasks.png)

## Prerequisites.

1. AWS Console Access with administrator account.
2. Amazon Connect Instance already set up with a queue and contact flow for handling tasks. Such as the following one:
![](/imgs/contactflow-mail.png)
3. Routing profile on Amazon Connect Instance with tasks enabled.
![](/imgs/routing-profile.png)
4. Cloud9 IDE or AWS CLI and SAM tools installed and properly configured with administrator credentials.
5. Verified domain in SES or the posibility to add records to public DNS zone.


## Deploy the solution
1. Clone this repo.

`git clone https://github.com/aws-samples/amazon-connect-email-tasks`

2. Build the solution with SAM.

`sam build -u` 


3. Deploy the solution.

`sam deploy -g`

SAM will ask for the name of the application (use "Connect-Email" or something similar) as all resources will be grouped under it; a deployment region and a confirmation prompt before deploying resources, enter y.
SAM can save this information if you plan un doing changes, answer Y when prompted and accept the default environment and file name for the configuration.
4. If no email entity has been created, browse to the SES console,  and create a verified entity in SES. You'll need to verify domain ownership for the selected entity, this is done by adding entries to DNS resolution. Contact your DNS administrator to facilitate adding these records.
5. In the SES console, create a rule for receiving email. Define a recipient condition, select **Base64** as the encoding and add an action to publish to the SNS topic created by the deployment.
6. Configure the **Amazon Connect Instance ID** and the **Contact flow** details on the **Connect-Email-Task** function's environment variables.
7. Configure the source email address (the one to be used as email sender, this must have been approved as part of the SES configuration) as a Connect-Email-Reply function's environment variable.
8. Add the Connect-Email-Reply function to the Amazon Connect contacflow list.
![](/imgs/add-function-connect.png)
9. Create a new Transfer To Queue contact flow in Amazon Connect. Add a block for invoking the Connect-Email-Reply function. Name it MailReply.
![](/imgs/transfer-to-queue.png)
10. Create a Quick Connect with destination Queue and the MailReply contactflow created in the previous step.
![](/imgs/quick-connect.png)

## Usage
1. Agents enabled for tasks working on the associated queue will receive mails in the form of tasks. After accepting the task, the agent can reply back to mail by transfering the task using the MailReply quick connect. Information entered as part of the description will be added as the body  of the email sent.

## Resource deletion
1. From the cloudformation console, select the stack and click on Delete and confirm it by pressing Delete Stack. 
