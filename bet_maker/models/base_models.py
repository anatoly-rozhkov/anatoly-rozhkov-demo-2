import uuid

from sqlalchemy import Column, MetaData, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())


class UpdatedAtModel(Base):
    __abstract__ = True

    updated_at = Column(type_=TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
