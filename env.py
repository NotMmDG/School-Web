import os
from dotenv import load_dotenv
from alembic.config import Config

class Settings:
    def __init__(self):
        # Define the path to the .env file
        env_path = os.path.join(os.path.dirname(__file__), 'app', '.env')

        # Load environment variables from the .env file
        load_dotenv(dotenv_path=env_path)

        # Determine the environment and select the appropriate database URL
        environment = os.getenv('ENVIRONMENT', 'development')
        if environment == 'production':
            self.DATABASE_URL = os.getenv('DATABASE_URL')
        else:  # Default to using SQLite for development and testing
            self.DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
        self.MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
        self.MYSQL_USER = os.getenv('MYSQL_USER')
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        self.MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
        self.PHPMYADMIN_USER = os.getenv('PHPMYADMIN_USER')
        self.PHPMYADMIN_PASSWORD = os.getenv('PHPMYADMIN_PASSWORD')
        self.PHPMYADMIN_PORT = os.getenv('PHPMYADMIN_PORT')
        self.WEB_PORT = os.getenv('WEB_PORT')
        self.SSL_CERT_PATH = os.getenv('SSL_CERT_PATH')
        self.SSL_KEY_PATH = os.getenv('SSL_KEY_PATH')
        self.USE_SSL = os.getenv('USE_SSL', 'false').lower() in ('true', '1', 't')

    def update_alembic_config(self):
        """Updates the Alembic configuration with the correct database URL."""
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), 'alembic.ini'))
        alembic_cfg.set_main_option('sqlalchemy.url', self.DATABASE_URL)
        return alembic_cfg

# Function to get a settings object
def get_settings() -> Settings:
    return Settings()
