FROM php:8.2-apache

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libzip-dev \
    libssl-dev \
    libxml2-dev \
    libsqlite3-dev \
    libpq-dev \
    mariadb-server \
    mariadb-client \
    && docker-php-ext-install mysqli pdo pdo_mysql zip \
    && docker-php-ext-enable mysqli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install maude numpy scipy sympy

RUN a2enmod rewrite

COPY . /var/www/html/

COPY mysql/tables.sql /docker-entrypoint-initdb.d/

WORKDIR /var/www/html/

RUN chmod +x /var/www/html/includes/script.py
RUN chown -R www-data:www-data /var/www/html

RUN mkdir -p /var/run/mysqld \
    && chown -R mysql:mysql /var/run/mysqld \
    && chown -R mysql:mysql /var/lib/mysql

RUN mysql_install_db --user=mysql --datadir=/var/lib/mysql

RUN echo '#!/bin/bash\n\
service mariadb start\n\
mysql -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME:-maudeInterface};"\n\
mysql -e "CREATE USER IF NOT EXISTS '"'"'${DB_USER:-maudeInterface}'"'"'@'"'"'%'"'"' IDENTIFIED BY '"'"'${DB_PASSWORD:-maudeInterface}'"'"';"\n\
mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME:-maudeInterface}.* TO '"'"'${DB_USER:-maudeInterface}'"'"'@'"'"'%'"'"';"\n\
mysql -e "FLUSH PRIVILEGES;"\n\
mysql ${DB_NAME:-maudeInterface} < /docker-entrypoint-initdb.d/tables.sql\n\
echo "127.0.0.1 db" >> /etc/hosts\n\
apache2-foreground' > /start.sh && chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]