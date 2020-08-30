# SemanticTuple

> Semantic tuple with n arguments.

## Example

```python
import scrappybara as sb

pipe = sb.Pipeline()

docs = pipe(['A colorful bicycle.'])

# First tuple of the document
stuple = docs[0].stuples[0]

print(stuple)
```

Output:

```terminal
NCA(bicycle, be, colorful)
```

## Constructor

`SemanticTuple(*args)`

### Call arguments

Call argument | Type | Description
-- | -- | --
`args` | series of [Arguments](argument.md) | Arguments of the tuple.

## Magic methods

### \_\_iter\_\_

`iter(SemanticTuple)`

Returns an iterator of [Arguments](argument.md).

### \_\_len\_\_

`len(SemanticTuple)`

Returns an integer: the number of [Arguments](argument.md).

### \_\_str\_\_

`str()`

Returns a string: same as `SemanticTuple.flatten()`.

## Methods

### arg

`SemanticTuple.arg(idx)`

Returns the [Argument](argument.md) at a given index. First argument has index 0.

#### Call arguments

Call argument | Type | Description
-- | -- | --
`idx` | integer | 0-idx of the argument to return.

### flatten

`SemanticTuple.flatten(with_decorators=True)`

Returns a string: flat representation of the tuple.

#### Named arguments

Named argument | Type | Default | Description
-- | -- | -- | --
`with_decorators` | boolean | `True` | Display arguments with decorators: e.g. *NOT* when negative.

### has_any_arg_with_code

`SemanticTuple.has_any_arg_with_code(arg_code)`

Returns a boolean: whether the tuple contains any arg with the given code.

#### Call arguments

Call argument | Type | Description
-- | -- | --
`arg_code` | string | Single-character code to match.

See [Argument.code](argument.md#code) to see the possible values.

## Properties

### code

`SemanticTuple.code`

Returns a string: code that describes the type of a tuple. It concatenates [Argument.code](argument.md#code) of all arguments.

Not every combination of [Argument](argument.md)'s codes is possible. Below are the type of tuples that can be extracted (the extraction process is greedy: it tries to extract tuples with the highest order possible. We use the wildcard `*` to indicate that the code could take any value corresponding to a part-of-speech tag).

#### Semantic quintuple

Code | Description | Examples
-- | -- | --
\*T\*T\* | **NOUN**+**VERB**+**NOUN**+**VERB**+**NOUN** | Predicate: *I want to eat apples* => *(i, want, i, eat, apple)*

#### Semantic quadruple

Code | Description | Examples
-- | -- | --
\*T\*I | **NOUN**+**VERB**+**NOUN**+**VERB** | Predicate: *I want to eat* => *(i, want, i, eat)*

#### Semantic triple

Code | Description | Examples
-- | -- | --
\*T\* | **NOUN** + **VERB** + **NOUN** | Predicate: *I eat an apple* => *(i, eat, apple)*
\*C\* | **NOUN** + **VERB** + **NOUN** | Copula predicate: *I am a doctor* => *(i, be, doctor)*
\*C\* | **NOUN** + **VERB** + **ADJ** | Copula predicate: *I am thirsty* => *(i, be, thirsty)*

#### Semantic double 

Code | Description | Examples
-- | -- | --
\*I | **NOUN** + **VERB** | Predicate with an intransitive verb: *I go to the restaurant* => *(i, go)*
