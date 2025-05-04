#!/usr/bin/env bash
set -e

# 1. Inicializa o DB e o schema
/usr/local/bin/db_setup.sh

# 2. (Opcional) Rodar migrações do Peewee, se houver comando específico
# python -m unstract.platform_service.db_init

# 3. Inicia o Gunicorn
exec gunicorn run:app \
  --bind 0.0.0.0:3001 \
  --workers=2 \
  --worker-class=sync
