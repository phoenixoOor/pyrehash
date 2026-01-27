from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, HashTarget, Result, AttackSession
from ..config.default_settings import settings

class Storage:
    def __init__(self, db_url: str = settings.DATABASE_URL):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_target(self, hash_value: str, algorithm: str):
        with self.Session() as session:
            target = HashTarget(hash_value=hash_value, algorithm=algorithm)
            session.add(target)
            session.commit()
            return target.id

    def save_result(self, hash_value: str, password: str):
        with self.Session() as session:
            target = session.query(HashTarget).filter_by(hash_value=hash_value).first()
            if not target:
                target_id = self.add_target(hash_value, "unknown")
            else:
                target_id = target.id
            
            result = Result(target_id=target_id, password=password)
            session.add(result)
            session.commit()

    def create_session(self, mode: str, algorithm: str, target: str, params: str):
        with self.Session() as session:
            attack_session = AttackSession(
                mode=mode, algorithm=algorithm, target_hash=target, 
                parameters=params, status="running"
            )
            session.add(attack_session)
            session.commit()
            return attack_session.id

    def update_session(self, session_id: int, progress: int, status: str = "running"):
        with self.Session() as session:
            attack_session = session.query(AttackSession).get(session_id)
            if attack_session:
                attack_session.progress = progress
                attack_session.status = status
                session.commit()
