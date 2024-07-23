# School Web Project

Welcome to the School Web Project! This project is a web application designed for school management, including functionalities for students, courses, professors, and more.

## Features

- User authentication and authorization
- Course management
- Student management
- Professor management
- OAuth2 with JWT for security
- Responsive frontend with React and Bootstrap
- API documentation with FastAPI

## Installation

### Prerequisites

- Docker
- Docker Compose
- Git
- Certbot (if using SSL)

### Installation Command

Run the following command to install and set up the project:

```bash
curl -o install.sh https://raw.githubusercontent.com/NotMmDG/School-Web/master/install.sh && chmod +x install.sh && ./install.sh
```
The script will prompt you for various configuration settings, including database credentials, ports, and SSL options. Follow the instructions to complete the setup.

Accessing the Application
Once the setup is complete, you can access the application and phpMyAdmin at the URLs provided in the final setup message. The ports will be the ones you specified during the installation process.

Usage
Authentication
Use the /token endpoint to obtain a JWT token. Include the token in the Authorization header for subsequent API requests.

API Documentation
Access the API documentation at http://<your-domain-or-ip>:<web_port>/docs for an interactive interface to explore the API endpoints.

Configuration
Environment Variables
The .env file in /opt/school-web contains environment variables for the application. You can modify the settings as needed.

Docker Compose
The docker-compose.yml file in /opt/school-web defines the Docker services. Modify this file if you need to change service configurations.

Customization
Changing Environment Variables
Navigate to /opt/school-web/.
Open the .env file in a text editor.
Modify the environment variables as needed.
Save the changes.

Updating Docker Compose Configuration
Navigate to /opt/school-web/.
Open the docker-compose.yml file in a text editor.
Modify the service configurations as needed.
Save the changes.

Restarting the Services
After making changes to the .env or docker-compose.yml files, restart the Docker services to apply the changes:
```bash
cd /opt/school-web/
sudo docker-compose down
sudo docker-compose up --build -d
```

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

License
This project is licensed under the MIT License.
