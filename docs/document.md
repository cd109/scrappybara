# Document

> Output of the Pipeline.

## Example

```python
import scrappybara as sb

pipe = sb.Pipeline()

docs = pipe(['I see a mountain. I also see a lake.'])

print(docs[0].stuples)
```

Output:

```terminal
[
    OTN(i, see, mountain),
    NCL(mountain, be, seen),
    OTN(i, see, lake),
    NCL(lake, be, seen)
]
```

## Constructor

`Document()`

## Magic methods

### \_\_iter\_\_

`iter(Document)`

Returns an iterator of [Sentences](sentence.md).

## Properties

### sentences

`Document.sentences`

Returns the list of [Sentences](sentence.md).

### stuples

`Document.stuples`

Returns the list of [SemanticTuples](semantic-tuple.md).

The list is the consolidation of [SemanticTuples](semantic-tuple.md) extracted from every sentences.
