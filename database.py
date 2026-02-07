from sqlalchemy import create_engine;
from sqlalchemy.orm import sessionmaker;
from dotenv import load_dotenv;
import os;

load_dotenv()

DB_USER = os.getenv("DB_USER") 
DB_PASSWORD = os.getenv("DB_PASSWORD") 
DB_HOST = os.getenv("DB_HOST") 
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")


DB_url=f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine=create_engine(DB_url)
SessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)

