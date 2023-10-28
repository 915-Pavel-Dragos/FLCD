from random import randint


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str(f"({self.key}, {self.value})")


class SymbolTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = []
        for _ in range(capacity):
            _mylist = []
            self.table.append(_mylist)

    def __hash_function(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self.__hash_function(key)
        self.table[index].append(Node(key, value))
        self.size += 1

    def search(self, key, value):
        index = self.__hash_function(key)

        for element in self.table[index]:
            if element.value == value:
                return True
        return False

    def remove(self, key, value):
        index = self.__hash_function(key)

        for element in self.table[index]:
            if element.value == value:
                self.table[index].remove(element)

    def __str__(self):
        elements = []
        for my_list in self.table:
            new_list = []
            for element in my_list:
                new_list.append(str(element))
            elements.append(new_list)
        return str(elements)

    def __len__(self):
        return self.size

    def __contains__(self, key, value):
        try:
            self.search(key, value)
            return True
        except KeyError:
            return False


def main():
    my_symbol_table = SymbolTable(12)

    for _ in range(12):
        key = randint(1, 12)
        value = randint(1, 12)
        my_symbol_table.insert(key, value)
    print(my_symbol_table)


main()
