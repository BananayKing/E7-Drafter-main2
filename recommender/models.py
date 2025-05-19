from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    character_selections = relationship(
        "UserCharacterSelection",
        back_populates="user",
        cascade="all, delete-orphan"
    )
class UserCharacterSelection(Base):
    __tablename__ = "user_character_selections"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    character_id = Column(String, nullable=False)

    user = relationship("User", back_populates="character_selections")

    