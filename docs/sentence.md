# Sentence

> A Document contains Sentences.

## Example

```python
import scrappybara as sb

pipe = sb.Pipeline()

docs = pipe(['I see a mountain. I also see a lake.'])

for sentence in docs[0]:
    print(sentence.stuples)
```

Output:

```terminal
[OTN(i, see, mountain), NCL(mountain, be, seen)]
[OTN(i, see, lake), NCL(lake, be, seen)]
```

## Constructor

`Sentence()`

## Magic methods

### \_\_iter\_\_

`iter(Sentence)`

Returns a list of [SemanticTuples](semantic-tuple.md).
