import numpy as np
from NN.Perceptron import Perceptron


class NnCore:
    def __init__(self, learning_constant):
        self.learning_constant = learning_constant
        self.input_length = 4  # for iris
        self.result_number = 3  # for iris

    def learn(self, neuron_map, data, labels, correction=False):
        error = 0
        error_rate = 0
        standard_deviation = 0
        errors = []
        for i in range(len(data)):
            local_data = data[i]
            for layer in neuron_map:
                output_data = []
                for neuron in layer:
                    neuron.set_data(local_data, labels[i])
                    if neuron == neuron_map[-1][-1]:
                        result = neuron.sigmoid_function(self.result_number)
                        if round(result) != labels[i]:
                            error_rate += 1
                        error += np.abs(result - labels[i])
                        errors.append(np.abs(result - labels[i]))
                    else:
                        result = neuron.relu_function()
                    output_data.append(result)
                    if correction:
                        neuron.correction(result, self.learning_constant)
                local_data = output_data
        error /= len(data)
        error_rate /= len(data)
        for err in errors:
            standard_deviation += np.power(err - error, 2)
        standard_deviation = np.sqrt(standard_deviation / (len(data) - 1))
        return neuron_map, error, round(error_rate * 100, 2), standard_deviation

    def test(self, neuron_map, data):
        for i in range(len(data)):
            local_data = data[i]
            for layer in neuron_map:
                output_data = []
                for neuron in layer:
                    neuron.set_data(local_data)
                    if neuron == neuron_map[-1][-1]:
                        return round(neuron.sigmoid_function(self.result_number))
                    else:
                        result = neuron.relu_function()
                    output_data.append(result)
                local_data = output_data

    def create_network(self, neuron_map, weights=None):
        network = []
        length = self.input_length
        for i in range(len(neuron_map)):
            column = []
            for j in range(neuron_map[i]):
                if weights:
                    perceptron = Perceptron(length, 1.0, weights[i][j])
                else:
                    perceptron = Perceptron(length, 1.0)
                column.append(perceptron)
            length = neuron_map[i]
            network.append(column)
        return network
