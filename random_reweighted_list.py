import random
from typing import List

"""Random weighted list which re-calculates the weights after each pick so you should have an even distribution of items
that are returned by the getRandomItem method"""


class RandomReweightedList(List):
    choices = {}
    items = []

    def __init__(self, items):
        super().__init__(items)
        self.items = items
        self.choices = {item: 1 for item in items}

    def get_random_item(self) -> any:
        item = random.choices(self.items, [sum(self.choices.values()) / self.choices[item] for item in self.items])[0]
        self.choices[item] = self.choices[item] + 1
        return item

    def __getitem__(self, item):
        super().__getitem__(item)

    def __setitem__(self, i, o):
        """not supported"""
