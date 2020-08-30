<img
    src="https://raw.githubusercontent.com/ericperriard/scrappybara/master/docs/img/logo.svg"
    width="350"
    style="display: block; width: 350px; margin: auto; margin-bottom: 3em"
/>

> Python library for Natural Language Processing.

Scrappybara provides tools to extract structured data from unstructured text. This data is useful for researchers and developers who want to build NLP applications.

Scappybara focuses on a single language: English. You won't have to bother with training models or downloading resources. Everything works right off the bat. This commitment also allows more development efforts tackling the meaning of language.

## Official website

* [ericperriard.github.io/scrappybara](https://ericperriard.github.io/scrappybara) (with tutorials & documentation)

## Where to ask questions

Type | URL
-- | --
Usage questions | [Stack Overflow](https://stackoverflow.com/questions/tagged/scrappybara)
Bug reports | [GitHub Issue Tracker](https://github.com/ericperriard/scrappybara/issues)
Feature requests | [GitHub Issue Tracker](https://github.com/ericperriard/scrappybara/issues)

## Install

Scrappybara is using Tensorflow v2.x for machine learning. Therefore you will need to install it first:

```shell
pip install tensorflow
```

Then the current release of Scrappybara:

```shell
pip install scrappybara
```

#### Try your first Scrappybara program

```python
import scrappybara as sb
pipe = sb.Pipeline()
docs = pipe(['I have a derpy dog.'])
print(docs[0].stuples)
```

And you should see 2 predicates of type **NOUN**+**VERB**+**NOUN**:

```terminal
[OTN(i, have, dog), NCA(dog, be, derpy)]
```

For more examples, see the tutorials on the [official website](https://ericperriard.github.io/scrappybara).
