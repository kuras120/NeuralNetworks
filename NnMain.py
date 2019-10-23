import copy
import time
from NN.NnCore import NnCore
from NN.Perceptron import Perceptron
from KNN.DataPreparation import DataPreparation


if __name__ == '__main__':

    # ************************ DATA INITIALIZATION ************************ #

    nn = NnCore(0.15)
    generator = DataPreparation(75)
    learn_data, learn_labels = generator.create_learn_data()
    test_data, test_labels = generator.create_test_data()
    neuron = Perceptron(len(learn_data[0]), 1.0)

    # ******************************* TESTS ******************************* #

    start_time = time.time()
    smallest_error = 1
    neuron_state = None
    smallest_sum_rates = [100, 100]
    error_sum_rates = 1
    neuron_best_rate = None
    while smallest_error > 0.1 and time.time() - start_time < 30:
        error, error_rate = nn.learn(neuron, learn_data, learn_labels, 3)
        if error < smallest_error:
            smallest_error = error
            neuron_state = copy.deepcopy(neuron)
            print('Error: ', error, 'Error rate: ', error_rate.__str__() + "%")
            temp_error_rate = 0
            for i in range(len(test_data)):
                neuron_state.set_data(test_data[i])
                result = neuron_state.sigmoid_function(3)
                if round(result) != float(test_labels[i]):
                    temp_error_rate += 1

            temp_rate = [round((temp_error_rate / len(test_data)) * 100, 2), error_rate]
            if sum(temp_rate) <= sum(smallest_sum_rates):
                smallest_sum_rates = temp_rate
                error_sum_rates = error
                neuron_best_rate = copy.deepcopy(neuron)

            print("Test error rate: ", temp_rate[0], "%")

    print("\nBest neuron state with error: ", smallest_error)
    print("Weights: ", neuron_state.weights)

    print("\nBest neuron state for test with error: ", error_sum_rates)
    print("Test rate: ", smallest_sum_rates[0].__str__() + "%", "Learn rate: ", smallest_sum_rates[1].__str__() + "%")
    print("Weights: ", neuron_best_rate.weights)
