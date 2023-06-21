import datetime
import sqlalchemy # работа с БД из pyton
from sqlalchemy_serializer import SerializerMixin # для возможности хранить в БД datatime

from .db_session import SqlAlchemyBase # подключение к БД
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint  # работа с БД
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash # хэширование пароля
from flask_login import UserMixin # создание модели пользователя, для взаимодействия с БД


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False, default='Студент') # для удобства идентификации пользователей
    hashed_password = Column(String, nullable=False)
    avatar = Column(String, nullable=True, default=None)

    student = relationship("Student", lazy="joined", backref="user")
    teacher = relationship("Teacher", lazy="joined", backref="user")
    topic = relationship("Topic", lazy="joined", backref="author", uselist=True, primaryjoin="User.id==Topic.author_id")
    answer = relationship("Answers", lazy="joined", backref="user", uselist=True, primaryjoin="User.id==Answers.user_id")
    # - В таблице "User" создается отношение One-to-One между "Student" и "Teacher" таблицами
    # с помощью `relationship("Student", backref="user")` и `relationship("Teacher", backref="user")`.

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

