import numpy as np


class NnCore:
    def __init__(self, learning_constant):
        self.learning_constant = learning_constant

    def learn(self, neuron, data, labels, result_number):
        error = 0
        error_rate = 0
        for i in range(len(data)):
            neuron.set_data(data[i], labels[i])
            result = neuron.sigmoid_function(result_number)
            if round(result) != float(labels[i]):
                error_rate += 1
            error += np.power(result - labels[i], 2)
            neuron.correction(result, self.learning_constant)
        error /= len(data)
        error_rate /= len(data)

        return error, (round(error_rate * 100, 2)).__str__() + '%'
