from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    String,
    create_engine,
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import SQLITE_DB
from memory.schemas import Memory

DATABASE_URL = f"sqlite:///{SQLITE_DB}"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


class MemoryRecord(Base):

    __tablename__ = "memories"

    id = Column(String, primary_key=True)

    category = Column(String)

    memory_key = Column(String)

    value = Column(String)

    source = Column(String)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)


Base.metadata.create_all(engine)


class KVStore:

    def __init__(self):

        self.session = SessionLocal()

    def save(self, memory: Memory):
        existing = (
            self.session.query(MemoryRecord)
            .filter((MemoryRecord.id == memory.id) | (MemoryRecord.memory_key == memory.key if memory.key else False))
            .first()
        )

        if existing:

            existing.value = memory.value

            existing.updated_at = datetime.utcnow()

        else:

            record = MemoryRecord(

                id=memory.id,

                category=memory.category,

                memory_key=memory.key,

                value=memory.value,

                source=memory.source,

                created_at=memory.created_at,

                updated_at=memory.updated_at,

            )

            self.session.add(record)

        self.session.commit()

    def get(self, key: str) -> Optional[Memory]:

        record = (

            self.session.query(MemoryRecord)

            .filter(MemoryRecord.memory_key == key)

            .first()

        )

        if not record:

            return None

        return Memory(

            id=record.id,

            category=record.category,

            key=record.memory_key,

            value=record.value,

            source=record.source,

            created_at=record.created_at,

            updated_at=record.updated_at,

        )

    def update(self, key: str, value: str):

        record = (

            self.session.query(MemoryRecord)

            .filter(MemoryRecord.memory_key == key)

            .first()

        )

        if not record:

            return

        record.value = value

        record.updated_at = datetime.utcnow()

        self.session.commit()

    def delete(self, key: str):

        record = (

            self.session.query(MemoryRecord)

            .filter(MemoryRecord.memory_key == key)

            .first()

        )

        if record:

            self.session.delete(record)

            self.session.commit()

    def list_all(self):

        records = self.session.query(MemoryRecord).all()

        return [

            Memory(

                id=r.id,

                category=r.category,

                key=r.memory_key,

                value=r.value,

                source=r.source,

                created_at=r.created_at,

                updated_at=r.updated_at,

            )

            for r in records

        ]


kv_store = KVStore()