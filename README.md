# MyBPE

This is a minimal implementation of Byte Pair Encoding (BPE) based on
[Andrej karpathy's Video on YouTube](https://www.youtube.com/watch?v=zduSFxRajkE&t=7s).

Example:

```python
from mybpe import BytePairEncoder

training_text: str = "This is a simple example of BPE"

bpe = BytePairEncoder(text=training_text, vocab_size=260)

ids: list[int] = bpe.encode("Text to encode")
print(ids)

decoded_text: str = bpe.decode(ids)
print(decoded_text)
```
