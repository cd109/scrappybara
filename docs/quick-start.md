# Quick start

> As easy as *1, 2*

## Install Scrappybara

### Compatibility

Latest Scrappybara v1.0.0 supports python 3.5-3.8.

### Pip install

Scrappybara is using Tensorflow v2.x for machine learning. Therefore you will need to install it first:

```shell
pip install tensorflow
```

Then the current release of Scrappybara:

```shell
pip install scrappybara
```

### Basic usage

```python
import scrappybara as sb

# Instantiate a pipeline (it might take few seconds to load)
pipe = sb.Pipeline()

# Process a text
docs = pipe(['I have a derpy dog.'])

# Preview the semantic tuples
print(docs[0].stuples)
```

And you should see 2 predicates of type **NOUN**+**VERB**+**NOUN**:

```terminal
[OTN(i, have, dog), NCA(dog, be, derpy)]
```

### Use GPUs

To greatly increase performances when processing a large collection of texts, it is recommended to use a GPU:
* [TensorFlow GPU support](https://www.tensorflow.org/install/gpu)

### Next steps

Check out the tutorial "[Extract semantic tuples](extract-semantic-tuples.md)".
