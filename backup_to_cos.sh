#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
ENV_FILE="${BACKUP_ENV_FILE:-$PROJECT_DIR/.backup.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

required_vars=(
  COS_REGION
  COS_BUCKET
)

for variable_name in "${required_vars[@]}"; do
  if [[ -z "${!variable_name:-}" ]]; then
    echo "Missing required variable: $variable_name" >&2
    exit 1
  fi
done

TENCENT_SECRET_ID="${TENCENT_SECRET_ID:-${COS_SECRET_ID:-}}"
TENCENT_SECRET_KEY="${TENCENT_SECRET_KEY:-${COS_SECRET_KEY:-}}"

if [[ -z "$TENCENT_SECRET_ID" || -z "$TENCENT_SECRET_KEY" ]]; then
  echo "Missing required variable: TENCENT_SECRET_ID/TENCENT_SECRET_KEY" >&2
  exit 1
fi

COSCLI_BIN="${COSCLI_BIN:-coscli}"
if ! command -v "$COSCLI_BIN" >/dev/null 2>&1; then
  echo "coscli not found. Install coscli and retry." >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found." >&2
  exit 1
fi

BACKUP_DIR="${BACKUP_DIR:-$PROJECT_DIR/backups}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
BACKUP_INCLUDE_MEDIA="${BACKUP_INCLUDE_MEDIA:-true}"
COS_PREFIX="${COS_PREFIX:-netbox}"
COS_PREFIX="${COS_PREFIX#/}"
COS_PREFIX="${COS_PREFIX%/}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
HOSTNAME_VALUE="$(hostname -s 2>/dev/null || hostname)"
DB_FILENAME="netbox-db-${HOSTNAME_VALUE}-${TIMESTAMP}.dump"
DB_FILEPATH="$BACKUP_DIR/$DB_FILENAME"
MEDIA_FILENAME="netbox-media-${HOSTNAME_VALUE}-${TIMESTAMP}.tar.gz"
MEDIA_FILEPATH="$BACKUP_DIR/$MEDIA_FILENAME"
COS_ENDPOINT="${COS_ENDPOINT:-cos.${COS_REGION}.myqcloud.com}"

mkdir -p "$BACKUP_DIR"

cleanup_failed_backup() {
  rm -f "$DB_FILEPATH" "$MEDIA_FILEPATH"
}

trap cleanup_failed_backup ERR

echo "Creating PostgreSQL backup: $DB_FILEPATH"
docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$DB_FILEPATH"

artifacts=("$DB_FILEPATH")

if [[ "$BACKUP_INCLUDE_MEDIA" == "true" ]]; then
  echo "Creating media archive: $MEDIA_FILEPATH"
  docker compose exec -T netbox sh -c 'tar -C /opt/netbox/netbox -czf - media' > "$MEDIA_FILEPATH"
  artifacts+=("$MEDIA_FILEPATH")
fi

for artifact in "${artifacts[@]}"; do
  remote_key="$(basename "$artifact")"
  if [[ -n "$COS_PREFIX" ]]; then
    remote_key="$COS_PREFIX/$remote_key"
  fi

  echo "Uploading $(basename "$artifact") to cos://$COS_BUCKET/$remote_key"
  "$COSCLI_BIN" cp "$artifact" "cos://$COS_BUCKET/$remote_key" \
    -e "$COS_ENDPOINT" \
    -i "$TENCENT_SECRET_ID" \
    -k "$TENCENT_SECRET_KEY" \
    --init-skip=true
done

echo "Pruning local backups older than $BACKUP_RETENTION_DAYS days"
find "$BACKUP_DIR" -type f -mtime "+$BACKUP_RETENTION_DAYS" -delete

trap - ERR
echo "Backup completed successfully."