import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint  # работа с БД
from sqlalchemy.orm import relationship, backref
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin # для возможности хранить в БД datatime


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    title = Column(String, nullable=False)
    task_type = Column(String, nullable=True, default='ТЕСТ') # Кросс-ворд, соотнести слова, хронология, тест

    question = relationship("Questions", lazy="joined", backref="task", primaryjoin="Task.id==Questions.task_id")
    answer = relationship("Answers", lazy="joined", backref="task", primaryjoin="Task.id==Answers.task_id")
    # topic = relationship("Topic", lazy="joined")

# - В таблице "Task" создается отношение Many-to-One между "Task" и "Topic" таблицами с помощью `Column(Integer, ForeignKey('topics.id'))` и `relationship("Task", backref="topic")`.