"""Text helper utilities."""
import re
from ai.classifier import get_highlighted_words

def normalize_text(text: str) -> str:
    """Normalize user input for consistent rule checks."""
    return " ".join(text.strip().lower().split())

def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    """Return True if any keyword is present in text."""
    return any(keyword in text for keyword in keywords)

def highlight_words(text: str, language: str, model_type: str) -> str:
    """
    Analyzes text and returns an HTML string with formal and informal words highlighted.
    """
    words_list = get_highlighted_words(text, language, model_type)
    formal_words = {
        "English": [],
        "Polish": []
    }
    
    informal_words = {
        "English": [],
        "Polish": []
    }
    print(words_list)
    for word in words_list:
        if float(word[1])>0:
            formal_words[language].append(str(word[0]))
        elif float(word[1])<0:
            informal_words[language].append(str(word[0]))

    print(formal_words)

    formal_style = "background-color: #d1ecf1; color: #0c5460; padding: 2px 6px; border-radius: 4px; font-weight: bold;"
    informal_style = "background-color: #f8d7da; color: #721c24; padding: 2px 6px; border-radius: 4px; font-weight: bold;"

    current_formal = formal_words.get(language, [])
    current_informal = informal_words.get(language, [])

    words = re.findall(r'\b\w+\b|[^\w\s]', text, re.UNICODE)
    highlighted_text = []

    for word in words:
        if re.match(r'[^\w\s]', word):
            highlighted_text.append(word)
            continue
            
        word_lower = word.lower()
        if word_lower in current_formal:
            highlighted_text.append(f'<span style="{formal_style}">{word}</span>')
        elif word_lower in current_informal:
            highlighted_text.append(f'<span style="{informal_style}">{word}</span>')
        else:
            highlighted_text.append(word)

    html_output = " ".join(highlighted_text)
    html_output = re.sub(r'\s+([.,!?])', r'\1', html_output)
    return html_output