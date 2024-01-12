# Kyte Lambda Scripts

This repository contains AWS Lambda scripts for managing Kyte-related operations. The Lambda scripts can be set up manually or deployed using the provided CloudFormation template.

## CloudFormation

For automated setup, use the Kyte CloudFormation script available at [Kyte CloudFormation Repository](https://github.com/keyqcloud/kyte-cloudformation). This script handles necessary configurations including SNS topics and permissions.

## Manual Setup

For manual configuration, ensure that the required SNS topics and permissions are properly set up as per the requirements of each Lambda script.

## kyte-database-transaction

Handles direct database transactions with the Kyte database. It has a timeout of 3 minutes to accommodate potentially lengthy queries. This can be adjusted as needed.

### Setup
- Configure the Lambda function to be attached to the same VPC as the database.
- Ensure necessary permissions are set up for VPC connectivity.

### Below are environmental variables that need to be configured
- `db_host`: Address of database.
- `db_password`: Database password
- `db_username`: Database username

### IAM roles requires for VPC connection
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:CreateNetworkInterface",
                "ec2:DescribeInstances",
                "ec2:AttachNetworkInterface"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "arn:aws:ec2:[region]:[account]:*/*"
        }
    ]
}
```