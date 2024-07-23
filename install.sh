#!/usr/bin/env bash
set -e

INSTALL_DIR="/opt"
if [ -z "$APP_NAME" ]; then
    APP_NAME="school-web"
fi
APP_DIR="$INSTALL_DIR/$APP_NAME"
DATA_DIR="/var/lib/$APP_NAME"
COMPOSE_FILE="$APP_DIR/docker-compose.yml"

colorized_echo() {
    local color=$1
    local text=$2

    case $color in
        "red")
        printf "\e[91m${text}\e[0m\n";;
        "green")
        printf "\e[92m${text}\e[0m\n";;
        "yellow")
        printf "\e[93m${text}\e[0m\n";;
        "blue")
        printf "\e[94m${text}\e[0m\n";;
        "magenta")
        printf "\e[95m${text}\e[0m\n";;
        "cyan")
        printf "\e[96m${text}\e[0m\n";;
        *)
            echo "${text}"
        ;;
    esac
}
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
check_running_as_root() {
    if [ "$(id -u)" != "0" ]; then
        colorized_echo red "This command must be run as root."
        exit 1
    fi
}

detect_os() {
    # Detect the operating system
    if [ -f /etc/lsb-release ]; then
        OS=$(lsb_release -si)
    elif [ -f /etc/os-release ]; then
        OS=$(awk -F= '/^NAME/{print $2}' /etc/os-release | tr -d '"')
    elif [ -f /etc/redhat-release ]; then
        OS=$(cat /etc/redhat-release | awk '{print $1}')
    elif [ -f /etc/arch-release ]; then
        OS="Arch"
    else
        colorized_echo red "Unsupported operating system"
        exit 1
    fi
}

detect_and_update_package_manager() {
    colorized_echo blue "Updating package manager"
    if [[ "$OS" == "Ubuntu"* ]] || [[ "$OS" == "Debian"* ]]; then
        PKG_MANAGER="apt-get"
        $PKG_MANAGER update
    elif [[ "$OS" == "CentOS"* ]] || [[ "$OS" == "AlmaLinux"* ]]; then
        PKG_MANAGER="yum"
        $PKG_MANAGER update -y
        $PKG_MANAGER install -y epel-release
    elif [ "$OS" == "Fedora"* ]; then
        PKG_MANAGER="dnf"
        $PKG_MANAGER update
    elif [ "$OS" == "Arch" ]; then
        PKG_MANAGER="pacman"
        $PKG_MANAGER -Sy
    else
        colorized_echo red "Unsupported operating system"
        exit 1
    fi
}

detect_compose() {
    # Check if docker compose command exists
    if docker compose >/dev/null 2>&1; then
        COMPOSE='docker compose'
    elif docker-compose >/dev/null 2>&1; then
        COMPOSE='docker-compose'
    else
        colorized_echo red "docker compose not found"
        exit 1
    fi
}

install_package () {
    if [ -z $PKG_MANAGER ]; then
        detect_and_update_package_manager
    fi

    PACKAGE=$1
    colorized_echo blue "Installing $PACKAGE"
    if [[ "$OS" == "Ubuntu"* ]] || [[ "$OS" == "Debian"* ]]; then
        $PKG_MANAGER -y install "$PACKAGE"
    elif [[ "$OS" == "CentOS"* ]] || [[ "$OS" == "AlmaLinux"* ]]; then
        $PKG_MANAGER install -y "$PACKAGE"
    elif [ "$OS" == "Fedora"* ]; then
        $PKG_MANAGER install -y "$PACKAGE"
    elif [ "$OS" == "Arch" ]; then
        $PKG_MANAGER -S --noconfirm "$PACKAGE"
    else
        colorized_echo red "Unsupported operating system"
        exit 1
    fi
}

install_docker() {
    # Install Docker and Docker Compose using the official installation script
    colorized_echo blue "Installing Docker"
    curl -fsSL https://get.docker.com | sh
    colorized_echo green "Docker installed successfully"
}

