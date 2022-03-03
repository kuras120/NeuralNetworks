import numpy as np
from matplotlib import pyplot as plt
from itertools import chain
from collections import Counter
from scratch.line_separation import Perceptron


class1 = [(3, 4), (4.2, 5.3), (4, 3), (6, 5), (4, 6), (3.7, 5.8),
          (3.2, 4.6), (5.2, 5.9), (5, 4), (7, 4), (3, 7), (4.3, 4.3)]
class2 = [(-3, -4), (-2, -3.5), (-1, -6), (-3, -4.3), (-4, -5.6),
          (-3.2, -4.8), (-2.3, -4.3), (-2.7, -2.6), (-1.5, -3.6),
          (-3.6, -5.6), (-4.5, -4.6), (-3.7, -5.8)]

p = Perceptron(2)


def lin1(x_t):
    return x_t + 4


for point in class1:
    p.adjust(1,
             p(point),
             point)
for point in class2:
    p.adjust(0,
             p(point),
             point)

evaluation = Counter()
for point in chain(class1, class2):
    if p(point) == 1:
        evaluation["above"] += 1
    else:
        evaluation["under"] += 1

test_points = [(3.9, 6.9), (-2.9, -5.9)]
for point in test_points:
    print(p(point))

print(evaluation.most_common())

X, Y = zip(*class1)
plt.scatter(X, Y, c="r")
X, Y = zip(*class2)
plt.scatter(X, Y, c="b")
x = np.arange(-7, 10)
y = 5*x + 10
m = -p.weights[0] / p.weights[1]
plt.plot(x, m*x)
plt.show()
