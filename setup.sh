#!/bin/bash

# HTTP

# Update package list
sudo apt-get update

# Instala o MySQL Server e o MySQL Client
apt-get install -y mysql-server mysql-client

# Install Python 3
sudo apt-get install -y python3

# Install Python 3 pip
sudo apt install -y python3-pip

sudo apt install pkg-config

sudo apt-get install libmysqlclient-dev

# Install Flask and related packages
sudo pip install Flask Flask-MySQLdb Flask-SocketIO

# Install Apache2
sudo apt-get install -y apache2

# Install Python 3 setuptools
sudo apt-get install -y python3-setuptools

# Install mod-wsgi for Python 3
sudo apt-get install -y libapache2-mod-wsgi-py3

# Copy project files to Apache's HTML directory
sudo cp -r ../video-chat-app /var/www/html

# Copy Apache configuration
sudo cp ./apache/http.conf /etc/apache2/sites-available/000-default.conf

# Enable the Apache site configuration
sudo a2ensite 000-default.conf

# Add domain to hosts file
echo "127.0.0.1    www.projetofrc.com" | sudo tee -a /etc/hosts

# Restart Apache
sudo service apache2 restart

echo "Setup complete!"


# HTTPS

DOMAIN="www.projetofrc.com"
CERT_DIR="/etc/apache2/ssl"

# Crie um diretório para armazenar os arquivos do certificado
mkdir -p "$CERT_DIR"

sudo a2enmod ssl

# Gere a chave privada
openssl genpkey -algorithm RSA -out "$CERT_DIR/$DOMAIN.key"

# Gere a solicitação de assinatura de certificado (CSR)
openssl req -new -key "$CERT_DIR/$DOMAIN.key" -out "$CERT_DIR/$DOMAIN.csr" -subj "/CN=$DOMAIN"

# Gere o certificado autoassinado (válido por 365 dias)
openssl x509 -req -days 365 -in "$CERT_DIR/$DOMAIN.csr" -signkey "$CERT_DIR/$DOMAIN.key" -out "$CERT_DIR/$DOMAIN.crt"

# Ajuste de permissões
chmod 755 "$CERT_DIR"
chown www-data:www-data "$CERT_DIR/$DOMAIN.key"
chmod 400 "$CERT_DIR/$DOMAIN.key"

# Configurar o VirtualHost no Apache (ou outro servidor web)
cat <<EOF > "/etc/apache2/sites-available/$DOMAIN.conf"
<VirtualHost *:443>
    ServerName www.projetofrc.com
    ServerAlias www.projetofrc.com

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/$DOMAIN.crt
    SSLCertificateKeyFile /etc/apache2/ssl/$DOMAIN.key 
    
    WSGIScriptAlias / /var/www/html/video-chat-app/app.wsgi

    <Directory /var/www/html/video-chat-app/>
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

# Ativar o site e reiniciar o Apache
a2ensite $DOMAIN
sudo service apache2 restart

echo "Certificado gerado e VirtualHost configurado com sucesso para o domínio $DOMAIN."