from __future__ import annotations
from algorithms.mergesort import mergesort, merge
from algorithms.binary_search import binary_search
from double_key_table import DoubleKeyTable, LinearProbeTable

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains_list = []
        self.difficulty_list = []
        self.test = LinearProbeTable()

    def cur_position(self, mountain: Mountain) -> int:
        if mountain not in self.mountains_list:
            raise KeyError
        else:
            return binary_search(self.difficulty_list, mountain.difficulty_level)
        
    def add_mountains(self, mountains: list[Mountain]) -> None:
        for mountain in mountains:
            self.difficulty_list.append(mountain.difficulty_level)
        input_list = mergesort(mountains, key=lambda x:x.difficulty_level)
        self.mountains_list = merge(self.mountains_list, input_list, key=lambda x:x.difficulty_level)
        self.difficulty_list = mergesort(self.difficulty_list)