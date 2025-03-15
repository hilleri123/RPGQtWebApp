from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy_utils import ColorType
from colour import Color
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


engine = create_engine(f'sqlite:///{os.getenv("DB_URL")}')