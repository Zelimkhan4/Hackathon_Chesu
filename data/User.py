from sqlalchemy import Integer, String, ForeignKey, Column
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    hashed_password = Column(String)
    email = Column(String, index=True, unique=True)
    name = Column(String)
    surname = Column(String)
    passport_number = Column(String, unique=True, nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

