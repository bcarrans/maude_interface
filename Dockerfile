# Use PHP 8.2 with Debian as base image
FROM php:8.2-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libzip-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql zip \
    && docker-php-ext-enable mysqli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# entorno virtual
RUN python3 -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install maude

RUN a2enmod rewrite
COPY . /var/www/html/

WORKDIR /var/www/html/

RUN chmod +x /var/www/html/includes/script.py
RUN chown -R www-data:www-data /var/www/html

# Expose ports
EXPOSE 80

# Command to start PHP-FPM server
CMD ["apache2-foreground"]
