import random
from collections.abc import MutableSequence


class RandomEvenDistributedList(MutableSequence):
    """Random weighted list which re-calculates the weights after each pick so you should have an even distribution of items
    that are returned by the getRandomItem method.

    This does not guarantee a 100% even distribution, but guarantees a base distribution of within a few % margins of
    "error"

    You can optionally specify a reset_interval to prevent python from having troubles with too little weighs.
    Defaults to 20. A higher reset_interval should not affect the distribution, but it is rather a way to not have
    weighs e.g. 0.00000000001 etc, in which the distribution would be lost.
    """
    reset_interval = 10

    def __init__(self, data=None, reset_interval=20):
        super(RandomEvenDistributedList, self).__init__()
        if data is not None:
            self._data = list(data)
        else:
            self._data = list()

        self.choices = {item: 1 for item in self._data}
        self.reset_interval = reset_interval

    def get_random_item(self) -> any:
        """"""

        """reset at specific intervals so the weighs don't get too low"""
        if sum(self.choices.values()) > self.reset_interval:
            self.choices = {item: 1 for item in self._data}

        item = random.choices(self._data, [1 / self.choices[item] for item in self._data])[0]
        self.choices[item] = self.choices[item] + 1
        return item

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._data)

    def __len__(self):
        """List length"""
        return len(self._data)

    def __getitem__(self, ii):
        """Get a list item"""
        return self._data[ii]

    def __delitem__(self, ii):
        """Delete an item"""
        del self.choices[self.__getitem__(ii)]
        del self._data[ii]

    def __setitem__(self, ii, val):
        # optional: self._acl_check(val)
        self._data[ii] = val
        self.choices.setdefault(val, 1)

    def __str__(self):
        return str(self._data)

    def insert(self, ii, val):
        # optional: self._acl_check(val)
        self._data.insert(ii, val)
        self.choices[val] = 1

    def append(self, val):
        self.insert(len(self._data), val)
        self.choices[val] = 1


if __name__ == '__main__':
    min_dist = None
    max_dist = None
    for j in range(0, 100):
        v = RandomEvenDistributedList(['my_item', 'my_other_item', '3', 'sonar', 4])
        choices = {item: 0 for item in v}
        for i in range(0, 10000):
            item = v.get_random_item()
            choices[item] = choices[item] + 1

        maxpct = 100 * (max(choices.values()) / 10000)
        minpct = 100 * (min(choices.values()) / 10000)
        max_dist = maxpct if max_dist is None else max(max_dist, maxpct)
        min_dist = minpct if min_dist is None else min(min_dist, minpct)

    print("Max: {0}, Min: {1}".format(max_dist, min_dist))