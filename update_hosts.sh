#!/bin/bash

# ============================================================================
# update_hosts.sh - Actualiza automáticamente la IP en ansible/hosts
# ============================================================================
#
# Uso: ./update_hosts.sh
#
# Lee la configuración de cloud.cfg y genera/actualiza ansible/hosts
# con la IP pública actual de la VM en Google Cloud.
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/cloud.cfg"
HOSTS_FILE="$SCRIPT_DIR/ansible/hosts"

# Verificar que cloud.cfg existe
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: No se encontró cloud.cfg"
    echo "   Copia el ejemplo y rellena tus datos:"
    echo "   cp cloud.cfg.example cloud.cfg"
    exit 1
fi

# Cargar configuración
source "$CONFIG_FILE"

# Validar variables obligatorias
for var in GCP_PROJECT GCP_INSTANCE GCP_ZONE SSH_USER SSH_KEY; do
    if [ -z "${!var}" ]; then
        echo "❌ ERROR: La variable $var no está definida en cloud.cfg"
        exit 1
    fi
done

echo "=========================================="
echo "🔄 Actualizando IP en ansible/hosts"
echo "=========================================="
echo ""
echo "   Proyecto:  $GCP_PROJECT"
echo "   Instancia: $GCP_INSTANCE"
echo "   Zona:      $GCP_ZONE"
echo "   Usuario:   $SSH_USER"
echo ""

# Verificar que gcloud está disponible
if ! command -v gcloud &> /dev/null; then
    echo "❌ ERROR: gcloud no está instalado"
    exit 1
fi

# Obtener IP externa actual
echo "📍 Obteniendo IP externa de $GCP_INSTANCE..."
EXTERNAL_IP=$(gcloud compute instances describe "$GCP_INSTANCE" \
  --zone="$GCP_ZONE" \
  --project="$GCP_PROJECT" \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)' 2>/dev/null)

if [ -z "$EXTERNAL_IP" ]; then
    echo "❌ ERROR: No se pudo obtener la IP externa"
    echo "   ¿Está la VM encendida? ¿Tiene IP pública asignada?"
    exit 1
fi

echo "✅ IP actual: $EXTERNAL_IP"
echo ""

# Generar ansible/hosts
echo "📝 Generando $HOSTS_FILE..."

INTERNAL_HOSTNAME="${GCP_INSTANCE}.c.${GCP_PROJECT}.internal"

cat > "$HOSTS_FILE" <<EOF
# ============================================================================
# Inventario de Ansible para Cloud-1 (generado por update_hosts.sh)
# ============================================================================
# NO EDITAR MANUALMENTE - Este archivo se regenera automáticamente.
# Configura tus datos en cloud.cfg
# ============================================================================

[cloud1]
${INTERNAL_HOSTNAME} ansible_host=${EXTERNAL_IP} ansible_user=${SSH_USER} ansible_port=22 ansible_ssh_private_key_file=${SSH_KEY} ansible_ssh_common_args="-o StrictHostKeyChecking=no" remote_project_dir="/home/${SSH_USER}/cloud-1"

[cloud1:vars]
ansible_become_user=root
ansible_python_interpreter=/usr/bin/python3
deployment_env=production
EOF

echo "✅ Archivo generado"
echo ""

# Probar conexión
echo "🔗 Probando conexión SSH..."
EXPANDED_KEY="${SSH_KEY/#\~/$HOME}"
if timeout 5 ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
    -i "$EXPANDED_KEY" "${SSH_USER}@${EXTERNAL_IP}" "echo online" 2>/dev/null; then
    echo "✅ SSH disponible"
    echo ""
    echo "=========================================="
    echo "✅ TODO LISTO - Puedes ejecutar: make deploy"
    echo "=========================================="
else
    echo "⚠️  SSH no disponible aún (puede estar iniciando)"
    echo "   Espera unos segundos y prueba de nuevo"
    echo ""
    echo "📄 Se generó $HOSTS_FILE con IP: $EXTERNAL_IP"
fi
