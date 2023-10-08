from __future__ import annotations
from algorithms.mergesort import mergesort, merge
from algorithms.binary_search import binary_search
from data_structures.hash_table import LinearProbeTable

from mountain import Mountain

class MountainOrganiser:
    """
    Unless stated otherwise, all methods have O(1) complexity.
    """

    def __init__(self) -> None:
        self.mountains_list = []
        self.mountains_table = LinearProbeTable()

    def cur_position(self, mountain: Mountain) -> int:
        """
        Finds the rank of the provided mountain given all mountains included so far.

        :raises KeyError: when the mountain doesn't exist.

        complexity best case: O(1), where it is the only mountain or first mountain in the list.
        complexity worst case: O(log(N)), where N is the total number of mountains included so far.
        """
        if mountain not in self.mountains_list:
            raise KeyError
        else:
            return self.mountains_table[mountain.name]
        
    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds a list of mountains to the organiser

        complexity best/worst case: O(Mlog(M)+N), where M is the length of the input list, and
                                N is the total number of mountains included so far.
        """
        self.mountains_list = merge(self.mountains_list, mergesort(mountains, key=lambda x:x.difficulty_level), key=lambda x:x.difficulty_level)

        for i, mountain in enumerate(self.mountains_list):
            print(i, mountain.name)
            self.mountains_table.__setitem__(mountain.name, i)
       
