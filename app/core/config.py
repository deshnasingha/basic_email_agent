import os
from pydantic_settings import BaseSettings
from typing import ClassVar
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Backend"
    API_PREFIX: str = "/api"
    
    
    MYSQL_HOST : str= '127.0.0.1'
    MYSQL_USER : str=  'dbuser'
    MYSQL_PASSWORD : str=  'user123'
    MYSQL_DB : str= 'workflowdb'
    MYSQL_PORT : int=  3306