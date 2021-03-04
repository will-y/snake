from custom_network import Network


class NeuralNetwork:

    def __init__(self, input_shape, action_space):
        self.model = Network(input_shape)
        self.model.add_layer(12)
        self.model.add_layer(12)
        self.model.add_layer(action_space)
        self.model.compile()
        self.model.print_network()