install_school_web_script() {
    FETCH_REPO="NotMmDG/School-Web"
    SCRIPT_URL="https://github.com/$FETCH_REPO/raw/master/install.sh"
    colorized_echo blue "Installing school-web script"
    curl -sSL $SCRIPT_URL | install -m 755 /dev/stdin /usr/local/bin/school-web
    colorized_echo green "school-web script installed successfully"
}

install_school_web() {
    # Fetch releases
    FILES_URL_PREFIX="https://raw.githubusercontent.com/NotMmDG/School-Web/master"

    mkdir -p "$DATA_DIR"
    mkdir -p "$APP_DIR"

    colorized_echo blue "Fetching compose file"
    curl -sL "$FILES_URL_PREFIX/docker-compose.yml" -o "$APP_DIR/docker-compose.yml"
    colorized_echo green "File saved in $APP_DIR/docker-compose.yml"
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
    colorized_echo blue "Fetching .env file"
    curl -sL "$FILES_URL_PREFIX/.env.example" -o "$APP_DIR/.env"
    sudo sed -i "s|MYSQL_DATABASE=.*|MYSQL_DATABASE=${MYSQL_DATABASE}|" "$APP_DIR/.env"
    sudo sed -i "s|MYSQL_USER=.*|MYSQL_USER=${MYSQL_USER}|" "$APP_DIR/.env"
    sudo sed -i "s|MYSQL_PASSWORD=.*|MYSQL_PASSWORD=${MYSQL_PASSWORD}|" "$APP_DIR/.env"
    sudo sed -i "s|MYSQL_ROOT_PASSWORD=.*|MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}|" "$APP_DIR/.env"
    sudo sed -i "s|PHPMYADMIN_USER=.*|PHPMYADMIN_USER=${PHPMYADMIN_USER}|" "$APP_DIR/.env"
    sudo sed -i "s|PHPMYADMIN_PASSWORD=.*|PHPMYADMIN_PASSWORD=${PHPMYADMIN_PASSWORD}|" "$APP_DIR/.env"
    sudo sed -i "s|PHPMYADMIN_PORT=.*|PHPMYADMIN_PORT=${PHPMYADMIN_PORT}|" "$APP_DIR/.env"
    sudo sed -i "s|WEB_PORT=.*|WEB_PORT=${WEB_PORT}|" "$APP_DIR/.env"
    sudo sed -i "s|SSL_CERT_PATH=.*|SSL_CERT_PATH=${SSL_CERT_PATH}|" "$APP_DIR/.env"
    sudo sed -i "s|SSL_KEY_PATH=.*|SSL_KEY_PATH=${SSL_KEY_PATH}|" "$APP_DIR/.env"
    sudo sed -i "s|USE_SSL=.*|USE_SSL=${USE_SSL}|" "$APP_DIR/.env"
    colorized_echo green "File saved in $APP_DIR/.env"
    colorized_echo green "school-web's files downloaded successfully"
}

uninstall_school_web_script() {
    if [ -f "/usr/local/bin/school-web" ]; then
        colorized_echo yellow "Removing school-web script"
        rm "/usr/local/bin/school-web"
    fi
}

uninstall_school_web() {
    if [ -d "$APP_DIR" ]; then
        colorized_echo yellow "Removing directory: $APP_DIR"
        rm -r "$APP_DIR"
    fi
}

uninstall_school_web_docker_images() {
    images=$(docker images | grep school-web | awk '{print $3}')

    if [ -n "$images" ]; then
        colorized_echo yellow "Removing Docker images of school-web"
        for image in $images; do
            if docker rmi "$image" >/dev/null 2>&1; then
                colorized_echo yellow "Image $image removed"
            fi
        done
    fi
}

uninstall_school_web_data_files() {
    if [ -d "$DATA_DIR" ]; then
        colorized_echo yellow "Removing directory: $DATA_DIR"
        rm -r "$DATA_DIR"
    fi
}

up_school_web() {
    $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" up -d --remove-orphans
}

down_school_web() {
    $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" down
}

show_school_web_logs() {
    $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" logs
}

follow_school_web_logs() {
    $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" logs -f
}

