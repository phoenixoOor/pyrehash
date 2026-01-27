from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class HashTarget(Base):
    __tablename__ = "hash_targets"
    
    id = Column(Integer, primary_key=True)
    hash_value = Column(String, unique=True, nullable=False)
    algorithm = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    results = relationship("Result", back_populates="target")

class AttackSession(Base):
    __tablename__ = "attack_sessions"
    
    id = Column(Integer, primary_key=True)
    mode = Column(String)  # dict, brute, etc.
    algorithm = Column(String)
    target_hash = Column(String)
    parameters = Column(String)  # JSON serialized params
    status = Column(String)  # running, paused, completed, failed
    progress = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Result(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("hash_targets.id"))
    password = Column(String)
    found_at = Column(DateTime, default=datetime.utcnow)
    
    target = relationship("HashTarget", back_populates="results")
