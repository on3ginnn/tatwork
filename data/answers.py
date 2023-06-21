import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, JSON # работа с БД
from sqlalchemy.orm import relationship, backref
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin # для возможности хранить в БД datatime


class Answers(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    modified_date = Column(DateTime, default=datetime.datetime.now)
    answers = Column(JSON, nullable=False)
    status = Column(String, nullable=False, default="Не пройдено") # Не пройдено, Зачтено
    score = Column(String, nullable=False)


# - В таблице "Answers" создается отношение Many-to-One между "Answers" и "User" таблицами
# с помощью Column(Integer, ForeignKey('users.id')) и relationship("Answers", backref="user"),
# а также отношение Many-to-One между "Answers" и "Task" таблицами с помощью Column(Integer, ForeignKey('tasks.id'))
# и relationship("Answers", backref="task").