import numpy as np
from nn.perceptron import Perceptron


class NnCore:
    def __init__(self, learning_constant, input_length):
        self.learning_constant = learning_constant
        self.input_length = input_length

    def learn_and_test(self, neuron_map, data, labels, result_number, correction=False):
        error = 0
        error_rate = 0
        for i in range(len(data)):
            local_data = data[i]
            for layer in neuron_map:
                output_data = []
                for neuron in layer:
                    neuron.set_data(local_data, labels[i])
                    result = neuron.sigmoid_function(result_number)
                    output_data.append(result)
                    if round(result) != float(labels[i]):
                        error_rate += 1
                    error += np.power(result - labels[i], 2)
                    if correction:
                        neuron.correction(result, self.learning_constant)
                local_data = output_data

        error /= len(data)
        error_rate /= len(data)

        return error, (round(error_rate * 100, 2)), neuron_map[-1][-1]

    def create_network(self, neuron_map):
        network = []
        length = self.input_length
        for layer in neuron_map:
            column = []
            for _ in range(layer):
                column.append(Perceptron(length, 1.0))
            length = layer
            network.append(column)

        return network
