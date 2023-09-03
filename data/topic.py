import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey # работа с БД
from sqlalchemy.orm import relationship, backref
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin # для возможности хранить в БД datatime

from sqlalchemy import ForeignKeyConstraint


class Topic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    created_date = Column(String, default=datetime.datetime.now().strftime('%H:%M %d-%m-%Y'))
    author = Column(String, nullable=False) # автор
    topic_lang = Column(String, nullable=False) # список РУС, ТАТ, КИНО
    picture = Column(String, nullable=True, default=None)

    tasks = relationship("Task", backref="topic", lazy="joined", uselist=True, primaryjoin="Topic.id==Task.topic_id")


