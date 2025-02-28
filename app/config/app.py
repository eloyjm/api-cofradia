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


config_app = APP()
