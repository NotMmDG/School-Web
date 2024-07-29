import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", default="sqlite:///./test.db")
        self.database_name = os.getenv("DATABASE_NAME", default="school")
        self.database_user = os.getenv("DATABASE_USER", default="school_user")
        self.database_password = os.getenv("DATABASE_PASSWORD", default="school_password")
        self.database_host = os.getenv("DATABASE_HOST", default="localhost")
        self.database_port = os.getenv("DATABASE_PORT", default="3306")
        self.mysql_root_password = os.getenv("MYSQL_ROOT_PASSWORD", default="root_password")
        self.phpmyadmin_user = os.getenv("PHPMYADMIN_USER", default="admin")
        self.phpmyadmin_password = os.getenv("PHPMYADMIN_PASSWORD", default="admin_password")
        self.phpmyadmin_port = os.getenv("PHPMYADMIN_PORT", default="8080")
        self.web_port = os.getenv("WEB_PORT", default="8000")
        self.use_ssl = os.getenv("USE_SSL", default=False)
        self.ssl_cert_path = os.getenv("SSL_CERT_PATH", default=None)
        self.ssl_key_path = os.getenv("SSL_KEY_PATH", default=None)

def get_settings():
    return Settings()

settings = get_settings()