school_web_cli() {
    $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" exec -e CLI_PROG_NAME="school-web cli" school-web school-web-cli "$@"
}

update_school_web_script() {
    FETCH_REPO="NotMmDG/School-Web"
    SCRIPT_URL="https://github.com/$FETCH_REPO/raw/master/install.sh"
    colorized_echo blue "Updating school-web script"
    curl -sSL $SCRIPT_URL | install -m 755 /dev/stdin /usr/local/bin/school-web
    colorized_echo green "school-web script updated successfully"
}

update_school_web() {
    $COMPOSE -f $COMPOSE_FILE -p "$APP_NAME" pull
}

is_school_web_installed() {
    if [ -d $APP_DIR ]; then
        return 0
    else
        return 1
    fi
}

is_school_web_up() {
    if [ -z "$($COMPOSE -f $COMPOSE_FILE ps -q -a)" ]; then
        return 1
    else
        return 0
    fi
}

install_command() {
    check_running_as_root
    # Check if school-web is already installed
    if is_school_web_installed; then
        colorized_echo red "School-web is already installed at $APP_DIR"
        read -p "Do you want to override the previous installation? (y/n) "
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            colorized_echo red "Aborted installation"
            exit 1
        fi
    fi
    detect_os
    if ! command -v jq >/dev/null 2>&1; then
        install_package jq
    fi
    if ! command -v curl >/dev/null 2>&1; then
        install_package curl
    fi
    if ! command -v docker >/dev/null 2>&1; then
        install_docker
    fi
    detect_compose
    install_school_web_script
    install_school_web
    up_school_web
    follow_school_web_logs
}

uninstall_command() {
    check_running_as_root
    # Check if school-web is installed
    if ! is_school_web_installed; then
        colorized_echo red "School-web's not installed!"
        exit 1
    fi

    read -p "Do you really want to uninstall School-web? (y/n) "
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        colorized_echo red "Aborted"
        exit 1
    fi

    detect_compose
    if is_school_web_up; then
        down_school_web
    fi
    uninstall_school_web_script
    uninstall_school_web
    uninstall_school_web_docker_images

    read -p "Do you want to remove School-web's data files too ($DATA_DIR)? (y/n) "
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        colorized_echo green "School-web uninstalled successfully"
    else
        uninstall_school_web_data_files
        colorized_echo green "School-web uninstalled successfully"
    fi
}

up_command() {
    help() {
        colorized_echo red "Usage: school-web up [options]"
        echo ""
        echo "OPTIONS:"
        echo "  -h, --help        display this help message"
        echo "  -n, --no-logs     do not follow logs after starting"
    }

    local no_logs=false
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -n|--no-logs)
                no_logs=true
            ;;
            -h|--help)
                help
                exit 0
            ;;
            *)
                echo "Error: Invalid option: $1" >&2
                help
                exit 0
            ;;
        esac
        shift
    done

    # Check if school-web is installed
    if ! is_school_web_installed; then
        colorized_echo red "School-web's not installed!"
        exit 1
    fi

    detect_compose

    if is_school_web_up; then
        colorized_echo red "School-web's already up"
        exit 1
    fi

    up_school_web
    if [ "$no_logs" = false ]; then
        follow_school_web_logs
    fi
}

down_command() {
    # Check if school-web is installed
    if ! is_school_web_installed; then
        colorized_echo red "School-web's not installed!"
        exit 1
    fi

    detect_compose

    if ! is_school_web_up; then
        colorized_echo red "School-web's already down"
        exit 1
    fi

    down_school_web
}

restart_command() {
    help() {
        colorized_echo red "Usage: school-web restart [options]"
        echo
        echo "OPTIONS:"
        echo "  -h, --help        display this help message"
        echo "  -n, --no-logs     do not follow logs after starting"
    }

    local no_logs=false
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -n|--no-logs)
                no_logs=true
            ;;
            -h|--help)
                help
                exit 0
            ;;
            *)
                echo "Error: Invalid option: $1" >&2
                help
                exit 0
            ;;
        esac
        shift
    done

    # Check if school-web is installed
    if ! is_school_web_installed; then
        colorized_echo red "School-web's not installed!"
        exit 1
    fi

    detect_compose

    down_school_web
    up_school_web
    if [ "$no_logs" = false ]; then
        follow_school_web_logs
    fi
}

