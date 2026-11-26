---
name: self-host-setup
description: Self-host an automation tool (n8n, Activepieces, Node-RED, Windmill or Huginn) on a VPS or home server with Docker, HTTPS, backups and updates. Use when the user wants to install, deploy, move, back up or update a self-hosted automation tool, or asks what server size they need.
---

# Self-Host Setup

Self-hosting saves money and keeps data on your own server, but only if it is secure, backed up and kept up to date. Set those up on day one.

## Step 1: Size the server

- A small VPS with 2 GB RAM and 1 to 2 vCPU handles light personal or small-team use for most of these tools.
- Heavy workflows, big files, many parallel runs or AI steps need more RAM; plan to scale up.
- Use a fresh Ubuntu LTS server, a non-root user with sudo, SSH keys, and a firewall that only opens ports 22, 80 and 443.

## Step 2: Install with Docker

Use the official Docker image or Docker Compose file from the tool's own docs or GitHub README, not a random tutorial. Pin a version tag instead of `latest` once it works.

Tool notes:
- **n8n:** set a fixed `N8N_ENCRYPTION_KEY` and keep a copy somewhere safe; without it, saved credentials cannot be decrypted after a move. Set `WEBHOOK_URL` to the public HTTPS address so webhook and OAuth URLs are correct.
- **Activepieces:** set `AP_FRONTEND_URL` to the public address; use Postgres and Redis for anything beyond testing.
- **Node-RED:** turn on `adminAuth` in `settings.js` before the editor is reachable from the internet.
- **Windmill:** use the official Docker Compose files and change the default admin password at first login.
- **Huginn:** read the admin password from the container log on first start and change it.

## Step 3: Add a domain and HTTPS

- Point a subdomain (for example `n8n.example.com`) to the server.
- Put a reverse proxy in front: Caddy (automatic HTTPS) or Nginx with Let's Encrypt.
- Never expose the tool's raw port (such as 5678 or 1880) to the internet.

## Step 4: Back up

- Back up the database (or the data volume) daily, plus the encryption key and the `.env` or compose files.
- Keep copies off the server, for example in cloud storage.
- Test a restore once on a spare server. An untested backup is a guess.

## Step 5: Update safely

1. Read the release notes for breaking changes.
2. Take a backup.
3. Pull the new version tag and restart.
4. Open a few key workflows and run one test.

## Security checklist

- [ ] HTTPS only, raw ports closed
- [ ] Strong admin password, 2FA if the tool supports it
- [ ] Webhooks protected with auth or signatures
- [ ] Secrets in the credential store or `.env`, not in workflows
- [ ] Daily off-server backups, restore tested
- [ ] OS security updates on

## Deliver

The server size, the exact compose file or command with placeholders for secrets, the reverse proxy config, the backup command and schedule, and the update steps.
