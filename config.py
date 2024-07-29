from decouple import config
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    def __init__(self):
        self.database_url = config("DATABASE_URL", default="sqlite:///./test.db")
        self.database_name = config("DATABASE_NAME", default="school")
        self.database_user = config("DATABASE_USER", default="school_user")
        self.database_password = config("DATABASE_PASSWORD", default="school_password")
        self.database_host = config("DATABASE_HOST", default="localhost")
        self.database_port = config("DATABASE_PORT", default="3306")
        self.mysql_root_password = config("MYSQL_ROOT_PASSWORD", default="root_password")
        self.phpmyadmin_user = config("PHPMYADMIN_USER", default="admin")
        self.phpmyadmin_password = config("PHPMYADMIN_PASSWORD", default="admin_password")
        self.phpmyadmin_port = config("PHPMYADMIN_PORT", default="8080")
        self.web_port = config("WEB_PORT", default="8000")
        self.use_ssl = config("USE_SSL", default=False, cast=bool)
        self.ssl_cert_path = config("SSL_CERT_PATH", default=None)
        self.ssl_key_path = config("SSL_KEY_PATH", default=None)

def get_settings():
    return Settings()

settings = get_settings()
