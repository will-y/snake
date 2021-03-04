class Node:

    def __init__(self, id, layer):
        self.id = id
        self.layer = layer
        self.connections = []
        self.weights = []
        self.inputs = []
        self.num_inputs = 0
        self.output = 0

    def add_connections(self, node_list):
        for node in node_list:
            self.connections.append(node)
            node.add_input()

    def add_input(self):
        self.num_inputs += 1

    def send_input(self, input):
        self.inputs.append(input)
        
        if self.num_inputs == len(self.inputs):
            self.output = 0
            for i in range(self.num_inputs):
                self.output += self.inputs[i] * self.weights[i]

            self.output = max(0, self.output)

            for node in self.connections:
                node.send_input(self.output)

            self.inputs = []

    def set_weights(self, weights):
        if len(weights) != self.num_inputs:
            raise Exception("Inputed weights don't match the number of inputs")
        self.weights = weights

    def get_weights(self):
        return self.weights

    def print_node(self):
        return "Node: {}, {}\nExpecting {} inputs\nGiving {} outputs\nConnections: {}".format(self.layer, self.id, self.num_inputs, len(self.connections), list(map(lambda node: (node.layer, node.id), self.connections)))