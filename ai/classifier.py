"""Formality classification logic."""

from utils.text_utils import contains_any, normalize_text

FORMAL_HINTS = ("please", "thank you", "regards", "sincerely")
INFORMAL_HINTS = ("hey", "lol", "gonna", "wanna", "bro", "omg")


def classify_tone(text: str) -> str:
    """Classify text as formal, informal, or unknown.

    Returns ``unknown`` when no hints are found or when formal/informal hints are tied.
    """
    normalized = normalize_text(text)
    if not normalized:
        return "unknown"

    formal_score = int(contains_any(normalized, FORMAL_HINTS))
    informal_score = int(contains_any(normalized, INFORMAL_HINTS))
    formal_score += int(normalized.endswith("."))
    informal_score += int("!" in normalized)

    if formal_score == informal_score:
        return "unknown"
    return "formal" if formal_score > informal_score else "informal"
