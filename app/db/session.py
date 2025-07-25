from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import Settings
from app.core.database import DATABASE_URL

#DATABASE_URL = f"mysql+pymysql://{Settings.MYSQL_USER}:{Settings.MYSQL_PASSWORD}@{Settings.MYSQL_HOST}:{Settings.MYSQL_PORT}/{Settings.MYSQL_DB}"
#DATABASE_URL = "mysql+pymysql://edpadmin:edpadmin@edpnew.c7uqx6xqd0nl.us-east-1.rds.amazonaws.com:4897/insightrag"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)