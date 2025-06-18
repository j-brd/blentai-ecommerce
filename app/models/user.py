from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    """
    Modèle User : représente un utilisateur dans la base de données.
    """

    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, nullable=False)
