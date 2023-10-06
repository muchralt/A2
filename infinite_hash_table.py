from data_structures.referential_array import ArrayR

class InfiniteHashTable:
    TABLE_SIZE = 27

    def __init__(self, level = None):
        self.array:ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZE)
        self.count = 0
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
        elif self.array[position] is None:
            raise KeyError
        else:
            return self.array[position][1]

    def __setitem__(self, key, value):
        position = self.hash(key)
        if self.array[position] is None:
            self.array[position] = (key, value)
            self.count += 1

        elif isinstance(self.array[position][1], InfiniteHashTable):
            internal_table = self.array[position][1]
            internal_table.__setitem__(key, value)

        else:
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
            if internal_table.count == 1 and res[1]:
                internal_table = None
                new_position = self.hash(key)
                self.array[new_position] = res[0]
                return res
            return [res[0], False]

        elif self.array[position] is None:
            raise KeyError
        else:
            self.array[position] = None
            self.count -= 1
        if self.count == 1:
            for i in range(self.TABLE_SIZE):
                if self.array[i] is not None:
                    return [self.array[i], True]
        
    def get_location(self, key):
        # location = [self.hash(key)]
        # if self.level < len(key) and key[self.level] in self.table:
        #     location += self.table[key[self.level]].get_location(key)
        # return location
        pass

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