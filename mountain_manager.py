from __future__ import annotations
from mountain import Mountain
import copy

class MountainManager:

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain) -> None:
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        return [mountain for mountain in self.mountains if mountain.difficulty_level == diff]

    def group_by_difficulty(self) -> list[list[Mountain]]:
        new_list = []
        mountains_copy = copy.deepcopy(self.mountains)
        mountain_iter = iter(self.mountains)
        mountain_iter2 = iter(self.mountains)
        for mountain in mountain_iter:
            new_list.append([item for item in mountain_iter2 if item.difficulty_level == mountain.difficulty_level])
        return new_list

        
            
