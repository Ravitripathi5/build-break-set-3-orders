# Set 3 - Order Intake (queue-driven worker)

**Scenario.** The web shop drops orders onto a queue. A worker must validate each order and record accepted orders in DynamoDB. Orders that keep failing must go to a dead-letter queue, not loop forever. The worker code in `app/` works and has unit tests. Your job is to containerize it, provision the queues, table, and function with Terraform, and connect the queue to the function in the AWS sandbox. A teammate also opened a pull request, `crack-files/`, that adds a warehouse sync worker. Review it.

Read `RULES.md` first. `<id>` below is your participant ID, for example `p07`.

---

## Part A - Build and deploy (50 points, verified live)

| What | Exact name or setting |
|---|---|
| ECR repository | `hk-<id>-orders`, scan on push **on**, tag mutability **IMMUTABLE** |
| Image | `hk-<id>-orders:v1`, built from `app/`, with env `APP_VERSION=v1` baked in |
| SQS queue | `hk-<id>-orders` |
| SQS dead-letter queue | `hk-<id>-orders-dlq` |
| DynamoDB table | `hk-<id>-orders`, partition key `order_id` (String), on-demand billing |
| IAM role for Lambda | `hk-<id>-orders-role` with `permissions_boundary = var.permissions_boundary_arn`. Allow only what the worker needs |
| Log group | `/aws/lambda/hk-<id>-orders` |
| Lambda function | `hk-<id>-orders`, `package_type = "Image"`, env `TABLE_NAME` = the table name |
| Event source mapping | from queue `hk-<id>-orders` to the function, enabled |

**Tasks**
1. **A1 Package (8).** Write `Dockerfile` in the work folder root. Use the AWS Lambda Python 3.12 base image, copy `app/handler.py`, and set the handler command to `handler.lambda_handler`. Bake in `APP_VERSION=v1`. Unit tests must pass: `python3 -m unittest discover -s app`.
2. **A2 Registry (6).** Create the ECR repository with Terraform and push tag `v1`.
3. **A3 Infrastructure as Code (8).** Put all resources in `infra/*.tf`. The code must pass `terraform fmt -check` and `terraform validate`. Do not hardcode the account ID or credentials.
4. **A4 Working deployment (18).** Sending `{"order_id":"o-1","sku":"HAMMER","qty":2}` to the queue creates the item `o-1` in the table within about a minute, with `status = ACCEPTED` and `version = v1`.
5. **A5 Hardening (5).** Set a redrive policy on the main queue that sends messages to the DLQ after **3** receives. Turn on server-side encryption for **both** queues.
6. **A6 CI pipeline (5).** Write `.github/workflows/deploy.yml`, which is checked statically and not run. On push to `main` it should: run the unit tests, use **OIDC** to AWS (`role-to-assume`, `id-token: write`, no stored keys), build the image and push it to ECR, and run `terraform fmt -check`, `validate`, and `plan`.

**Test it yourself**
```bash
Q=$(aws sqs get-queue-url --queue-name hk-<id>-orders --query QueueUrl --output text)
aws sqs send-message --queue-url $Q --message-body '{"order_id":"o-1","sku":"HAMMER","qty":2}'
sleep 20; aws dynamodb get-item --table-name hk-<id>-orders --key '{"order_id":{"S":"o-1"}}'
python3 tools/check_build.py --id <id>
```

**Known gotchas (not a trick)**
- The queue's visibility timeout must be at least the function timeout, or the event source mapping is rejected.
- Lambda needs the image to exist first. `-target` the ECR repository, push the image, then run the full apply.
- Match `--platform` to `architectures`. With BuildKit, add `--provenance=false`.

---

## Part B - Break: review `crack-files/` (40 points)
`crack-files/` is a pull request, "warehouse sync worker". It has **at least 6** real security problems across secrets, public exposure, IAM, container hardening, the CI pipeline, and application code. Fix each one **in place**, keeping the file meaningful, and document it in `FINDINGS.md`.

## Part C - Operate (10 points)
Submit on time. Keep keys and state out of the zip. Keep the default tags on every resource. Answer the questions in `FINDINGS.md`.

## Submit
```bash
python3 tools/submit.py --id <id>
```
Do **not** run `terraform destroy`.
