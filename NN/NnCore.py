import numpy as np


class NnCore:
    def __init__(self, learning_constant):
        self.learning_constant = learning_constant

    def learn(self, dataset, result_number):
        error = 0
        error_rate = 0
        for element in dataset:
            result = element.sigmoid_function(result_number)
            if round(result) != float(element.classification):
                error_rate += 1
            error += np.power(result - element.classification, 2)
            element.correction(self.learning_constant, result_number)
        error /= len(dataset)
        error_rate /= len(dataset)

        return error, (round(error_rate * 100, 2)).__str__() + '%'
