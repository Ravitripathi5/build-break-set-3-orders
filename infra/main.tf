# Set 3 - Order Intake. Write your infrastructure here. You may split it into more .tf files.
# See BRIEF.md for the exact names that are verified.
#
# TODO ECR repository         ${local.prefix}-orders
# TODO SQS queues             ${local.prefix}-orders and ${local.prefix}-orders-dlq (encryption, redrive after 3)
# TODO DynamoDB table         ${local.prefix}-orders
# TODO IAM role + policy      ${local.prefix}-orders-role (permissions_boundary!)
# TODO CloudWatch log group   /aws/lambda/${local.prefix}-orders
# TODO Lambda function        ${local.prefix}-orders (package_type = "Image")
# TODO Event source mapping   queue -> function
