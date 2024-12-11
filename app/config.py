import os
import logging
from pydantic import Field
from pydantic_settings import BaseSettings

base_dir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):

    gpt_api_key: str = Field("123", env='GPT_API_KEY')

    client_id: str = Field("123", env='CLIENT_ID')
    client_secret: str = Field("123", env='CLIENT_SECRET')
    tenant_id: str = Field("123", env='TENANT_ID')

    user_email: str = Field("xyz", env='USER_EMAIL')

    # app_version: str = Field("1.0.0", env='APP_VERSION')


    class Config:
        env_file = os.path.join(base_dir, "../.env")


def get_settings():
    return Settings()


def setup_logging():
    ch = logging.FileHandler("./mailboxmaverics.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(ch)
    return logger


