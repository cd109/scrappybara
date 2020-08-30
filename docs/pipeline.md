# Pipeline

> Processes texts into Documents.

## Example

```python
import scrappybara as sb

pipe = sb.Pipeline()

docs = pipe(['This is a beautiful pipe. It does magical things.'])

print(docs[0].stuples)
```

Output:

```terminal
[
    OCN(this, be, pipe),
    NCA(pipe, be, beautiful),
    OTN(it, do, thing),
    NCA(thing, be, magical),
    NCL(thing, be, done)
]
```

## Constructor

`Pipeline(sentencizer=Sentencizer(), nb_processes=multiprocessing.cpu_count(), batch_size=128, use_gpu=True)`

### Named arguments

Named argument | Type | Default | Description |
-- | -- | -- | --
`sentencizer` | callable | Default [Sentencizer](sentencizer.md) | Takes a text and returns a list of list of tokens (grouped by sentence).
`nb_cores` | int | all cores available | Number of cores used by the pipeline.
`batch_size` | int | 128 | Size of batch that goes into deep-learning models.
`use_gpu` | boolean | True | Whether to use GPU for deep-learning inferences.

The default [Sentencizer](sentencizer.md) performs well with standard texts. But if your text has an odd or very specific formatting, you can use your own sentencization method (the sentencization process tokenizes text and groups tokens by sentences).

To greatly increase speed, `batch_size` is the most important parameter with `use_gpu` set to `True`. When processing a lot of texts, it's important to use the highest value possible. The value is limited by the GPU's available memory. 

Since Scrappybara is using TensorFlow for machine learning, you will need to follow these instructions in order to use your GPU:
* [TensorFlow GPU support](https://www.tensorflow.org/install/gpu)

## Magic methods

### \_\_call\_\_

`Pipeline(texts, chunk_nouns=True)`

Returns a list of [Documents](document.md).

#### Call Arguments

Call argument | Type | Description
-- | -- | --
`texts` | list of strings | Texts to be processed.

#### Named arguments

Named argument | Type | Default | Description
-- | -- | -- | --
`chunk_common_nouns` | boolean | `True` | Whether to attach common nouns as a single noun.

If `chunk_commoun_nouns` is `False`, only the root noun will be used: a *lemon squeezer* will just be a *squeezer*.