status_command() {
    # Check if school-web is installed
    if ! is_school_web_installed; then
        echo -n "Status: "
        colorized_echo red "Not Installed"
        exit 1
    fi

    detect_compose

    if ! is_school_web_up; then
        echo -n "Status: "
        colorized_echo blue "Down"
        exit 1
    fi

    echo -n "Status: "
    colorized_echo green "Up"

    json=$($COMPOSE -f $COMPOSE_FILE ps -a --format=json)
    services=$(echo "$json" | jq -r 'if type == "array" then .[] else . end | .Service')
    states=$(echo "$json" | jq -r 'if type == "array" then .[] else . end | .State')
    # Print out the service names and statuses
    for i in $(seq 0 $(expr $(echo $services | wc -w) - 1)); do
        service=$(echo $services | cut -d' ' -f $(expr $i + 1))
        state=$(echo $states | cut -d' ' -f $(expr $i + 1))
        echo -n "- $service: "
        if [ "$state" == "running" ]; then
            colorized_echo green $state
        else
            colorized_echo red $state
        fi
    done
}

logs_command() {
    help() {
        colorized_echo red "Usage: school-web logs [options]"
        echo ""
        echo "OPTIONS:"
        echo "  -h, --help        display this help message"
        echo "  -n, --no-follow   do not show follow logs"
    }

    local no_follow=false
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -n|--no-follow)
                no_follow=true
            ;;
            -h|--help)
                help
                exit 0
            ;;
            *)
                echo "Error: Invalid option: $1" >&2
                help
                exit 0
            ;;
        esac
        shift
    done

    # Check if school-web is installed
    if ! is_school_web_installed; then
        colorized_echo red "School-web's not installed!"
        exit 1
    fi

    detect_compose

    if ! is_school_web_up; then
        colorized_echo red "School-web is not up."
        exit 1
    fi

    if [ "$no_follow" = true ]; then
        show_school_web_logs
    else
        follow_school_web_logs
    fi
}

cli_command() {
    # Check if school-web is installed
    if ! is_school_web_installed; then
        colorized_echo red "School-web's not installed!"
        exit 1
    fi

    detect_compose

    if ! is_school_web_up; then
        colorized_echo red "School-web is not up."
        exit 1
    fi

    school_web_cli "$@"
}

update_command() {
    check_running_as_root
    # Check if school-web is installed
    if ! is_school_web_installed; then
        colorized_echo red "School-web's not installed!"
        exit 1
    fi

    detect_compose

    update_school_web_script
    colorized_echo blue "Pulling latest version"
    update_school_web

    colorized_echo blue "Restarting School-web's services"
    down_school_web
    up_school_web

    colorized_echo blue "School-web updated successfully"
}

usage() {
    colorized_echo red "Usage: school-web [command]"
    echo
    echo "Commands:"
    echo "  up              Start services"
    echo "  down            Stop services"
    echo "  restart         Restart services"
    echo "  status          Show status"
    echo "  logs            Show logs"
    echo "  cli             School-web CLI"
    echo "  install         Install School-web"
    echo "  update          Update latest version"
    echo "  uninstall       Uninstall School-web"
    echo "  install-script  Install School-web script"
    echo
}

case "$1" in
    up)
    shift; up_command "$@";;
    down)
    shift; down_command "$@";;
    restart)
    shift; restart_command "$@";;
    status)
    shift; status_command "$@";;
    logs)
    shift; logs_command "$@";;
    cli)
    shift; cli_command "$@";;
    install)
    shift; install_command "$@";;
    update)
    shift; update_command "$@";;
    uninstall)
    shift; uninstall_command "$@";;
    install-script)
    shift; install_school_web_script "$@";;
    *)
    usage;;
esac
