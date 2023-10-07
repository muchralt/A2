from __future__ import annotations
from algorithms.mergesort import mergesort, merge
from algorithms.binary_search import binary_search

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains_list = []

    def cur_position(self, mountain: Mountain) -> int:
        return binary_search(self.mountains_list, mountain.difficulty_level)
        
    def add_mountains(self, mountains: list[Mountain]) -> None:
        for mountain in mountains:
            input_list = mergesort(mountains, key=lambda x:x.difficulty_level)
        self.mountains_list = merge(self.mountains_list, input_list, key=lambda x:x.difficulty_level)