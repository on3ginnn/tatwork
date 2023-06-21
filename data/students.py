import datetime
from sqlalchemy_serializer import SerializerMixin # для возможности хранить в БД datatime
from .db_session import SqlAlchemyBase # подключение к БД
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey # работа с БД
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash # хэширование пароля
from flask_login import UserMixin # создание модели пользователя, для взаимодействия с БД


class Student(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group = Column(String, nullable=False, default='ИС-221') # список ИС-222б, ИС-221, ПРЕПОД

    # user = relationship('User') # это не нужно, если в User уже есть student = relationship("Student", backref="user"),
    # они аналогичны

