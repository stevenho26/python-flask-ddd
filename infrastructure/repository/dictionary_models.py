from sqlalchemy import Column, Integer, String, Text
from infrastructure.database import db

class DictionaryDTO(db.Model):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(255), nullable=False, index=True)
    definition = Column(Text, nullable=False)

    def __repr__(self):
        return f"<DictionaryDTO(word={self.word})>"
