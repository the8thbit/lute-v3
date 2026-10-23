"""Unicode helpers."""

import unicodedata


def canonical_key(text):
    """Return the canonical comparison key for text."""
    return unicodedata.normalize("NFC", text)
