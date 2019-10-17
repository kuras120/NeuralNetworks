from NN.NnCore import NnCore
from NN.Perceptron import DataCell, Perceptron
from KNN.DataPreparation import DataPreparation


if __name__ == '__main__':
    nn = NnCore(1.01)
    generator = DataPreparation(12)
    learn_data, learn_labels = generator.create_learn_data()
    neurons = []
    for i in range(len(learn_data)):
        neuron_data = []
        for j in range(len(learn_data[i])):
            cell = DataCell(learn_data[i][j], 1 if (j + 1) % 2 == 0 else -1)
            neuron_data.append(cell)
        neuron = Perceptron(neuron_data, DataCell(1, 0.5 if (i + 1) % 2 == 0 else -0.5), learn_labels[i])
        neurons.append(neuron)

    error = 1.0
    for i in range(3):
        error, error_rate = nn.learn(neurons, 3)
        print('Error: ', error, 'Error rate: ', error_rate)
