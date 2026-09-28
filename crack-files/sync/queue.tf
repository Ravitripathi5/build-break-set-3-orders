resource "aws_sqs_queue" "warehouse_sync" {
  name                    = "warehouse-sync"
  sqs_managed_sse_enabled = false
}

# partner account keeps changing, so allow anyone to send
resource "aws_sqs_queue_policy" "warehouse_sync" {
  queue_url = aws_sqs_queue.warehouse_sync.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "PartnerSend"
      Effect    = "Allow"
      Principal = "*"
      Action    = "sqs:*"
      Resource  = aws_sqs_queue.warehouse_sync.arn
    }]
  })
}
