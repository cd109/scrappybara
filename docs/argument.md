# Argument

> Argument of a SemanticTuple.

## Example

```python
import scrappybara as sb

pipe = sb.Pipeline()

docs = pipe(['Vietnam has beautiful landscapes.'])
doc = docs[0]

# First semantic tuple of the first sentence:
stuple = doc.stuples[0]  # PTN(vietnam, have, landscape)

# Second argument of the tuple:
if stuple:
    arg = stuple.arg(1)
    print(arg.word, arg.code, arg.tag)
```

Output:

```terminal
have T VERB
```

## Constructor

`Argument(word, code, is_affirmative=True)`

### Call arguments

Call argument | Type | Description
-- | -- | --
`word` | string | Word contained in the argument.
`code` | string | Character code of the argument.

### Named arguments

Named argument | Type | Default | Description
-- | -- | -- | --
`is_affirmative` | boolean | `True` | Whether the argument is affirmative.

Only verbs can have this property set to `False` during tuples' extraction.

## Magic methods

### \_\_str\_\_

`str(Argument)`

Returns a string: same as `Argument.flatten()`.

## Methods

### flatten

`Argument.flatten(with_decorators=True)`

Returns a string: representation of the argument.

#### Named arguments

Named argument | Type | Default | Description
-- | -- | -- | --
`with_decorators` | boolean | `True` | Whether to display other strings around the word: e.g. *NOT* when negative.

## Properties

### code

`Argument.code` returns a string: character code that describes the type of argument.

Code | Part-of-speech tag | Description
-- | -- | --
**A** | **ADJ** | Adjective that is not a past-participle: e.g. *tall*, *breaking*
**L** | **ADJ** | Adjective that is a past-participle: e.g. *cooked*, *baked*
**N** | **NOUN** | Common noun: e.g. *country*, *can opener*
**P** | **NOUN** | Proper noun: e.g. *Laura*, *Ministry of Foreign Affairs*
**O** | **NOUN** | Pronoun: e.g. *something*, *he*, *him*
**S** | **NOUN** | Symbolic noun: e.g. *mysite.com*, *#OnSale*
**U** | **NOUN** | Numeral noun: e.g. *37*, *twenty-two*
**T** | **VERB** | Transitive verb, used with an object: e.g. *ask a question*
**I** | **VERB** | Intransitive verb, used without object: e.g. *eat*, *sleep*
**R** | **VERB** | Verb with a recipient, used with an indirect object: e.g. *ask somebody* 

### is_affirmative

`Argument.is_affirmative`

Returns a boolean: whether the verb has been found with an affirmative form in the sentence.

### tag

`Argument.tag`

Returns a string: part-of-speech tag of the argument.

The value can only be **NOUN**, **VERB** or **ADJ**.

### word

`Argument.word`

Returns a string: word contained in the argument.
