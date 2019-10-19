import numpy as np
import random


class Perceptron:
    def __init__(self, data_length, bias):
        self.weights = []
        for _ in range(data_length + 1):
            self.weights.append(random.uniform(-1, 1))
        self.bias = bias
        self.data_input = None
        self.classification = None

    def set_data(self, data_input, classification=None):
        self.data_input = data_input
        self.classification = classification

    def sum(self):
        weighted_sum = 0
        for i in range(len(self.data_input)):
            weighted_sum += self.data_input[i] * self.weights[i]

        weighted_sum += self.bias * self.weights[-1]

        return weighted_sum

    def sigmoid_function(self, result_number):
        return (result_number - 1) / (1 + np.power(np.e, -self.sum()))

    def correction(self, output, learning_constant):
        for i in range(len(self.data_input)):
            self.weights[i] += learning_constant * (self.classification - output) * self.data_input[i]

        self.weights[-1] += learning_constant * (self.classification - output)
