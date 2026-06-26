from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@localhost:5432/{db_name}")
Base = declarative_base()
Session = sessionmaker(bind=engine)