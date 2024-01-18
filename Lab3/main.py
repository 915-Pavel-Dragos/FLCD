import re


class Pif:
    def __init__(self):
        self._table = []

    def add(self, token, pos):
        self._table.append((token, pos))

    def __str__(self):
        string = ""
        for elem in self._table:
            string += str(f"({elem[0]}, {elem[1]})\n")
        return string


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
        _sum = 0
        for letter in key:
            _sum += ord(letter)
        return _sum % self.capacity

    def get_value_by_key(self, key):
        index = self.__hash_function(key)
        return self.table[index][0].value

    def insert(self, key, value):
        index = self.__hash_function(key)
        if self.search(key) == -1:
            self.table[index].append(Node(key, value))
            self.size += 1
        else:
            new_index = self.search(key)
            self.table[index].append(Node(key, new_index))
            self.size += 1

    def search(self, key):
        index = self.__hash_function(key)

        for elem in self.table[index]:
            if elem.key == key:
                return elem.value
        return -1

    def remove(self, key):
        index = self.__hash_function(key)

        self.table[index].pop()
        self.size -= 1

    def get_index(self, key):
        index = self.__hash_function(key)
        if self.search(key) != -1 and len(self.table[index]) != 0:
            return self.table[index][0].value
        return -1

    def __str__(self):
        elements = []
        for my_list in self.table:
            new_list = []
            if len(my_list) > 0:
                for element in my_list:
                    new_list.append(str(element))
                elements.append(new_list)
        return str(elements)

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False

class FA:
    def __init__(self, filename):
        self.Q = []
        self.Sigma = []
        self.q0 = []
        self.F = []
        self.Gamma = {}
        self.read_input_file(filename)

    def read_input_file(self, filename):
        f = open(filename)
        # Read the set of states
        line = f.readline()
        for index in range(len(line)):
            if line[index] == ',' or line[index] == '}':
                self.Q.append(line[index - 1])
        # print(f"this is Q = {self.Q}\n")

        # Read the alphabet of the language
        line = f.readline()
        for index in range(len(line)):
            if line[index] == ',' or line[index] == '}':
                self.Sigma.append(line[index - 1])
        # print(f"this is Sigma = {self.Sigma}\n")

        # Read the set of the initial states
        line = f.readline()
        for index in range(len(line)):
            if line[index] == ',' or line[index] == '}':
                self.q0.append(line[index - 1])
        # print(f"this is q0 = {self.q0}\n")

        # Read the set of final states
        line = f.readline()
        for index in range(len(line)):
            if line[index] == ',' or line[index] == '}':
                self.F.append(line[index - 1])
        # print(f"this is F = {self.F}\n")

        # Read the set of transition states
        f.readline()
        line = f.readline()
        while line != '}':
            origin_index = line.find(',')
            dest_index = line.find(')')
            if (line[origin_index - 1], line[dest_index - 1]) in self.Gamma:
                self.Gamma[(line[origin_index - 1], line[dest_index - 1])].append(line[-2])
            else:
                self.Gamma[(line[origin_index - 1], line[dest_index - 1])] = [line[-2]]
            line = f.readline()
        # print(f"this is Gamma = {self.Gamma}")

    def is_dfa(self):
        for key in self.Gamma.keys():
            if len(self.Gamma[key]) > 1:
                return False
        return True

    def sequence_fa_accepted(self, sequence):
        if self.is_dfa():
            start = self.q0[0]
            for character in sequence:
                if character != '\"':
                    if (start, character) in self.Gamma.keys():
                        start = self.Gamma[(start, character)][0]
                    else:
                        return False
            if start in self.F:
                return True
        return False

    def __str__(self):
        string = "This is Q: " + str(self.Q) + "\n" + \
            "This is Sigma: " + str(self.Sigma) + "\n" + \
            "This is q0: " + str(self.q0) + "\n" + \
            "This is F: " + str(self.F) + "\n" + \
            "This is Gamma: " + str(self.Gamma)

        return string


def check_identifier(term):
    my_fa = FA("FA_identifier.in")
    return my_fa.sequence_fa_accepted(term)
    # return re.match(r'^[a-zA-Z]([a-zA-Z]|[0-9])*$', term) is not None


def check_constant(term):
    # return re.match(r'^0|[+-]?[1-9][0-9]*$|^\'.*\'$', term) is not None
    count = 0
    for char in term:
        if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+']:
            count += 1
    if count == len(term):
        my_fa = FA("FA_integer_constant.in")
        return my_fa.sequence_fa_accepted(term)
    else:
        return re.match(r'^\'.*\'$', term) is not None


