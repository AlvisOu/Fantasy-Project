from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class PlayerData(Base):
    __tablename__ = 'player_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    player_name = Column(String(100), nullable=False)
    position = Column(String(50), nullable=False)
    team = Column(String(50), nullable=False)
    projected_score = Column(Float, nullable=False)
    boom_probability = Column(Float, nullable=False)
    bust_probability = Column(Float, nullable=False)
    actual_score = Column(Float, nullable=False)
    injury_status = Column(String(50), nullable=False)
    lineup_status = Column(String(50), nullable=False)
    fantasy_team = Column(String(50), nullable=False)

DATABASE_URL = "mysql+mysqlconnector://user:password@localhost:3307/fantasy_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
