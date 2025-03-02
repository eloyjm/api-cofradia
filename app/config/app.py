from decouple import config
import os

__version__ = "0.1.0"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
        self.dds_url = config(
            "DDS_URL",
            "https://www.diariodesevilla.es/contenidos/programa-semana-santa-sevilla",  # noqa: E501
        )
        self.marchs_url = config(
            "MARCHS_URL",
            "https://glissandoo.com/blog/posts/las-marchas-de-procesion-mas-famosas-de-youtube",  # noqa: E501
        )
        self.hermandades_data_path = config(
            "HERMANDADES_DATA_PATH", "app/config/hermandades_data.json"
        )

        self.suit_path = config("SUIT_PATH", "static/images/suit")

        self.shield_path = config("SHIELD_PATH", "static/images/shield")

        self.base_path = BASE_DIR

        self.access_token_expiration = int(
            config("ACCESS_TOKEN_EXPIRATION", "30")
        )

        self.secret_key = config("SECRET_KEY")
        self.algorithm = config("ALGORITHM")


config_app = APP()
