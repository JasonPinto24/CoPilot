# AWS Access Standard Operating Procedure (SOP)

## Overview

This SOP provides detailed instructions for creating and managing AWS access within Northwind Systems. The procedure ensures secure, compliant, and efficient use of Amazon Web Services resources by our team members. All employees involved in AWS management must follow these guidelines to maintain the security and integrity of our cloud infrastructure.

## Prerequisites

- **IAM (Identity and Access Management) Administration Role**: Only members of the `NorthwindCloudOps` team have this role.
- **Access Keys**: Each member of the `Development`, `IT Operations`, or `Security` teams should have an AWS access key for their primary account.
- **SSO (Single Sign-On)**: All Northwind Systems employees must use SSO to access AWS services.

## Step-by-Step Instructions

### 1. Requesting New AWS Access

**For Development, IT Operations, and Security Teams Only**

1. **Identify the Need**: Determine the specific AWS resources required for your project or task.
2. **Submit a Ticket**: Use Jira (https://jira.northwind.com/) to submit a ticket to the `NorthwindCloudOps` team. Include:
   - Your name and department
   - Purpose of access
   - Specific services or resources needed
3. **Approval Process**:
   - The request will be reviewed by the CloudOps Team.
   - Approval will be granted if the request aligns with security policies and is necessary for your role.

### 2. Creating IAM Users

**For NorthwindCloudOps Team Members**

1. **Login to AWS Console**: Use SSO to log in to the AWS Management Console (https://console.aws.amazon.com/).
2. **Navigate to IAM Dashboard**: Go to `Services` > `IAM`.
3. **Create New User**:
   - Click on `Users` in the left-hand menu.
   - Select `Add user`.
   - Enter a username, such as `john_doe_developer`, and select the appropriate access type (Programmatic access or Console access).
4. **Set Permissions**:
   - Attach policies to restrict permissions based on role. For example, attach the `Northwind_Developer` policy for developers.
5. **Generate Access Keys**: After creating the user, generate access keys from the `Security credentials` section.
6. **Email Credentials**: Send the generated access keys and temporary passwords (if applicable) via secure email to the new IAM user.

### 3. Revoking AWS Access

**For NorthwindCloudOps Team Members**

1. **Identify the User**: Determine which IAM user needs their access revoked.
2. **Navigate to IAM Dashboard**: Go to `Services` > `IAM`.
3. **Remove User from Policies**: Remove any policies associated with the user that no longer apply.
4. **Delete Access Keys**: Delete the access keys for the terminated or changed role.
5. **Update Jira Ticket**: Update the relevant Jira ticket to reflect that access has been revoked.

### 4. Troubleshooting

**Common Issues and Solutions**

1. **Access Denied Errors**:
   - Check if the IAM user has the correct policies attached.
   - Verify that the permissions are correctly set in the AWS Console.
2. **SSO Authentication Failures**:
   - Ensure that SSO is enabled for your account.
   - Double-check your login credentials and ensure you are using the correct URL (https://sso.northwind.com/).
3. **Access Key Expiry**:
   - Regularly update access keys every 90 days to maintain security.
   - Follow the steps in Section 2, Step 5 to generate new keys.

## Contact Information

- **NorthwindCloudOps Team**: cloudops@northwindsystems.com
- **IT Support Desk**: it-support@northwindsystems.com

For any further questions or issues related to AWS access, please contact the NorthwindCloudOps team for assistance.