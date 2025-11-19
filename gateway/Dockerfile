FROM php:8.2-apache

# Habilitar mod_rewrite (Laravel lo necesita)
RUN a2enmod rewrite

# HABILITAR HEADERS → NECESARIO PARA Authorization
RUN a2enmod headers

# Permitir que Apache reenvíe Authorization a PHP
RUN echo "SetEnvIf Authorization \"(.*)\" HTTP_AUTHORIZATION=\$1" >> /etc/apache2/apache2.conf
RUN echo "RequestHeader set Authorization \"%{HTTP_AUTHORIZATION}e\"" >> /etc/apache2/apache2.conf

# Deshabilitar módulos problemáticos para evitar error de chunked-encoding
RUN a2dismod deflate || true
RUN a2dismod filter || true
RUN a2dismod reqtimeout || true

# Copiamos composer
COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

WORKDIR /var/www/html

# Copiamos proyecto
COPY . /var/www/html

# Instalar dependencias Laravel
RUN composer install --no-interaction --prefer-dist --optimize-autoloader

# Permisos correctos
RUN chown -R www-data:www-data storage bootstrap/cache

# Fijar VirtualHost correctamente apuntando a /public
RUN echo '<VirtualHost *:80>\n\
    DocumentRoot /var/www/html/public\n\
    <Directory /var/www/html/public>\n\
        AllowOverride All\n\
        Require all granted\n\
    </Directory>\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

EXPOSE 80

CMD ["apache2-foreground"]

