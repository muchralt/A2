from data_structures.referential_array import ArrayR

class InfiniteHashTable:
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
        position = self.hash(key)

        if isinstance(self.array[position][1], InfiniteHashTable):
            internal_table = self.array[position][1]
            internal_table.__getitem__(key)

        elif self.array[position][0] != key:
            raise KeyError
        else:
            return self.array[position][1]

    def __setitem__(self, key, value):
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
        # keys = []
        # for k, v in self.table.items():
        #     if isinstance(v, InfiniteHashTable):
        #         keys.extend([k + subkey for subkey in v.sort_keys()])
        #     else:
        #         keys.append(k)
        # keys.sort()
        # return keys
        pass
    
    
    def __len__(self):
        return self.count