"""Analyse sentences, extract acronyms and their expanded form if e.g. "...Test Driven Development (TDD)..." is seen"""
import re
from collections import Counter

# Goal:
# Extract acronym and expanded form if both are present in a sentence
# Count these examples, we can extract the most-frequent as being good examples

# Problems:
# A mix of lowercase letters could be useful, currently we ignore it so e.g.
# "Royal Bank of Scotland (RBS)"
# will extract ("Bank of Scotland", "RBS") even though 'of' should be skipped
# for an acronym

# License: MIT (http://opensource.org/licenses/MIT)


def detect_acronym(sentence):
    """Look at tokens in a sentence to try to find acryonym+definition like 'Test Driven Development (TDD)'"""
    acronym_strings = []
    tokens = sentence.split()  # split on whitespace

    for idx, token in enumerate(tokens):
        # look for token that uses brackets e.g. (TDD) or (UK)
        result = re.findall("\((.*)\)", token)
        for res in result:
            # check that the bracketed item is uppercase so we'd ignore e.g.
            # (part-time project)
            if res.isupper():
                nbr_possible_tokens = len(res)
                # filter out sentences that start with a bracketed expression
                # ignore -> "(UK) spent some time visiting here"
                # keep   -> "...learned Test Driven Development (TDD) whilst..."
                if idx >= nbr_possible_tokens:
                    # build a tuple of (<acronym without brackets>, <string of preceeding tokens>)
                    # e.g. ('TDD', 'Test Driven Development')
                    details = (res, tuple(tokens[idx - nbr_possible_tokens:idx]))
                    acronym_strings.append(details)
    return acronym_strings


def count_acronyms_in_sentences(sentences):
    """Iterate over sentences to extract a Counter of acronym frequencies"""
    # Note that you can pass in a generator (using yield) if you're iterating
    # over a complex items (e.g. MongoDB record items)
    c = Counter()
    for sentence in sentences:
        c.update(detect_acronym(sentence))
    return c


if __name__ == "__main__":
    sentences = ["In here we talk about Test Driven Development (TDD) and other stuff",
                 "Mission Objectives (MI) are important, so is Test Driven Development (TDD)",
                 "The United Kingdom (UK) is a lovely place to live, so are other places (e.g. USA)"]
    print(count_acronyms_in_sentences(sentences))
    # Expected output:
    # Counter({('TDD', ('Test', 'Driven', 'Development')): 2, ('MI', ('Mission', 'Objectives')): 1, ('UK', ('United', 'Kingdom')): 1})
