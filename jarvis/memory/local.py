# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午2:51
# @Author  : Su Yang
# @File    : local.py
# @Software: PyCharm 
# @Comment :
import dataclasses
import os
from typing import Any, List, Optional, Tuple

import numpy as np
import orjson

from jarvis.memory.memory import Memory
from jarvis.utils.embedding import create_embedding
import jarvis.settings as settings

EMBED_DIM = settings.EMBEDDING_DIM
SAVE_OPTIONS = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS


def create_default_embeddings():
    return np.zeros((0, EMBED_DIM)).astype(np.float32)


@dataclasses.dataclass
class CacheContent:
    texts: List[str] = dataclasses.field(default_factory=list)
    embeddings: np.ndarray = dataclasses.field(
        default_factory=create_default_embeddings
    )


class LocalMemory(Memory):
    """A class that stores the memory in a local file"""

    def __init__(self) -> None:
        """Initialize a class instance

        Args:
            None

        Returns:
            None
        """
        self.filename = f"{settings.MEMORY_INDEX}.json"
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "w+b") as f:
                    file_content = f.read()
                    if not file_content.strip():
                        file_content = b"{}"
                        f.write(file_content)

                    loaded = orjson.loads(file_content)
                    self.data = CacheContent(**loaded)
            except orjson.JSONDecodeError:
                print(f"Error: The file '{self.filename}' is not in JSON format.")
                self.data = CacheContent()
        else:
            print(
                f"Warning: The file '{self.filename}' does not exist."
                "Local memory would not be saved to a file."
            )
            self.data = CacheContent()

    def add(self, text: str):
        """
        Add text to our list of texts, add embedding as row to our
            embeddings-matrix

        Args:
            text: str

        Returns: None
        """
        if "Command Error:" in text:
            return ""
        self.data.texts.append(text)

        embedding = create_embedding(text)

        vector = np.array(embedding).astype(np.float32)
        vector = vector[np.newaxis, :]
        self.data.embeddings = np.concatenate(
            [
                self.data.embeddings,
                vector,
            ],
            axis=0,
        )

        with open(self.filename, "wb") as f:
            out = orjson.dumps(self.data, option=SAVE_OPTIONS)
            f.write(out)
        return text

    def clear(self) -> str:
        """
        Clears the redis server.

        Returns: A message indicating that the memory has been cleared.
        """
        self.data = CacheContent()
        return "Obliviated"

    def get(self, data: str) -> Optional[List[Any]]:
        """
        Gets the data from the memory that is most relevant to the given data.

        Args:
            data: The data to compare to.

        Returns: The most relevant data.
        """
        return self.get_relevant(data, 1)

    def get_relevant(self, data: str, k: int = 5) -> List[Any]:
        """
        matrix-vector mult to find score-for-each-row-of-matrix
         get indices for top-k winning scores
         return texts for those indices
        Args:
            data: str
            k: int

        Returns: List[str]
        """
        embedding = create_embedding(data)

        scores = np.dot(self.data.embeddings, embedding)

        top_k_indices = np.argsort(scores)[-k:][::-1]

        return [self.data.texts[i] for i in top_k_indices]

    def get_stats(self) -> Tuple[int, Tuple[int, ...]]:
        """
        Returns: The stats of the local cache.
        """
        return len(self.data.texts), self.data.embeddings.shape
