# Extract semantic tuples

> Learn how to convert natural language into data that a computer can use.

## Overview

A [Pipeline](pipeline) will process texts and return a list of corresponding [Documents](document).

A document contains [Sentences](sentence). Each [Sentence](sentence) contains its extracted [SemanticTuples](semantic-tuple).

A [SemanticTuple](semantic-tuple) is made of two or more [Arguments](argument).

## Step by step

### 1. Create a Pipeline

```python
import scrappybara as sb

pipe = sb.Pipeline()
```
The constructor must load resources such as deep-learning models, a language model, word vectors, etc. Therefore this step can take few seconds. 

### 2. Process text

```python
docs = pipe(['Josh met a friend. Her name was slavic.'])
doc = docs[0]
```

A [Pipeline](pipeline) is callable. We can use the instance as a function with a single argument: a list of texts to process.

A text is simply a Python string. It's usually a body of text that makes sense on its own: e.g. a news article, a blog post, an email etc.

### 3. Read a Document

#### Get the semantic tuples

The output of a [Pipeline](pipeline) is a list of [Documents](document).

The [Document](document)'s property `stuples` returns the [SemanticTuples](semantic-tuple) gathered from every [Sentences](sentence).

```python
print(doc.stuples)
```

Would print:

```terminal
[PTN(josh, meet, friend), NCL(friend, be, met), NCA(name, be, slavic)]
```

In front of each tuple, you can read a string code:
* `PTN` means: *Proper noun + Transitive verb + Noun*.
* `NCL` means: *Noun + Copula + Past-participle adjective*.
* `NCA` means: *Noun + Copula + Adjective*. 

In other words, the code of a [SemanticTuple](semantic-tuple) is the concatenation of each [Argument](argument)'s code.

The complete list of [Argument](argument)'s codes can be found [here](argument#code).

Their possible combination to form a [SemanticTuple](semantic-tuple) can be found [here](semantic-tuple#code).

#### Group tuples by sentences

A [Document](document) is made of [Sentences](sentence). So, if you want the tuples grouped by [Sentences](sentence), you can iterate over a [Document](document):


```python
for sentence in doc:
    print(sentence.stuples)
```

Would print:

```terminal
[PTN(josh, meet, friend), NCL(friend, be, met)]
[NCA(name, be, slavic)]
```

You can also iterate over a [Sentence](sentence) to access its [SemanticTuples](semantic-tuple):

```python
for sentence in doc:
    for stuple in sentence:
        print(len(stuple), stuple)
```

Would print:

```terminal
3 PTN(josh, meet, friend)
3 NCL(friend, be, met)
3 NCA(name, be, slavic)
```

`len(stuple)` returned the number of arguments in the tuple.


### 4. Filter semantic tuples

If we only wanted the tuples with 3 arguments (triples) that are predicates (the second argument is a transitive verb), we could filter the tuples like this:

```python
stuples = [st for st in doc.stuples if len(st) == 3 and st.code[1] == 'T']
```

Would print:

```terminal
[PTN(josh, meet, friend)]
```

There is another way for writing the same filter, using [Arguments](argument.md)'s properties:

```python
stuples = [st for st in doc.stuples if len(st) == 3 and st.arg(1).code == 'T']
```

### 5. Access arguments

We will use the [Argument](argument.md)'s properties in order to compile data into any desired format.

A [SemanticTuple](semantic-tuple.md) is made of [Arguments](argument.md). Here is an example on how to access them:

```python
for stuple in doc.stuples:
    arg = stuple.arg(0)  # First argument of the tuple
    print(arg.word, arg.code, arg.tag)
```

Would print:

```terminal
josh P NOUN
friend N NOUN
name N NOUN
```

To get all [Arguments](argument.md) of a [SemanticTuple](semantic-tuple.md), we can iterate over it:

```python
for stuple in doc.stuples:
    for arg in stuple:
        print(arg.word, arg.code, arg.tag)
```

Would print:

```terminal
josh P NOUN
meet T VERB
friend N NOUN
friend N NOUN
be C NOUN
met L ADJ
name N NOUN
be C NOUN
slavic A ADJ
``` 

## Next steps

To explore the different options related to tuple extraction, you can read the following pages:
- [Pipeline](pipeline.md)
- [Document](document.md)
- [Sentence](sentence.md)
- [SemanticTuple](semantic-tuple.md)
- [Argument](argument.md)
