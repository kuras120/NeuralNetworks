import copy
import numpy as np
from NN.Perceptron import Perceptron


class NnCore:
    def __init__(self, learning_constant):
        self.learning_constant = learning_constant

    def learn(self, neuron_map, data, labels, result_number):
        error = 0
        error_rate = 0
        mapped_neurons = []
        for i in range(len(data)):
            local_data = data[i]
            for layer in neuron_map:
                temp_data = []
                for j in range(layer):
                    neuron = Perceptron(len(local_data), 1.0)
                    mapped_neurons.append(neuron)
                    neuron.set_data(local_data, labels[i])
                    result = neuron.sigmoid_function(result_number)
                    temp_data.append(result)
                    if layer == 1:
                        if round(result) != float(labels[i]):
                            error_rate += 1
                        error += np.power(result - labels[i], 2)
                    neuron.correction(result, self.learning_constant)
                local_data = temp_data

        error /= len(data)
        error_rate /= len(data)

        return error, (round(error_rate * 100, 2)), mapped_neurons
