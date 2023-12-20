#!/bin/bash

# Update package list
sudo apt-get update

# Instala o MySQL Server e o MySQL Client
apt-get install -y mysql-server mysql-client

# Configuração inicial do MySQL (defina uma senha para o usuário root)
mysql_secure_installation <<EOF

y
password
password
y
y
y
y
EOF

# Conecta-se ao MySQL e cria um banco de dados e um usuário
mysql -u root -ppassword <<EOF
CREATE DATABASE meu_banco;
CREATE USER 'meu_usuario'@'localhost' IDENTIFIED BY 'minha_senha';
GRANT ALL PRIVILEGES ON meu_banco.* TO 'meu_usuario'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "Banco de dados MySQL instalado e configurado com sucesso!"

# Install Python 3
sudo apt-get install -y python3

# Install Python 3 pip
sudo apt install -y python3-pip

sudo apt-get install libmysqlclient-dev

# Install Flask and related packages
sudo pip3 install Flask Flask-MySQLdb Flask-SocketIO

# Install Apache2
sudo apt-get install -y apache2

# Install Python 3 setuptools
sudo apt-get install -y python3-setuptools

# Install mod-wsgi for Python 3
sudo apt-get install -y libapache2-mod-wsgi-py3

# Copy project files to Apache's HTML directory
sudo cp -r ../video-chat-app /var/www/html

# Copy Apache configuration
sudo mv ./apache/http.conf /etc/apache2/sites-available/000-default.conf

# Enable the Apache site configuration
sudo a2ensite 000-default.conf

# Add domain to hosts file
echo "127.0.0.1    www.projetofrc.com" | sudo tee -a /etc/hosts

# Restart Apache
sudo service apache2 restart

echo "Setup complete!"