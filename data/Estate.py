from sqlalchemy import Integer, String, ForeignKey, Column
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Estate(SqlAlchemyBase):
    __tablename__ = 'estate'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, index=True)
    address = Column(String)
    about = Column(String)

