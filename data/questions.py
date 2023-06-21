import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, JSON # работа с БД
from sqlalchemy.orm import relationship, backref
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin # для возможности хранить в БД datatime


class Questions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    question = Column(JSON, nullable=False) # задание состоит из нескольких вопросов, поэтому JSON


# - В таблице "Questions" создается отношение Many-to-One между "Questions" и "Task" таблицами
# с помощью `Column(Integer, ForeignKey('tasks.id'))` и `relationship("Questions", backref="task")` в Topic.