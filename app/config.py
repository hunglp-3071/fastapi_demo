from pydantic import BaseSettings
import logging


class Settings(BaseSettings):
    DEFAULT_VAR = ''
    SECRET_KEY = str
    ALGORITHM = str
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    class Config:
        env_file = ".env"


def setup_logger(name) -> logging.Logger:
    FORMAT = "[%(name)s %(module)s:%(lineno)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    logging.basicConfig(
        format=FORMAT, datefmt=TIME_FORMAT, level=logging.DEBUG, filename="./app/python.log"
    )

    logger = logging.getLogger(name)
    return logger