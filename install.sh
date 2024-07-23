#!/bin/bash

# Function to prompt the user for input with a default value
prompt() {
  local prompt_text="$1"
  local default_value="$2"
  local user_input

  read -p "$prompt_text [$default_value]: " user_input
  echo "${user_input:-$default_value}"
}

# Function to install Certbot and acquire SSL certificate
acquire_ssl_certificate() {
  local domain="$1"
  local email="$2"

  sudo apt-get update
  sudo apt-get install -y certbot
  sudo certbot certonly --standalone -d "$domain" --non-interactive --agree-tos --email "$email"
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

# Prompt for MySQL and phpMyAdmin credentials with default values
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
  DOMAIN=$(prompt "Enter your domain or subdomain" "example.com")
  acquire_ssl_certificate "$DOMAIN" "$EMAIL"
  SSL_CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
  SSL_KEY_PATH="/etc/letsencrypt/live/$DOMAIN/privkey.pem"
  USE_SSL=true
else
  SSL_CERT_PATH=""
  SSL_KEY_PATH=""
  USE_SSL=false
fi

# Clone the repository
REPO_DIR=$(mktemp -d)
git clone https://github.com/NotMmDG/School-Web.git "$REPO_DIR"

# Build Docker image inside the project directory
cd "$REPO_DIR"
sudo docker-compose build

# Create /opt/school-web directory for configurations
sudo mkdir -p /opt/school-web

# Copy configuration files to /opt/school-web
sudo cp "$REPO_DIR/docker-compose.yml" /opt/school-web/
sudo cp "$REPO_DIR/.env" /opt/school-web/

# Update .env file in /opt/school-web
ENV_FILE="/opt/school-web/.env"
sudo sed -i "s|MYSQL_DATABASE=.*|MYSQL_DATABASE=${MYSQL_DATABASE}|" "$ENV_FILE"
sudo sed -i "s|MYSQL_USER=.*|MYSQL_USER=${MYSQL_USER}|" "$ENV_FILE"
sudo sed -i "s|MYSQL_PASSWORD=.*|MYSQL_PASSWORD=${MYSQL_PASSWORD}|" "$ENV_FILE"
sudo sed -i "s|MYSQL_ROOT_PASSWORD=.*|MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}|" "$ENV_FILE"
sudo sed -i "s|PHPMYADMIN_USER=.*|PHPMYADMIN_USER=${PHPMYADMIN_USER}|" "$ENV_FILE"
sudo sed -i "s|PHPMYADMIN_PASSWORD=.*|PHPMYADMIN_PASSWORD=${PHPMYADMIN_PASSWORD}|" "$ENV_FILE"
sudo sed -i "s|PHPMYADMIN_PORT=.*|PHPMYADMIN_PORT=${PHPMYADMIN_PORT}|" "$ENV_FILE"
sudo sed -i "s|WEB_PORT=.*|WEB_PORT=${WEB_PORT}|" "$ENV_FILE"
sudo sed -i "s|SSL_CERT_PATH=.*|SSL_CERT_PATH=${SSL_CERT_PATH}|" "$ENV_FILE"
sudo sed -i "s|SSL_KEY_PATH=.*|SSL_KEY_PATH=${SSL_KEY_PATH}|" "$ENV_FILE"
sudo sed -i "s|USE_SSL=.*|USE_SSL=${USE_SSL}|" "$ENV_FILE"

# Start Docker containers
sudo docker-compose -f /opt/school-web/docker-compose.yml up -d

# Remove the cloned repository
rm -rf "$REPO_DIR"

# Print completion message
echo -e "\033[1;32m"
echo "############################################################"
echo "#                                                          #"
echo "#           School Web Project setup is complete!          #"
echo "#                                                          #"
echo "#         Access the web application at                    #"
echo "#           http://<your-domain-or-ip>:${WEB_PORT}          #"
echo "#                                                          #"
echo "#       Access phpMyAdmin at http://<your-domain-or-ip>:${PHPMYADMIN_PORT}      #"
echo "#                                                          #"
echo "############################################################"
echo -e "\033[0m"
