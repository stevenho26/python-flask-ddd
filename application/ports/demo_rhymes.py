from flask import render_template, request, flash, redirect, url_for

def init_rhyme_demo(app):
    @app.route('/demo-rhymes', methods=['GET', 'POST'])
    def demo_rhymes():
        result = None
        word = ''
        
        if request.method == 'POST':
            word = request.form.get('word', '').strip()
            
            # Simple validation: single word only
            if not word:
                pass # empty submission
            elif ' ' in word:
                result = {'error': 'Vui lòng chỉ nhập 1 từ đơn.'}
            else:
                word_lower = word.lower()
                onset, rhyme = extract_rhyme(word_lower)
                result = {
                    'original': word,
                    'onset': onset,
                    'rhyme': rhyme
                }

        return render_template('demo_rhymes.html', result=result, word=word)

def extract_rhyme(word):
    """
    Extracts onset and rhyme from a vietnamese word based on simple rules.
    """
    # Sorted by length descending to match longest possible onset first
    onsets = [
        "ngh", "ng", "gh", "ch", "tr", "th", "ph", "kh", "nh", "gi", "qu", 
        "th", "tr", "ch", "ph", "nh", "kh", "gi", "qu", "gh", "ng", 
        "b", "c", "d", "đ", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "x"
    ]
    
    # Sort onsets by length desc to ensure we match 'ngh' before 'ng' or 'n'
    onsets.sort(key=len, reverse=True)
    
    current_onset = ""
    current_rhyme = word
    
    for onset in onsets:
        if word.startswith(onset):
            current_onset = onset
            current_rhyme = word[len(onset):]
            break
            
    return current_onset, current_rhyme
