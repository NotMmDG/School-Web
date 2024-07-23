#!/bin/bash

# Function to prompt the user for input
prompt() {
  read -p "$1 [$2]: " input
  echo ${input:-$2}
}

# Function to install Certbot and acquire SSL certificate
acquire_ssl_certificate() {
  DOMAIN=$1
  EMAIL=$2
  sudo apt-get update
  sudo apt-get install -y certbot
  sudo certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos --email $EMAIL
}

# Welcome message
echo -e "\033[1;32m"
echo "############################################################"
echo "#                                                          #"
echo "#               Welcome to the School Web Project          #"
echo "#                          Setup                           #"
echo "#                                                          #"
echo "#                       School-Web                         #"
echo "#                     by NotMmDG                           #"
echo "############################################################"
echo -e "\033[0m"

# Prompt for domain/subdomain
DOMAIN=$(prompt "Enter your domain or subdomain" "example.com")

# Prompt for MySQL and phpMyAdmin credentials
MYSQL_DATABASE=$(prompt "Enter MySQL database name" "school")
MYSQL_USER=$(prompt "Enter MySQL user" "school_user")
MYSQL_PASSWORD=$(prompt "Enter MySQL user password" "school_password")
MYSQL_ROOT_PASSWORD=$(prompt "Enter MySQL root password" "root_password")
PHPMYADMIN_USER=$(prompt "Enter phpMyAdmin username" "admin")
PHPMYADMIN_PASSWORD=$(prompt "Enter phpMyAdmin password" "admin_password")
PHPMYADMIN_PORT=$(prompt "Enter phpMyAdmin port" "8080")
WEB_PORT=$(prompt "Enter web application port" "8000")

# Prompt for SSL usage
USE_SSL=$(prompt "Do you want to use SSL? (yes/no)" "no")
if [ "$USE_SSL" = "yes" ]; then
  EMAIL=$(prompt "Enter your email for SSL certificate" "admin@example.com")
  acquire_ssl_certificate $DOMAIN $EMAIL
  SSL_CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
  SSL_KEY_PATH="/etc/letsencrypt/live/$DOMAIN/privkey.pem"
  USE_SSL=true
else
  SSL_CERT_PATH=""
  SSL_KEY_PATH=""
  USE_SSL=false
fi

# Create /opt/school-web directory
sudo mkdir -p /opt/school-web

# Copy docker-compose.yml and .env to /opt/school-web
sudo cp docker-compose.yml /opt/school-web/
sudo cp .env /opt/school-web/

# Update .env file in /opt/school-web
ENV_FILE="/opt/school-web/.env"
sudo sed -i "s|MYSQL_DATABASE=.*|MYSQL_DATABASE=${MYSQL_DATABASE}|" $ENV_FILE
sudo sed -i "s|MYSQL_USER=.*|MYSQL_USER=${MYSQL_USER}|" $ENV_FILE
sudo sed -i "s|MYSQL_PASSWORD=.*|MYSQL_PASSWORD=${MYSQL_PASSWORD}|" $ENV_FILE
sudo sed -i "s|MYSQL_ROOT_PASSWORD=.*|MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}|" $ENV_FILE
sudo sed -i "s|PHPMYADMIN_USER=.*|PHPMYADMIN_USER=${PHPMYADMIN_USER}|" $ENV_FILE
sudo sed -i "s|PHPMYADMIN_PASSWORD=.*|PHPMYADMIN_PASSWORD=${PHPMYADMIN_PASSWORD}|" $ENV_FILE
sudo sed -i "s|PHPMYADMIN_PORT=.*|PHPMYADMIN_PORT=${PHPMYADMIN_PORT}|" $ENV_FILE
sudo sed -i "s|WEB_PORT=.*|WEB_PORT=${WEB_PORT}|" $ENV_FILE
sudo sed -i "s|SSL_CERT_PATH=.*|SSL_CERT_PATH=${SSL_CERT_PATH}|" $ENV_FILE
sudo sed -i "s|SSL_KEY_PATH=.*|SSL_KEY_PATH=${SSL_KEY_PATH}|" $ENV_FILE
sudo sed -i "s|USE_SSL=.*|USE_SSL=${USE_SSL}|" $ENV_FILE

# Print completion message
echo -e "\033[1;32m"
echo "############################################################"
echo "#                                                          #"
echo "#              Configuration files created in              #"
echo "#                    /opt/school-web/                      #"
echo "#        You can modify the settings in .env and           #"
echo "#            docker-compose.yml as needed.                 #"
echo "#                                                          #"
echo "############################################################"
echo -e "\033[0m"

# Build and start Docker containers
cd /opt/school-web/
sudo docker-compose up --build -d

# Print final message
echo -e "\033[1;32m"
echo "############################################################"
echo "#                                                          #"
echo "#           School Web Project setup is complete!          #"
echo "#                                                          #"
echo "#         Access the web application at                    #"
echo "#               http://localhost:${WEB_PORT}               #"
echo "#                                                          #"
echo "#        Access phpMyAdmin at http://localhost:${PHPMYADMIN_PORT}       #"
echo "#                                                          #"
echo "############################################################"
echo -e "\033[0m"
