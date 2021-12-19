import copy
import time
from NN.NnCore import NnCore
from KNN.DataPreparation import DataPreparation


class TestRunner:
    def __init__(self, learn_samples):
        # 150 samples of iris
        # rest will be test samples
        self.__learn_samples = learn_samples
        self.__parameters_number = 4  # for iris

    def run(self, r_seed):
        # ************************ DATA INITIALIZATION ************************ #

        generator = DataPreparation(self.__learn_samples, r_seed)
        learn_data, learn_labels = generator.create_learn_data()
        test_data, test_labels = generator.create_test_data()

        nn = NnCore(0.001, self.__parameters_number)
        neuron_map = nn.create_network([2, 1])

        # ******************************* TESTS ******************************* #

        start_time = time.time()
        smallest_error = 1
        neuron_state = None
        smallest_sum_rates = [100, 100]
        error_sum_rates = 1
        neuron_best_rate = None
        while smallest_error > 0.05 and time.time() - start_time < 30:
            error, error_rate, output_neuron = nn.learn_and_test(neuron_map, learn_data, learn_labels, 3, True)
            if error < smallest_error:
                smallest_error = error
                neuron_state = copy.deepcopy(output_neuron)
                # print('Error: ', error, 'Error rate: ', error_rate.__str__() + '%')
                test_error, test_error_rate, test_output_neuron = nn.learn_and_test(neuron_map, test_data, test_labels, 3)
                test_result = [test_error_rate, error_rate]
                if sum(test_result) <= sum(smallest_sum_rates):
                    smallest_sum_rates = test_result
                    error_sum_rates = error
                    neuron_best_rate = copy.deepcopy(output_neuron)
                # print('Test error rate: ', test_result[0], '%')

        print('\n# ******************************* SEED: ' + str(r_seed) + ' ******************************* #')
        print('\nBest neuron state with error: ', smallest_error)
        print('Weights: ', neuron_state.weights)

        print('\nBest neuron state for test with error: ', error_sum_rates)
        print('Test rate: ', smallest_sum_rates[0].__str__() + '%', 'Learn rate: ', smallest_sum_rates[1].__str__() + '%')
        print('Weights: ', neuron_best_rate.weights)
        return neuron_state.weights, neuron_best_rate.weights
