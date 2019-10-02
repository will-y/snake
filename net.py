from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense
import sys
from custom_network import Network

class NeuralNetwork:

    def __init__(self, input_shape, action_space, custom = False):
        if not custom:
            self.model = Sequential()
            self.model.add(Dense(12, activation="relu", input_dim=input_shape))
            self.model.add(Dense(12))
            self.model.add(Dense(action_space))
            self.model.compile(loss="mean_squared_error",
                            optimizer=RMSprop(lr=0.00025,
                                                rho=0.95,
                                                epsilon=0.01),
                            metrics=["accuracy"])
            self.model.summary()
        else:
            self.model = Network(input_shape)
            self.model.add_layer(12)
            self.model.add_layer(12)
            self.model.add_layer(action_space)
            self.model.compile()
            self.model.print_network()