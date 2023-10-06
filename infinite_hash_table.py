class InfiniteHashTable:
    TABLE_SIZE = 27

    def __init__(self, level):
        # self.level = 0
        # self.table = {}

        self.array:ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZES)
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
        if self.level == len(key):
            return self.table.get(key, None)
        elif self.level < len(key) and key[self.level] in self.table:
            return self.table[key[self.level]].__getitem__(key)
        else:
            return None

    def __setitem__(self, key, value):
        # if self.level == len(key):
        #     self.table[key] = value
        # elif self.level < len(key):
            # table_index = self.hash(key)
            # if table_index not in self.table:
            #     self.table[table_index] = InfiniteHashTable()
            #     self.table[table_index].level = self.level + 1
            # self.table[table_index].__setitem__(key, value)

        position = self.hash(key)
        if self.array[position] is None:
            self.array[position] = (key, value)
        else:
            collision_cell = self.array[position]

            internal_table = InfiniteHashTable(self.level+1)
            new_collision_pos = internal_table.hash(collision_cell[0])
            internal_table.array[new_collision_pos] = collision_cell
            internal_table.__setitem__(key, value)
            self.array[position] = (key[:self.level+1], value)

    def __delitem__(self, key):
        if self.level == len(key):
            del self.table[key]
        elif self.level < len(key) and key[self.level] in self.table:
            self.table[key[self.level]].__delitem__(key)
            if len(self.table[key[self.level]].table) == 0:
                del self.table[key[self.level]]

    def get_location(self, key):
        location = [self.hash(key)]
        if self.level < len(key) and key[self.level] in self.table:
            location += self.table[key[self.level]].get_location(key)
        return location

    def sort_keys(self):
        keys = []
        for k, v in self.table.items():
            if isinstance(v, InfiniteHashTable):
                keys.extend([k + subkey for subkey in v.sort_keys()])
            else:
                keys.append(k)
        keys.sort()
        return keys