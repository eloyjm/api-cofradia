from decouple import config


class DATABASE:
    def __init__(self):
        self.postgres_db = config("POSTGRES_DATABASE")
        self.postgres_host = config("PG_HOST")
        self.postgres_port = int(config("PG_PORT"))
        self.postgres_user = config("POSTGRES_USER")
        self.postgres_password = config("POSTGRES_PASSWORD")

    def get_connection_uri(self):
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


database = DATABASE()
