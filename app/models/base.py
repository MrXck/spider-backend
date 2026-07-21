from sqlalchemy import event, Column, BigInteger
from sqlalchemy.orm import declarative_base
from app.core.snowflake import snowflake


class Base:
    id = Column(BigInteger, primary_key=True)


Base = declarative_base(cls=Base)


@event.listens_for(Base, "before_insert", propagate=True)
def base_before_insert(mapper, connection, target):
    if target.id is None:
        target.id = snowflake.next_id()
