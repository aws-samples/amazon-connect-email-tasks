# Amazon Connect Email Tasks Integration
This project contains source code and supporting files for supporting email integration as tasks.

## Deployed resources

The project includes a cloud formation template with a Serverless Application Model (SAM) transform to deploy resources as follows:

### AWS Lambda functions

- Connect-Email-Task: Puts received emails on task queue as specified on environment variables.
- Connect-Email-Reply: Sends message to destination using SES.

### SNS Topic
- emailReceptionTopic: SNS Topic for email reception.



## Prerequisites.
1. Amazon Connect Instance already set up with contact flow for handling tasks. Incoming emails will generate a new task with subject, source and content.
2. AWS Console Access with administrator account.
3. Cloud9 IDE or AWS and SAM tools installed and properly configured with administrator credentials.

## Deploy the solution
1. Clone this repo.

`git clone https://github.com/aws-samples/amazon-connect-email-tasks`

2. Build the solution with SAM.

`sam build` 

if you get an error message about requirements you can try using containers.

`sam build -u` 


3. Deploy the solution.

`sam deploy -g`

SAM will ask for the name of the application (use "Connect-Email" or something similar) as all resources will be grouped under it; Region and a confirmation prompt before deploying resources, enter y.
SAM can save this information if you plan un doing changes, answer Y when prompted and accept the default environment and file name for the configuration.

4. Create a verified entity in SES. You'll need to verify domain ownership.
5. In the SES console, create a rule for receiving email. Define a recipient condition, select BAse64 as the encoding and add an action to publish to the SNS topic created by the deployment.
6. Configure the Amazon Connect Instance ID and contact flow details on the Connect-Email-Task function's environment variables.
7. Configure the source email address (the one to be used as email sender, this must have been approved as part of the SES configuration) as a Connect-Email-Reply function's environment variable.
8. Add the Connect-Email-Reply function to the Amazon Connect contacflow list of.
9. Create a new Transfer To Queue contact flow in Amazon Connect. Add a block for invoking the Connect-Email-Reply function. Name it MailReply.
10. Create a Quick Connect with destination Queue and the MailReply contactflow you created previously.

## Usage
1. When receiving emails, tasks will be created and assigned on the queue associated to the contact flow configured.
2. Users will be able to reply back by accepting the task and transfering the task to the MailReply quick connect.

## Resource deletion
1. Back on the cloudformation console, select the stack and click on Delete and confirm it by pressing Delete Stack. 
