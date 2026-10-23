"""
Find terms in contest string using ahocorapy.
"""

from ahocorapy.keywordtree import KeywordTree

from lute.utils.unicode_utils import canonical_key


class MultiwordTermIndexer:
    """
    Find terms in strings using ahocorapy.
    """

    zws = "\u200B"  # zero-width space

    def __init__(self):
        self.kwtree = KeywordTree(case_insensitive=True)
        self.original_terms = {}
        self.finalized = False

    def add(self, t):
        "Add zws-enclosed term to tree."
        canonical = canonical_key(t)
        self.original_terms.setdefault(canonical, []).append(t)
        add_t = f"{self.zws}{canonical}{self.zws}"
        self.kwtree.add(add_t)

    def search_all(self, lc_tokens):
        "Find all terms and starting token index."
        if not self.finalized:
            self.kwtree.finalize()
            self.finalized = True

        zws = self.zws
        canonical_tokens = [canonical_key(t) for t in lc_tokens]
        content = zws + zws.join(canonical_tokens) + zws
        zwsindexes = [i for i, char in enumerate(content) if char == zws]
        results = self.kwtree.search_all(content)

        for result in results:
            # print(f"{result}\n", flush=True)
            canonical = result[0].strip(zws)
            charpos = result[1]
            index = zwsindexes.index(charpos)
            token_count = canonical.count(zws) + 1
            raw_match = zws.join(lc_tokens[index : index + token_count])
            originals = self.original_terms[canonical]
            exact = [t for t in originals if t == raw_match]
            yield ((exact or originals)[0], index)
