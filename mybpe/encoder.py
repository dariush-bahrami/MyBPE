"""The byte pair encoder module."""

from .functions import decode, encode, get_id_to_pair


class BytePairEncoder:
    """A byte pair encoder.

    Args:
        text (str): The text to train the encoder on.
        vocab_size (int): The vocab size.
    """

    def __init__(self, text: str, vocab_size: int):
        self.vocab_size = vocab_size
        self.id_to_pair = get_id_to_pair(list(text.encode("utf-8")), vocab_size)

    def encode(self, text: str) -> list[int]:
        """Encode a text using the byte pair encoder.

        Args:
            text (str): The text to encode.

        Returns:
            list[int]: The encoded text.
        """
        return encode(list(text.encode("utf-8")), self.id_to_pair)

    def decode(self, ids: list[int]) -> str:
        """Decode a list of tokens using the byte pair encoder.

        Args:
            ids (list[int]): The ids to decode.

        Returns:
            str: The decoded text.
        """
        return bytes(decode(ids, self.id_to_pair)).decode("utf-8")
