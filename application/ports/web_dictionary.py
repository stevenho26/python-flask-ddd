from flask import render_template, request
from infrastructure.repository.dictionary_repository import DictionaryRepository
from infrastructure.repository.models import BookDTO # Keep existing imports clean if needed

def init_web_dictionary(app):
    
    @app.route('/dictionary', methods=['GET'])
    def dictionary_page():
        keyword = request.args.get('q', '')
        results = []
        definition = None
        repo = DictionaryRepository()

        if keyword:
            # 1. Try to get definition for the exact word
            # Often user clicks a word in the list, so exact match is priority for definition display
            exact_match_entry = repo.get_definition(keyword)
            if exact_match_entry:
                definition = exact_match_entry.definition
            
            # 2. Get sidebar list (starts with keyword)
            results = repo.search_words(keyword)
            
            # If search returns nothing, try fuzzy search
            if not results:
                 results = repo.fuzzy_search(keyword)
            
            # If definition is still None but we have results, 
            # maybe user typed partial word. 
            # We don't auto-select definition to avoid confusion, unless it's the only result.
            if not definition and len(results) == 1:
                definition = results[0].definition
                # Also update keyword to match the found word for UI consistency
                keyword = results[0].word

        return render_template('dictionary.html', keyword=keyword, results=results, definition=definition)
