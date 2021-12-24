import copy
import time
from NN.NnCore import NnCore
from KNN.DataPreparation import DataPreparation


class TestRunner:
    @staticmethod
    def test(weights, sample):
        nn = NnCore(0.001)
        neuron_map = nn.create_network([2, 1], weights)
        return nn.test(neuron_map, sample)

    @staticmethod
    def run(samples_number, r_seed=None):
        # ************************ DATA INITIALIZATION ************************ #

        generator = DataPreparation(samples_number, r_seed)
        learn_data, learn_labels = generator.create_learn_data()
        test_data, test_labels = generator.create_test_data()

        nn = NnCore(0.001)
        neuron_map = nn.create_network([2, 1])

        # ******************************* TESTS ******************************* #

        start_time = time.time()

        # LEARN AND TEST
        errors = [1, 1, 1]
        std_devs = [1, 1, 1]
        rates = [100, 100]

        # BEST
        best_errors = [1, 1]
        best_std_devs = [1, 1]
        best_rates = [100, 100]
        neuron_best_state = None

        while errors[0] > 0.05 and time.time() - start_time < 30:
            output, error, error_rate, std_dev = nn.learn(neuron_map, learn_data, learn_labels, True)
            if error < errors[0]:
                errors[0] = error
                std_devs[0] = std_dev
                neuron_learn_state = copy.deepcopy(output)
                # print('Error: ', error, 'Error rate: ', error_rate.__str__() + '%')
                output_test, error_test, error_test_rate, std_test_dev = nn.learn(neuron_map, test_data, test_labels)
                rates = [error_rate, error_test_rate]
                errors[1] = error_test
                std_devs[1] = std_test_dev
                if error_test < errors[2]:
                    errors[2] = error_test
                    std_devs[2] = std_test_dev
                    if sum(rates) < sum(best_rates):
                        best_errors[0] = errors[0]
                        best_errors[1] = errors[2]
                        best_rates = rates
                        best_std_devs[0] = std_devs[0]
                        best_std_devs[1] = std_devs[2]
                        neuron_best_state = copy.deepcopy(neuron_learn_state)

        print('\n# ******************************* SEED: ' + str(r_seed) + ' ******************************* #')
        print('\nNeuron state with error: ', errors[0], ' and test error: ', errors[1])
        print('Learn error rate: ', str(rates[0]) + '%', 'Test error rate: ', str(rates[1]) + '%')
        print('Standard deviation: ', std_devs[0], ' Test standard deviation: ', std_devs[1])

        print('\nNeuron state for best with error: ', best_errors[0], ' and test error: ', best_errors[1])
        print('Learn error rate: ', str(best_rates[0]) + '%', 'Test error rate: ', str(best_rates[1]) + '%')
        print('Standard deviation: ', best_std_devs[0], ' Test standard deviation: ', best_std_devs[1])
        return [best_errors, best_rates, neuron_best_state, best_std_devs]
