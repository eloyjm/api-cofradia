from config.app import config_app
from config.logging.logger import logger
import uvicorn

if __name__ == "__main__":
    port = config_app.port

    logger.info(f"Starting CofradIA API on PORT {port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level=config_app.log_level.lower(),
        log_config=config_app.logger_config_path,
    )
