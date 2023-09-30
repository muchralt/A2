from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR
from data_structures.linked_stack import LinkedStack

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.top_level_hash_table = LinearProbeTable(self.TABLE_SIZES)
        
        if internal_sizes is not None:
            self.TABLE_SIZES = internal_sizes
        self.TABLE_SIZES = DoubleKeyTable.TABLE_SIZES

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        position1 = self.hash1(key1)

        probe1 = False
        probe2 = False

        for _ in range(self.top_level_hash_table.table_size):
            if self.top_level_hash_table.array[position1] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert is True and self.top_level_hash_table.__contains__(key1) is False:
                    internal_table = LinearProbeTable(self.TABLE_SIZES)
                    self.top_level_hash_table.array[position1] = (key1, internal_table)
                    probe1 = True
                    break
                else:
                    raise KeyError(key1)
            elif self.top_level_hash_table.array[position1][0] == key1:
                probe1 = True
                break
            else:
                # Taken by something else. Time to linear probe.
                position1 = (position1 + 1) % self.top_level_hash_table.table_size

        if is_insert is True and probe1 is False:
            raise FullError("Table is full!")
        elif probe1 is False:
            raise KeyError(key1)
        
        position2 = self.hash2(key2, internal_table)

        for _ in range(internal_table.table_size):
            if internal_table.array[position2] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert:
                    probe2 = True
                    break
                else:
                    raise KeyError(key2)
            elif internal_table.array[position2][0] == key2:
                probe2 = True
                break
            else:
                # Taken by something else. Time to linear probe.
                position2 = (position2 + 1) % internal_table.table_size

        if is_insert is True and probe2 is False:
            raise FullError("Table is full!")
        elif probe2 is False:
            raise KeyError(key2)
        
        return (position1, position2)

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            DoubleKeyTable.keys(self, key)
        else:
            pass

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        top_level_keys = []
        internal_keys = []
        if key is None:
            for i in range(self.top_level_hash_table.table_size):
                if self.top_level_hash_table.array[i] is not None:
                    top_level_keys.append(self.top_level_hash_table.array[i][0])
            return top_level_keys

        else:
            position = self.hash1(key)
            internal_table = self.top_level_hash_table.array[position][1]
            for i in range(internal_table.table_size):
                if internal_table.array[i] is not None:
                    internal_keys.append(internal_table.array[i][0])
            return internal_keys

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        all_values = []
        internal_values = []

        if key is None:
            for i in range(self.top_level_hash_table.table_size):
                if self.top_level_hash_table.array[i] is not None:
                    all_values.append(self.top_level_hash_table.array[i][1])
            return all_values
        else:
            position = self.hash1(key)
            internal_table = self.top_level_hash_table.array[position][1]
            for i in range(internal_table.table_size):
                if internal_table.array[i] is not None:
                    internal_values.append(internal_table.array[i][1])
            return internal_values
        
    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        raise NotImplementedError()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        raise NotImplementedError()

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        raise NotImplementedError()

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.top_level_hash_table.table_size

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.top_level_hash_table.__len__()

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()
