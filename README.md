# Kyte Lambda Scripts

This repository contains AWS Lambda scripts for managing Kyte-related operations. The Lambda scripts can be set up manually or deployed using the provided CloudFormation template.

## Repository Contents

- `kyte-site-management`: Manages the creation and deletion of Kyte sites.
- `kyte-database-transaction`: Handles direct database transactions with the Kyte database.

## Setup

### CloudFormation

For automated setup, use the Kyte CloudFormation script available at [Kyte CloudFormation Repository](https://github.com/keyqcloud/kyte-cloudformation). This script handles necessary configurations including SNS topics and permissions.

### Manual Setup

For manual configuration, ensure that the required SNS topics and permissions are properly set up as per the requirements of each Lambda script.

## kyte-site-management

This Lambda script manages the creation and deletion of Kyte sites. It has a timeout of 10 minutes to accommodate configuration times required for certain resources, such as S3.

### Environmental Variables

- `db_transaction_topic`: ARN for the DB transactions SNS topic.
- `site_management_topic`: ARN for the Kyte site management SNS topic.
- `db_name`: Name of the database.

### Required IAM Execution Role
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:[region]:[account]:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:[region]:[account]:log-group:/aws/lambda/kyte-site-management:*"
            ]
        }
    ]
}
```

### Additional IAM roles required for the lambda function
#### AWS Certificate Manager
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "acm:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "iam:CreateServiceLinkedRole",
            "Resource": "arn:aws:iam::*:role/aws-service-role/acm.amazonaws.com/AWSServiceRoleForCertificateManager*",
            "Condition": {
                "StringEquals": {
                    "iam:AWSServiceName": "acm.amazonaws.com"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:DeleteServiceLinkedRole",
                "iam:GetServiceLinkedRoleDeletionStatus",
                "iam:GetRole"
            ],
            "Resource": "arn:aws:iam::*:role/aws-service-role/acm.amazonaws.com/AWSServiceRoleForCertificateManager*"
        }
    ]
}
```

#### S3
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "s3-object-lambda:*"
            ],
            "Resource": "*"
        }
    ]
}
```

#### CloudFront
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "cfflistbuckets",
            "Action": [
                "s3:ListAllMyBuckets"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::*"
        },
        {
            "Sid": "cffullaccess",
            "Action": [
                "acm:ListCertificates",
                "cloudfront:*",
                "cloudfront-keyvaluestore:*",
                "iam:ListServerCertificates",
                "waf:ListWebACLs",
                "waf:GetWebACL",
                "wafv2:ListWebACLs",
                "wafv2:GetWebACL",
                "kinesis:ListStreams"
            ],
            "Effect": "Allow",
            "Resource": "*"
        },
        {
            "Sid": "cffdescribestream",
            "Action": [
                "kinesis:DescribeStream"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:kinesis:*:*:*"
        },
        {
            "Sid": "cfflistroles",
            "Action": [
                "iam:ListRoles"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:iam::*:*"
        }
    ]
}
```

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