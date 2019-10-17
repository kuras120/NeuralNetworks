import numpy as np


class DataCell:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def weighted_value(self):
        return self.value * self.weight


class Perceptron:
    def __init__(self, data_input, bias=None, classification=None):
        self.data_input = data_input
        self.bias = bias
        self.classification = classification

    def sum(self):
        weighted_sum = 0
        for element in self.data_input:
            weighted_sum += element.weighted_value()

        if self.bias:
            weighted_sum += self.bias.weighted_value()

        return weighted_sum

    def sigmoid_function(self, result_number):
        return (result_number - 1) / (1 + np.power(np.e, -self.sum()))

    def correction(self, learning_constant, result_number):
        output = self.sigmoid_function(result_number)
        for element in self.data_input:
            element.weight = learning_constant * (self.classification - output) * element.value

            # print("Class: ", float(self.classification), "Out: ", output, "result: ", float(self.classification) == round(output),
            #       "Weight: ", element.weight)
