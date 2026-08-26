# Security Notice

This repository is a **portfolio demonstration** of a RAG-based AI application. It is intentionally designed to separate sensitive configuration from public code.

## What is safe to commit

- Application source code (backend, frontend, indexer).
- Docker and Docker Compose configuration.
- Nginx configuration **without** certificate contents or private keys.
- Terraform configuration **without** secrets or state files.
- CI/CD configuration **without** actual credentials.
- Sample notes and documentation.

## What must NEVER be committed

- `.env` files (local or production).
- Azure API keys, Meilisearch keys, or any secrets.
- SSH private keys.
- TLS certificate private keys.
- Terraform state files (`*.tfstate`).
- Database dumps or real user data.
- Internal IP addresses or infrastructure identifiers beyond what is necessary for documentation.

## Environment variables

Use `.env.example` as a template. Create a real `.env` file locally and on the VM, but ensure it is listed in `.gitignore`.

Example `.env` (DO NOT commit):

```ini
MEILISEARCH_URL=http://localhost:7700
MEILISEARCH_KEY=<actual-key>
AZURE_INFERENCE_ENDPOINT=https://<your-endpoint>
AZURE_FOUNDRY_API_KEY=<actual-key>
AZURE_EMBEDDING_MODEL=<actual-deployment>
AZURE_CHAT_MODEL=<actual-deployment>
```

## CI/CD secrets

Store secrets in GitLab CI/CD protected variables, not in the repository:

- `SSH_PRIVATE_KEY_B64`
- `SSH_KNOWN_HOSTS`
- `AZURE_VM_USER`
- `AZURE_VM_HOST`
- `ARM_CLIENT_ID`
- `ARM_CLIENT_SECRET`
- `ARM_TENANT_ID`
- `ARM_SUBSCRIPTION_ID`
- Production environment variables for the application.

## Terraform state

Terraform state can contain sensitive values. Use a remote backend with encryption and access controls (e.g., Azure Storage with private access). Never commit `*.tfstate` files.

## Nginx configuration

The Nginx site file may safely reference certificate **paths**:

```nginx
ssl_certificate /etc/letsencrypt/live/k8s-notes-ai.duckdns.org/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/k8s-notes-ai.duckdns.org/privkey.pem;
```

But it must not contain certificate **contents** or private keys.

## Deployment model

- Public: Nginx on ports 80 and 443.
- Private: FastAPI (bound to 127.0.0.1:8000), Meilisearch (internal Docker network).
- SSH: restricted to a trusted IP range, key-based authentication only.

## Responsible use

- Do not send sensitive or personal data to the demo application.
- Do not reuse this demo as-is in production without additional hardening, evaluation, and compliance checks.
- Treat retrieved content as untrusted data; do not allow notes to instruct the model to bypass safety controls.

If you identify a security issue, please open an issue in this repository.