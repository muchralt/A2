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

        if sizes is None:
            self.top_level_hash_table = LinearProbeTable(self.TABLE_SIZES)
        else:
            self.top_level_hash_table = LinearProbeTable(sizes)

        self.top_level_hash_table.hash = lambda k: self.hash1(k)
        
        if internal_sizes is not None:
            self.TABLE_SIZES = internal_sizes

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

        :complexity best: O(hash(key1) + hash(key2)) first position is empty
        :complexity worst: O(hash(key1) + hash(key2) + N*comp(K1) + M*comp(K2)) when we've searched the entire table
        where N is the tablesize and M is the internal table size.
        """
        position1 = self.top_level_hash_table._linear_probe(key1, is_insert)
        if is_insert is True and self.top_level_hash_table.array[position1] is None:
            internal_table = LinearProbeTable(self.TABLE_SIZES)
            internal_table.hash = lambda k: self.hash2(k, internal_table)
            self.top_level_hash_table.array[position1] = (key1, internal_table)
            self.top_level_hash_table.count += 1

        internal_table = self.top_level_hash_table.array[position1][1]

        position2 = internal_table._linear_probe(key2, is_insert)
        return (position1, position2)

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        complexity best case: O(M), where M is the number of top-level keys.
        complexity worst case: O(N + __getitem__) where N is internal table size.
        """
        if key is None:
            for i in range(self.top_level_hash_table.table_size):
                if self.top_level_hash_table.array[i] is None:
                    continue
                else:
                    yield self.top_level_hash_table.array[i][0]
        else:
            internal_table = self.top_level_hash_table.__getitem__(key)
            for i in range(internal_table.table_size):
                if internal_table.array[i] is None:
                    continue
                else:
                    yield internal_table.array[i][0]

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        :complexity best case: O(N) where N is self.top_level_hash_table.table_sizes.
        :complexity worst case: O(hash(key) + __getitem__ + M) where M is self.internal_sizes.
        """
        if key is None:
            return self.top_level_hash_table.keys()

        else:
            internal_table = self.top_level_hash_table.__getitem__(key)
            internal_table.hash = lambda k: self.hash2(k, internal_table)
            return internal_table.keys()

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        complexity best case: O(M * N), where M is the number of top-level values
                                and N is the number of internal-level values.
        complexity worst case: O(N + __getitem__) where N is internal table size.
        """
        if key is None:
            for i in range(self.top_level_hash_table.table_size):
                cell = self.top_level_hash_table.array[i]
                if cell is None:
                    continue
                else:
                    internal_table = cell[1]
                    for value in internal_table.values():
                        yield value
        else:
            internal_table = self.top_level_hash_table.__getitem__(key)
            for i in range(internal_table.table_size):
                if internal_table.array[i] is None:
                    continue
                else:
                    yield internal_table.array[i][1]

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        complexity best case: O(N), where N is the number of top-level keys.
        complexity worst case: O(N + M), where N is the number of top-level keys, 
                                and M is the total number of values in all internal tables.
        """
        if key is None:
            internal_table_list = self.top_level_hash_table.values()
            return [value for internal_table in internal_table_list for value in internal_table.values()]        

        else:
            internal_table = self.top_level_hash_table.__getitem__(key)
            internal_table.hash = lambda k: self.hash2(k, internal_table)
            return internal_table.values()
        
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

        complexity best/worst case: O(_linear_probe)
        """
        position = self._linear_probe(key[0], key[1], False)
        internal_table = self.top_level_hash_table.array[position[0]][1]
        return internal_table.array[position[1]][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        complexity best case: O(1), where its the first item.
        complexity worst case: O(N*hash(K1) + N*hash(K2) + N^2*comp(K1) N^2*comp(K2)), where it needs to rehash the top-level 
                                and internal tables and lots of probing. N is the table size.
        """
        position = self._linear_probe(key[0], key[1], True)

        if self.top_level_hash_table.array[position[0]] is None:
            self.top_level_hash_table.count += 1

        internal_table = self.top_level_hash_table.array[position[0]][1]

        if len(self.top_level_hash_table) > self.top_level_hash_table.table_size / 2:
            self.top_level_hash_table._rehash()

        if internal_table.array[position[1]] is None:
            internal_table.count += 1

        if len(internal_table) > internal_table.table_size / 2:
            internal_table._rehash()

        internal_table.array[position[1]] = (key[1], data)

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        complexity best case: O(_linear_probe), where we don't have to delete the internal table.
        complexity worst case: O(_linear_probe*2), where we do have to delete the internal table.
        """
        position = self._linear_probe(key[0], key[1], False)
        internal_table = self.top_level_hash_table.array[position[0]][1]
        internal_table.__delitem__(key[1])
        if internal_table.is_empty():
            self.top_level_hash_table.__delitem__(key[0])
            
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
