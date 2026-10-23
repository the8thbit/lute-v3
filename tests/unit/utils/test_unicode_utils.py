"""Unicode helper tests."""

from lute.utils.unicode_utils import canonical_key


def test_canonical_key_for_composed_latin_character():
    "Composed and decomposed spellings share one key."
    assert canonical_key("é") == canonical_key("e\u0301")


def test_canonical_key_for_bengali_composition_exclusion():
    "Bengali composition-exclusion spellings share one key."
    separate_codepoints = "ছায়া"
    single_codepoint = "ছায়া"

    assert canonical_key(separate_codepoints) == canonical_key(single_codepoint)


def test_canonical_key_handles_mixed_normalization():
    "Each character is normalized even when a token mixes forms."
    assert canonical_key("ée\u0301") == canonical_key("éé")


def test_canonical_key_is_bounded_for_repeated_composition_exclusions():
    "Long tokens produce one key rather than a combinatorial variant set."
    token = "ছায়া" * 1000

    key = canonical_key(token)

    assert key == canonical_key(key)
    assert len(key) <= 2 * len(token)
