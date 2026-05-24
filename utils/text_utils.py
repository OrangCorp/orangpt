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
    Analyzes text and returns an HTML string with formal and informal words 
    highlighted using a precise gradient based on feature importance weights.
    Neutral words are left completely unstyled.
    """
    words_list = get_highlighted_words(text, language, model_type)
    if not words_list:
        return text.replace("\n", "<br>")

    # Calculate absolute max score to normalize gradients relatively
    max_score = max(abs(float(val)) for _, val in words_list) if words_list else 1.0
    if max_score == 0:
        max_score = 1.0

    # Build local scoring lookup dictionary
    word_scores = {str(word).lower(): float(val) for word, val in words_list}

    # Split using capturing group to preserve all spacing, punctuation, and newlines exactly
    tokens = re.split(r'(\s+|\b\w+\b)', text)
    highlighted_text = []

    for token in tokens:
        if not token:
            continue
        
        # Process alphanumeric words
        if re.match(r'^\w+$', token):
            token_lower = token.lower()
            if token_lower in word_scores:
                score = word_scores[token_lower]
                
                # Filter out true neutrals or microscopic values
                if abs(score) > 0.001:
                    # Scale opacity from 0.30 (subtle) up to 0.90 (high intensity)
                    alpha = 0.30 + 0.60 * (abs(score) / max_score)
                    
                    if score > 0:
                        # Formal: Teal/Cyan gradient highlights with white text
                        style = f"background-color: rgba(0, 180, 216, {alpha:.2f}); color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: bold; display: inline;"
                        highlighted_text.append(f'<span style="{style}">{token}</span>')
                        continue
                    elif score < 0:
                        # Informal: Vibrant Red/Coral gradient highlights with white text
                        style = f"background-color: rgba(239, 35, 60, {alpha:.2f}); color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: bold; display: inline;"
                        highlighted_text.append(f'<span style="{style}">{token}</span>')
                        continue
                        
        # Keep punctuation, spacing, newlines, and neutral words unmodified
        escaped_token = token.replace("\n", "<br>")
        highlighted_text.append(escaped_token)

    return "".join(highlighted_text)