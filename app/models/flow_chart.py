import datetime

from sqlalchemy import Column, String, Text, BigInteger, DateTime

from app.models.base import Base


class FlowChart(Base):
    __tablename__ = "flow_chart"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    user_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
    flow_json = Column(Text(), nullable=False)
    create_time = Column(DateTime(), default=datetime.datetime.now(), nullable=False)
    update_time = Column(DateTime(), nullable=True)
