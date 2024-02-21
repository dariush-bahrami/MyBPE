"""This module contains functions for byte pair encoding (BPE)."""

from collections import Counter


def get_most_common_pair(ids: list[int]) -> tuple[int, int]:
    """Returns the most common pair of ids in a list of ids.

    Args:
        ids (list[int]): A list of ids.

    Returns:
        tuple[int, int]: The most common pair of ids.
    """
    pair_counts = Counter(zip(ids[:-1], ids[1:]))
    most_common_pair = pair_counts.most_common(1)[0][0]
    return most_common_pair


def merge_pair(ids: list[int], pair: tuple[int, int], id: int) -> list[int]:
    """Merge a pair of ids in a list of ids with a new id.

    Args:
        ids (list[int]): A list of ids.
        pair (tuple[int, int]): A pair of ids.
        id (int): The new id to replace the pair of ids with.

    Returns:
        list[int]: The list of ids with the pair merged.
    """
    result: list[int] = []
    i = 0
    while i < len(ids):
        if ((i + 1) < len(ids)) and ((ids[i], ids[i + 1]) == pair):
            result.append(id)
            i += 2
        else:
            result.append(ids[i])
            i += 1
    return result


def unmerge_pair(ids: list[int], pair: tuple[int, int], id: int) -> list[int]:
    """Unmerge a given id in a list of ids with a pair of ids.

    Args:
        ids (list[int]): A list of ids.
        pair (tuple[int, int]): A pair of ids.
        id (int): The id of the pair to unmerge.

    Returns:
        list[int]: The list of ids with the pair unmerged.
    """
    result: list[int] = []
    for token in ids:
        if token == id:
            result.extend(pair)
        else:
            result.append(token)
    return result


def get_id_to_pair(ids: list[int], vocab_size: int) -> dict[int, tuple[int, int]]:
    """Get a dictionary that maps ids to pairs of ids.

    Args:
        ids (list[int]): A list of ids.
        vocab_size (int): The vocab size.

    Returns:
        dict[int, tuple[int, int]]: A dictionary that maps ids to pairs of ids. The ids
            are in the range [256, vocab_size).

    """
    id_to_pair = {}
    for id in range(256, vocab_size):
        most_common_pair = get_most_common_pair(ids)
        id_to_pair[id] = most_common_pair
        ids = merge_pair(ids, most_common_pair, id)
    return id_to_pair


def encode(ids: list[int], id_to_pair: dict[int, tuple[int, int]]) -> list[int]:
    """Encode a list of ids using a dictionary that maps ids to pairs of ids. The pairs
    are merged iteratively from the smallest id to the largest id.

    Args:
        ids (list[int]): A list of ids.
        id_to_pair (dict[int, tuple[int, int]]): A dictionary that maps ids to pairs of
            ids.

    Returns:
        list[int]: A list of ids with the pairs merged.
    """
    for id in sorted(id_to_pair.keys()):
        pair = id_to_pair[id]
        ids = merge_pair(ids, pair, id)
    return ids


def decode(ids: list[int], id_to_pair: dict[int, tuple[int, int]]) -> list[int]:
    """Decode a list of ids using a dictionary that maps ids to pairs of ids. The pairs
    are unmerged iteratively from the largest id to the smallest id.

    Args:
        ids (list[int]): A list of ids.
        id_to_pair (dict[int, tuple[int, int]]): A dictionary that maps ids to pairs of
            ids.

    Returns:
        list[int]: A list of ids with the pairs unmerged.
    """
    for id in sorted(id_to_pair.keys(), reverse=True):
        pair = id_to_pair[id]
        ids = unmerge_pair(ids, pair, id)
    return ids