class Scanner:
    def __init__(self):
        self.reserved_words = []
        self.operators = []
        self.separators = []

    def read_tokens(self):
        with open('Tokens.in', 'r') as f:
            for elem in range(14):
                self.operators.append(f.readline().strip())
            for elem in range(10):
                sep = f.readline().strip()
                if sep == 'space':
                    self.separators.append(" ")
                else:
                    self.separators.append(sep)
            for elem in range(13):
                self.reserved_words.append(f.readline().strip())

    def is_operator(self, operator):
        if operator in self.operators:
            return True
        return False

    @staticmethod
    def read_comment(line, index):
        letter = line[index]
        my_string = letter
        index += 1
        letter = line[index]
        while letter != '~':
            letter = line[index]
            my_string += letter
            index += 1
        return my_string, len(my_string)

    @staticmethod
    def read_string(line, index):
        letter = line[index]
        my_string = letter
        index += 1
        letter = line[index]
        while letter != '\'':
            letter = line[index]
            my_string += letter
            index += 1
        return my_string, len(my_string) - 1

    @staticmethod
    def more_characters_operators(line, index):
        letter = line[index]
        my_string = letter
        if letter == '<' and line[index + 1] == '<':
            my_string += '<'
        elif letter == '<' and line[index + 1] == ')':
            my_string += ')'
        elif letter == '<' and line[index + 1] == ')' and line[index + 2] == '=':
            my_string += ")="
        elif letter == '<' and line[index + 1] == '-':
            my_string += '-'
        if letter == '>' and line[index + 1] == '>':
            my_string += '>'
        if letter == '=' and line[index + 1] == '(' and line[index + 2] == '>':
            my_string += "=(>"
        if letter == '!' and line[index + 1] == '=':
            my_string += '='
        if letter == '+':
            my_string += '+'
        if letter == '-':
            my_string += '-'
        if letter == '*':
            my_string += '*'
        if letter == '/':
            my_string += '/'
        if letter == '%':
            my_string += '%'
        if len(my_string) > 1:
            return my_string, len(my_string)
        return my_string, 0

    def get_line_tokens(self, line):
        my_string = ""
        tokens = []
        index = 0
        while index < len(line):
            letter, aux = self.more_characters_operators(line, index)
            index += aux
            if letter == '~':
                my_string, aux = self.read_comment(line, index)
                index += aux
                tokens.append(my_string)
                my_string = ""
            elif letter == '\'':
                my_string, aux = self.read_string(line, index)
                index += aux
                tokens.append(my_string)
                my_string = ""
            elif letter not in self.operators and letter not in self.separators and letter != ' ' and \
                    letter != '\t' and letter != '\n':
                my_string += letter
            else:
                if my_string != "":
                    tokens.append(my_string)
                    my_string = ""
            if letter in self.operators or letter in self.separators and letter != '~':
                tokens.append(letter)
            index += 1
        return tokens


class Exec:
    @staticmethod
    def execute(fileName, ST1, ST2, PIF, ERROR, general_index):
        with open(fileName, 'r') as f:
            my_index_c = 0
            my_index_i = 0
            errors = []
            scan = Scanner()
            scan.read_tokens()
            identifiers = SymbolTable(10)
            constants = SymbolTable(10)
            my_pif = Pif()
            for line in f:
                tokens = scan.get_line_tokens(line)
                for elem in tokens:
                    if elem in scan.separators or elem in scan.operators or elem in scan.reserved_words:
                        my_pif.add(elem, -1)
                    elif check_constant(elem):
                        index = constants.get_index(elem)
                        if index == -1:
                            constants.insert(elem, my_index_c)
                            my_index_c += 1
                        value = constants.get_value_by_key(elem)
                        my_pif.add(elem, value)
                    elif check_identifier(elem):
                        index = identifiers.get_index(elem)
                        if index == -1:
                            identifiers.insert(elem, my_index_i)
                            my_index_i += 1
                        value = identifiers.get_value_by_key(elem)
                        my_pif.add(elem, value)
                    elif elem[0] != '~':
                        errors.append((elem, general_index))
                general_index += 1
        ST1.write(str(constants))
        ST2.write(str(identifiers))
        PIF.write(str(my_pif))
        ERROR.write(str(errors))
        return len(errors)


def main():
    fileName = "p1.txt"
    ST1 = open("ST1.out", "w")
    ST1.write("HashTable was used to represent the SymbolTable\n")
    ST2 = open("ST2.out", "w")
    ST2.write("HashTable was used to represent the SymbolTable\n")
    PIF = open("PIF.out", "w")
    ERROR = open("ERROR.out", "w")
    general_index = 1
    E = Exec()
    flag = E.execute(fileName, ST1, ST2, PIF, ERROR, general_index)
    if flag == 0:
        print("Lexically correct")
    else:
        print("Lexical error found!")


# main()

print(check_constant('\'askegdfIW976435T129374BSDASDOIURFA9WER\''))