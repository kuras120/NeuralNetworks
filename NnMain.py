import copy
from NN.NnCore import NnCore
from NN.Perceptron import Perceptron
from KNN.DataPreparation import DataPreparation


if __name__ == '__main__':
    nn = NnCore(1.1)
    generator = DataPreparation(100)
    learn_data, learn_labels = generator.create_learn_data()
    neuron = Perceptron(len(learn_data[0]), 1)

    smallest_error = 1
    neuron_state = None
    for _ in range(1000):
        error, error_rate = nn.learn(neuron, learn_data, learn_labels, 3)
        if error < smallest_error:
            smallest_error = error
            neuron_state = copy.deepcopy(neuron)

        print('Error: ', error, 'Error rate: ', error_rate)

    print("Best neuron state with error: ", smallest_error)
    print("Weights: ", neuron_state.weights)

    print("Test data")
    test_data, test_labels = generator.create_test_data()
    neuron_state.set_data(test_data[0])
    result = neuron_state.sigmoid_function(3)
    print("Result: ", round(result), "Label: ", float(test_labels[0]))
