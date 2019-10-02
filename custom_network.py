from node import Node
from display import NetworkDisplay
import random

class Network:

    def __init__(self, inputs):
        self.layers = []
        self.inputs = inputs
        self.compiled = False
        self.add_layer(inputs, True)

    def add_layer(self, num_nodes, first_layer = False):
        if not self.compiled:
            layer = []

            # add new nodes to the new layer
            for i in range(num_nodes):
                temp = Node(i, len(self.layers))
                layer.append(temp)

                if first_layer:
                    temp.add_input()

            if len(self.layers) != 0:
                # not first layer, need to connect the previous layer to this one
                for node in self.layers[-1]:
                    node.add_connections(layer)
                
            self.layers.append(layer)
        else:
            raise Exception("Cannot add layers to a compiled network")

    def get_weights(self):
        weights = []
        for i in range(len(self.layers)):
            weights.append(list(map(lambda node: node.get_weights(), self.layers[i])))
        return weights

    def set_weights(self, weights):
        for i in range(len(self.layers)):
            for j in range(len(self.layers[i])):
                self.layers[i][j].set_weights(weights[i][j])

    def __set_initial_weights(self):
        for list_of_nodes in self.layers:
            for node in list_of_nodes:
                node_weights = []
                for i in range(node.num_inputs):
                    #node_weights.append(random.gauss(0, 1))
                    node_weights.append(random.random())
                node.set_weights(node_weights)

    def compile(self):
        self.compiled = True
        self.__set_initial_weights()

    
    def predict(self, inputs):
        if len(inputs) != self.inputs:
            raise Exception("Invalid inputs for the network")
        else:
            for i in range(self.inputs):
                self.layers[0][i].send_input(inputs[i])

            output = []

            for node in self.layers[-1]:
                output.append(node.output)

            return output

    def print_network(self):
        for i in range(len(self.layers)):
            print("Layer {}: -----------------------\n".format(i))
            for node in self.layers[i]:
                print(node.print_node())
                print("\n")

    def display_network(self):
        NetworkDisplay(self)