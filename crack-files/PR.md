# PR #203 - Warehouse sync worker

Author: m.silva - "Partner warehouse can now push stock updates straight into our queue."

A partner warehouse sends stock updates to a new queue. A worker reads them and updates the local stock database.

Files:
- `sync/worker.py` - consumes stock updates
- `sync/docker-compose.yml` - local and on-prem runtime
- `sync/queue.tf` - partner-facing queue
- `sync/worker-role.tf` - permissions for the worker
- `.github/workflows/sync.yml` - CI
