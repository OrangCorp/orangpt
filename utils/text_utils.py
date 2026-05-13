"""Text helper utilities."""


def normalize_text(text: str) -> str:
    """Normalize user input for consistent rule checks."""
    return " ".join(text.strip().lower().split())


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    """Return True if any keyword is present in text."""
    return any(keyword in text for keyword in keywords)
