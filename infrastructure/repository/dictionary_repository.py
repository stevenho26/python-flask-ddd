from infrastructure.repository.dictionary_models import DictionaryDTO
from infrastructure.database import db

class DictionaryRepository:
    def search_words(self, keyword, limit=20):
        """
        Search for words starting with keyword.
        """
        if not keyword:
            return []
        
        # Case insensitive search for words starting with keyword
        # Using db.session explicitly
        query = db.session.query(DictionaryDTO).filter(
            DictionaryDTO.word.ilike(f"{keyword}%")
        ).limit(limit)
        
        return query.all()

    def get_definition(self, word):
        """
        Get definition of a specific word (exact match).
        """
        return db.session.query(DictionaryDTO).filter(
            DictionaryDTO.word == word
        ).first()

    def fuzzy_search(self, keyword, limit=20):
       """
       Search containing keyword
       """
       return db.session.query(DictionaryDTO).filter(
            DictionaryDTO.word.ilike(f"%{keyword}%")
        ).limit(limit).all()
