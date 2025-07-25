import os
from pydantic_settings import BaseSettings
from typing import ClassVar
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

class Settings(BaseSettings):
    APP_NAME: str = ""
    API_PREFIX: str = ""
    
    
    MYSQL_HOST : str= ''
    MYSQL_USER : str=  ''
    MYSQL_PASSWORD : str=  ''
    MYSQL_DB : str= ''
    MYSQL_PORT : int=  
