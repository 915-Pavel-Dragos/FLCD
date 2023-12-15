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


x = FA("FA.in")
