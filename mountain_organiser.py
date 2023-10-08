from __future__ import annotations
from algorithms.mergesort import mergesort, merge
from algorithms.binary_search import binary_search
from data_structures.hash_table import LinearProbeTable

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains_list = []
        self.mountains_table = LinearProbeTable()

    def cur_position(self, mountain: Mountain) -> int:
        if mountain not in self.mountains_list:
            raise KeyError
        else:
            return self.mountains_table[mountain.name]
        
    def add_mountains(self, mountains: list[Mountain]) -> None:
        
        self.mountains_list = merge(self.mountains_list, mergesort(mountains, key=lambda x:x.difficulty_level), key=lambda x:x.difficulty_level)

        for i, mountain in enumerate(self.mountains_list):
            print(i, mountain.name)
            self.mountains_table.__setitem__(mountain.name, i)
       