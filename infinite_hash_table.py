from data_structures.referential_array import ArrayR
from algorithms.mergesort import mergesort

class InfiniteHashTable:
    """
    Unless stated otherwise, all methods have O(1) complexity.
    """
    TABLE_SIZE = 27

    def __init__(self, level = None):
        self.array:ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.bot_level = True
        #Initialise None argument for level: If level = None then self.level = 0
        if level is None:
            self.level = 0
        else:
            self.level = level

    def hash(self, key):
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key):
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        complexity best case: O(hash(key)), where we straight find the value.
        complexity worst case: O(hash(key) * N), where N is how many times we have to recurse
        """
        position = self.hash(key)

        if isinstance(self.array[position][1], InfiniteHashTable):
            internal_table = self.array[position][1]
            internal_table.__getitem__(key)

        elif self.array[position][0] != key:
            raise KeyError
        else:
            return self.array[position][1]

    def __setitem__(self, key, value):
        """
        Set an (key, value) pair in our hash table.

        complexity best case: O(hash(key)), where there are no collisions.
        complexity worst case: O(hash(key) )
        """
        position = self.hash(key)
        self.count += 1
        if self.array[position] is None:
            self.array[position] = (key, value)

        elif isinstance(self.array[position][1], InfiniteHashTable):
            internal_table = self.array[position][1]
            internal_table.__setitem__(key, value)

        else:
            self.bot_level = False
            collision_cell = self.array[position]
            internal_table = InfiniteHashTable(self.level+1)
            new_collision_pos = internal_table.hash(collision_cell[0])
            internal_table.array[new_collision_pos] = collision_cell
            internal_table.count += 1
            self.array[position] = (key[:self.level+1], internal_table)
            internal_table.__setitem__(key, value)

    def __delitem__(self, key):
        self.del_helper(key)
                
    def del_helper(self, key):
        position = self.hash(key)

        if isinstance(self.array[position][1], InfiniteHashTable):
            internal_table = self.array[position][1]
            res = internal_table.del_helper(key)
            self.count -= 1
            if internal_table.count == 1 and internal_table.bot_level:
                internal_table = None
                new_position = self.hash(key)
                self.array[new_position] = res
                self.bot_level = True
                return res
            return res

        elif self.array[position][0] != key:
            raise KeyError
        else:
            self.array[position] = None
            self.count -= 1
        if self.count == 1:
            for i in range(self.TABLE_SIZE):
                if self.array[i] is not None:
                    return self.array[i]
        
    def get_location(self, key):
        location = []
        position = self.hash(key)
        location.append(position)

        if isinstance(self.array[position][1], InfiniteHashTable):
            internal_table = self.array[position][1]
            return location + internal_table.get_location(key)
            
        elif self.array[position][0] != key:
            raise KeyError
        else:
            return location

    def sort_keys(self):
        return mergesort(self.keys())

    def keys(self):
        res = []
        for i in range(self.TABLE_SIZE):
            if self.array[i] is None:
                continue
            elif isinstance(self.array[i][1], InfiniteHashTable):
                internal_table = self.array[i][1]
                # res + internal_table.keys()
                internal_keys = internal_table.keys()
                res = res + internal_keys
            else:
                res.append(self.array[i][0])
        return res
    
    def __len__(self):
        return self.count