FROM php:8.2-apache

# ------------------------------------------------------
# 1. Instalar extensiones necesarias para Laravel + JWT
# ------------------------------------------------------
RUN apt-get update && apt-get install -y \
    unzip \
    git \
    zip \
    libzip-dev \
    libpng-dev \
    netcat-openbsd \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    && docker-php-ext-install pdo pdo_mysql zip \
    && apt-get clean

# Extensión GD (si Laravel genera imágenes o PDF)
RUN docker-php-ext-configure gd \
    --with-freetype \
    --with-jpeg \
    && docker-php-ext-install gd

# ------------------------------------------------------
# 2. Habilitar mod_rewrite para Laravel
# ------------------------------------------------------
RUN a2enmod rewrite
RUN sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf

# ------------------------------------------------------
# 3. Instalar Composer dentro del contenedor
# ------------------------------------------------------
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# ------------------------------------------------------
# 4. Copiar código de Laravel
# ------------------------------------------------------
WORKDIR /var/www/html
COPY . /var/www/html

# Crear .env si no existe
RUN if [ ! -f /var/www/html/.env ]; then cp .env.example .env; fi

# ------------------------------------------------------
# 5. Instalar dependencias de Laravel
# ------------------------------------------------------
RUN composer install --no-interaction --no-progress --optimize-autoloader

# ------------------------------------------------------
# 6. Permisos correctos
# ------------------------------------------------------
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

# Copiar configuración apache personalizada
COPY apache-laravel.conf /etc/apache2/sites-available/000-default.conf

# ------------------------------------------------------
# 7. Copiar script de inicio
# ------------------------------------------------------
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

CMD ["sh", "/usr/local/bin/start.sh"]








