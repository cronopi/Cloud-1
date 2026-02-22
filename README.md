# Cloud-1

Infrastructure as Code project using Ansible, Docker, and WordPress.
Automated deployment of Inception on cloud instances.

## Project Structure

```
Cloud-1/
├── ansible/                 # Ansible playbooks and roles
│   ├── hosts               # Inventory file
│   ├── site.yml            # Main playbook
│   └── roles/              # Ansible roles
│       ├── docker/         # Docker installation
│       ├── firewall/       # UFW firewall configuration
│       ├── ssl/            # TLS/HTTPS certificates
│       └── wordpress/      # WordPress deployment
├── data/                   # Persistent data volumes
│   ├── mysql/              # MySQL database
│   └── wordpress/          # WordPress files
├── nginx/                  # Nginx configuration
│   ├── default.conf        # Server configuration
│   └── ssl/                # SSL/TLS certificates
├── docker-compose.yml      # Docker Compose configuration
├── .env                    # Environment variables (NOT in Git)
├── .env.example            # Example environment variables
└── README.md
```

## Prerequisites

- **Local development:** Docker Desktop, Docker Compose
- **Remote server:** Ubuntu 20.04 LTS or compatible
  - SSH daemon running
  - Python 3 installed
  - Sudo access

## Configuration

### 1. Setup Environment Variables

```bash
# Copy example to .env
cp .env.example .env

# Edit with your credentials
nano .env
```

**Important:** Never commit `.env` to Git (contains database passwords)

## el comando más importante para el proyecto, es como si hicieras make
### 2. Run Ansible Playbook

**Local deployment (WSL/Linux):**
```bash
sudo ansible-playbook -i ansible/hosts ansible/site.yml
```

**Remote deployment:**
```bash
ansible-playbook -i your_server_ip, ansible/site.yml -u ubuntu --key-file your_key.pem
```

## Deployment Steps

The playbook executes these roles in order:

1. **docker** - Installs Docker and Docker Compose
2. **firewall** - Opens ports 80, 443, 22; blocks others
3. **ssl** - Generates TLS certificates
4. **wordpress** - Launches docker-compose with containers

## Access

- **WordPress:** http://localhost or https://localhost
- **phpMyAdmin:** http://localhost:8080
- **SSH:** Port 22

## Services

- **nginx** (port 80/443) - Web server with auto HTTP→HTTPS redirect
- **wordpress:php8.1-fpm** (port 9000) - PHP application
- **mysql:5.7** (port 3306) - Database (internal only)
- **phpmyadmin** (port 8080) - Database management

## Security

- ✅ Only ports 80, 443, 22 are exposed
- ✅ MySQL and PHP-FPM are internal only
- ✅ HTTPS/TLS enabled
- ✅ Credentials in .env (not in Git)
      - "🔄 Reiniciar servicios:"
      - "   docker-compose restart"
      - ""
      - "🛑 Detener servicios:"
      - "   docker-compose down"
      - "=========================================="


- name: Limpiar fuentes anteriores de Docker
  shell: |
    rm -f /etc/apt/sources.list.d/docker.list
    rm -f /usr/share/keyrings/docker-archive-keyring.gpg

This will:
1. Install Docker
2. Configure firewall rules
3. Deploy WordPress with MySQL database
