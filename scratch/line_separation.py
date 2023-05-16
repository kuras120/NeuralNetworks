import numpy as np
from collections import Counter
from matplotlib import pyplot as plt


class Perceptron:
    def __init__(self, input_length, weights=None):
        if weights is None:
            self.weights = np.random.random(input_length) * 2 - 1
        else:
            self.weights = weights

        self.learning_rate = 0.1

    def print_weights(self):
        print(self.weights)

    @staticmethod
    def unit_step_function(x):
        if x < 0:
            return 0
        return 1

    def __call__(self, in_data):
        weighted_input = self.weights * in_data
        weighted_sum = weighted_input.sum()
        return Perceptron.unit_step_function(weighted_sum)

    def adjust(self, target_result, calculated_result, in_data):
        error = target_result - calculated_result
        for i in range(len(in_data)):
            correction = error * in_data[i] * self.learning_rate
            self.weights[i] += correction


def above_line(point, line_func):
    x, y = point
    if y > line_func(x):
        return 1
    else:
        return 0


def lin1(x):
    return x + 4


if __name__ == "__main__":
    points = np.random.randint(1, 100, (500, 2))
    p = Perceptron(2)
    p.print_weights()
    for point_t in points:
        p.adjust(above_line(point_t, lin1), p(point_t), point_t)
    evaluation = Counter()
    p.print_weights()
    for point_t in points:
        if p(point_t) == above_line(point_t, lin1):
            evaluation["correct"] += 1
        else:
            evaluation["wrong"] += 1
    print(evaluation.most_common())

    cls = [[], []]
    for point_t in points:
        cls[above_line(point_t, lin1)].append(tuple(point_t))
    colours = ("r", "b")
    for k in range(2):
        X, Y = zip(*cls[k])
        plt.scatter(X, Y, c=colours[k])

    X = np.arange(-3, 103)

    m = -p.weights[0] / p.weights[1]
    print(m)
    plt.plot(X, m * X, label="ANN line")
    # plt.plot(X, lin1(X), label="line1")
    plt.legend()
    plt.show()
