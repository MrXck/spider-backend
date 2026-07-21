from sqlalchemy import Column, String, Text, BigInteger, DateTime

from app.models.base import Base


class User(Base):
    __tablename__ = "flow_chart"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=False)
    flow_json = Column(Text(), nullable=False)
    create_time = Column(DateTime(), nullable=False)
    update_time = Column(DateTime(), nullable=True)
