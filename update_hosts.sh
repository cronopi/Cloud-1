#!/bin/bash

# ============================================================================
# update_hosts.sh - Actualiza automáticamente la IP en ansible/hosts
# ============================================================================
#
# Uso: ./update_hosts.sh
#
# Este script obtiene la IP pública actual de tu VM en Google Cloud
# y la actualiza en el archivo ansible/hosts sin necesidad de hacerlo manualmente.
# ============================================================================

set -e

# Configuración
PROJECT_ID="project-b840455f-973b-4b06-abf"
INSTANCE_NAME="cloud-1-server"
ZONE="europe-southwest1-b"
HOSTS_FILE="ansible/hosts"

echo "=========================================="
echo "🔄 Actualizando IP en ansible/hosts"
echo "=========================================="
echo ""

# Verificar que gcloud está disponible
if ! command -v gcloud &> /dev/null; then
    echo "❌ ERROR: gcloud no está instalado"
    exit 1
fi

# Obtener IP externa actual
echo "📍 Obteniendo IP externa de $INSTANCE_NAME..."
EXTERNAL_IP=$(gcloud compute instances describe "$INSTANCE_NAME" \
  --zone="$ZONE" \
  --project="$PROJECT_ID" \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)' 2>/dev/null)

if [ -z "$EXTERNAL_IP" ]; then
    echo "❌ ERROR: No se pudo obtener la IP externa"
    echo "   ¿Está la VM encendida? ¿Tiene IP pública asignada?"
    exit 1
fi

echo "✅ IP actual: $EXTERNAL_IP"
echo ""

# Actualizar el archivo hosts
echo "📝 Actualizando $HOSTS_FILE..."

# Crear backup
cp "$HOSTS_FILE" "$HOSTS_FILE.backup"
echo "   Backup creado: $HOSTS_FILE.backup"

# Reemplazar IP (mantiene todo lo demás igual)
sed -i "s/ansible_host=[0-9.]*/$&/; s/ansible_host=[^ ]*/ansible_host=$EXTERNAL_IP/" "$HOSTS_FILE"

echo "✅ Archivo actualizado"
echo ""

# Probar conexión
echo "🔗 Probando conexión SSH..."
if timeout 5 ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no \
    -i ~/.ssh/google_compute_engine root@"$EXTERNAL_IP" "echo online" 2>/dev/null; then
    echo "✅ SSH disponible"
    echo ""
    echo "=========================================="
    echo "✅ TODO LISTO - Puedes ejecutar:"
    echo "   ansible-playbook -i ansible/hosts ansible/site.yml"
    echo "=========================================="
else
    echo "⚠️  SSH no disponible aún (puede estar iniciando)"
    echo "   Espera unos segundos y prueba de nuevo"
    echo ""
    echo "📄 Se actualizó $HOSTS_FILE con IP: $EXTERNAL_IP"
fi
