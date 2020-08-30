# Scrappybara

> Python library for Natural Language Processing.

## Overview

Scrappybara provides tools to extract structured data from unstructured text. This data is useful for researchers and developers who want to build NLP applications.

Scappybara focuses on a single language: English. You won't have to bother with training models or downloading resources. Everything works right off the bat. This commitment also allows more development efforts tackling the meaning of language.

See the [Quick start](quick-start.md) guide to get started.

### Example

Given the sentence:

```text
"In the last scene, Tamara drops her skepticism toward Sasha and allows him to fall asleep with his head resting on her lap."
```

Scrappybara would extract the following semantic tuples:
- Predicate **NOUN**+**VERB**+**NOUN**: `(tamara, drop, skepticism)`
- Predicate **NOUN**+**VERB**+**NOUN**+**VERB**: `(tamara, allow, he, fall asleep)`
- Copula predicates **NOUN**+**VERB**+**NOUN**: `(scene, be, last)`, `(skepticism, be, dropped)`
- Intransitive predicates **NOUN**+**VERB**: `(head, rest)`
 
## Features

- **Extraction of semantic tuples from unstructured text**:
    - Creates multiple tuples when finding conjunctions AND/OR
    - Detects negative forms: *no cat can swim* => `(cat, NOT swim)`
    - Converts passive form to active form, and vice-versa
    - Chunks nouns: *I love my lemon squeezer* => `(i, love, lemon squeezer)`
    - Leverages hardware for high speed: use of CPU multithreading and GPU
    
### MIT license

Free to use for any commercial or non-commercial purposes.
