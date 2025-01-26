from decouple import config

__version__ = "0.1.0"


class APP:
    def __init__(self):
        self.port = int(config("API_PORT", "8000"))
        self.openapi_path = config("OPENAPI_PATH", "app/openapi/openapi.json")
        self.log_level = config("LOG_LEVEL", "INFO")
        self.logger_env = config("LOGGER_ENV", "development")
        self.version = __version__
        self.environment = config("ENVIRONMENT", "development")
        self.logger_config_path = config(
            "LOGGER_CONFIG_PATH", "app/config/logging/logging.yaml"
        )


config_app = APP()
