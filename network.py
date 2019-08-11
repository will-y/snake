from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense


class NeuralNetwork:

    def __init__(self, input_shape, action_space):
        self.model = Sequential()
        self.model.add(Dense(64, activation="relu", input_shape=input_shape))
        self.model.add(Dense(32))
        self.model.add(Flatten())
        self.model.add(Dense(action_space))
        self.model.compile(loss="mean_squared_error",
                           optimizer=RMSprop(lr=0.00025,
                                             rho=0.95,
                                             epsilon=0.01),
                           metrics=["accuracy"])
        self.model.summary()