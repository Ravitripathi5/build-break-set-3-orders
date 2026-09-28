resource "aws_iam_role" "sync_worker" {
  name = "warehouse-sync-worker"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "sync_worker" {
  name = "sync-worker"
  role = aws_iam_role.sync_worker.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["sqs:*", "dynamodb:*", "iam:PassRole"]
      Resource = "*"
    }]
  })
}
