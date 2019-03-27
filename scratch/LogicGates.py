import numpy as np


class Perceptron:
    def __init__(self, input_length, weights=None):
        if weights is None:
            self.weights = np.ones(input_length) * 0.5
        else:
            self.weights = weights

    @staticmethod
    def unit_step_function(x, func_name):
        if func_name == "AND":
            if x > 0.5:
                return 1
        elif func_name == "OR":
            if x == 0.5:
                return 1

        return 0

    def __call__(self, in_data, func):
        weighted_input = self.weights * in_data
        weighted_sum = weighted_input.sum()
        return Perceptron.unit_step_function(weighted_sum, func)


if __name__ == "__main__":
    name = "OR"
    p = Perceptron(2, np.array([0.5, 0.5]))
    for ar in [np.array([0, 0]), np.array([0, 1]), np.array([1, 0]), np.array([1, 1])]:
        y = p(np.array(ar), name)
        print(ar, y)
