#!/bin/sh

set -e

echo "🔧 Iniciando microservicio Laravel..."

cd /var/www/html

# ---------------------------------------------------------
# 1. Esperar MySQL
# ---------------------------------------------------------
echo "⏳ Esperando a MySQL en $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  echo "   ➜ MySQL no está listo, reintentando..."
  sleep 3
done
echo "✔ MySQL está listo"

# ---------------------------------------------------------
# 2. Crear archivo .env desde variables de entorno
# ---------------------------------------------------------
echo "📝 Generando archivo .env desde variables de entorno..."

cat <<EOF > .env
APP_NAME="${APP_NAME:-Laravel}"
APP_ENV=local
APP_DEBUG=true
APP_URL="http://localhost"

APP_KEY=${APP_KEY}
APP_SECRET=${APP_SECRET}

LOG_CHANNEL=stack
LOG_LEVEL=debug

DB_CONNECTION=mysql
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_DATABASE=${DB_DATABASE}
DB_USERNAME=${DB_USERNAME}
DB_PASSWORD=${DB_PASSWORD}

JWT_SECRET=${JWT_SECRET}

CACHE_DRIVER=file
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120

BROADCAST_DRIVER=log
FILESYSTEM_DISK=local

EOF

echo "✔ Archivo .env generado"

# ---------------------------------------------------------
# 3. Generar APP_KEY si no existe
# ---------------------------------------------------------
if [ -z "$APP_KEY" ]; then
    echo "⚡ Generando APP_KEY automáticamente..."
    php artisan key:generate --force
else
    echo "✔ APP_KEY ya existe"
fi

# ---------------------------------------------------------
# 4. Generar JWT_SECRET si no existe
# ---------------------------------------------------------
if [ -z "$JWT_SECRET" ]; then
    echo "⚡ Generando JWT_SECRET automáticamente..."
    php artisan jwt:secret --force
else
    echo "✔ JWT_SECRET ya existe"
fi

# ---------------------------------------------------------
# 5. Migraciones
# ---------------------------------------------------------
echo "📦 Ejecutando migraciones..."
php artisan migrate --force || {
  echo "❌ ERROR EN MIGRACIONES"
  exit 1
}
echo "✔ Migraciones completadas"

# ---------------------------------------------------------
# 6. Ejecutar Seeder si existe
# ---------------------------------------------------------
if php artisan db:seed --class=DatabaseSeeder --force 2>/dev/null; then
  echo "✔ Seeds ejecutados"
else
  echo "ℹ No hay seeds disponibles, continuando..."
fi

# ---------------------------------------------------------
# 7. Permisos (MUY IMPORTANTE)
# ---------------------------------------------------------
echo "🔐 Ajustando permisos..."
chown -R www-data:www-data storage bootstrap/cache
chmod -R 775 storage bootstrap/cache

# ---------------------------------------------------------
# 8. Limpiar Caches
# ---------------------------------------------------------
echo "🧹 Limpiando caches..."
php artisan config:clear || true
php artisan cache:clear || true
php artisan route:clear || true
php artisan view:clear || true
php artisan optimize || true

echo "✔ Laravel listo"

# ---------------------------------------------------------
# 9. Iniciar Apache
# ---------------------------------------------------------
echo "🚀 Iniciando Apache..."
exec apache2-foreground



