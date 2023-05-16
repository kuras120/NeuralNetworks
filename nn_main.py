<<<<<<< HEAD:NnMain.py
from KNN.DataPreparation import DataPreparation
from NN.test.TestRunner import TestRunner

if __name__ == '__main__':
    best_state = [[100, 100], [100, 100], [], []]
    for i in range(1):
        print('\n', i, '. TEST')
        # Max 149
        instance = TestRunner.run(125)
        if instance[1][0] <= best_state[1][0] and instance[1][1] <= best_state[1][1] and instance[0][0] <= best_state[0][0] and instance[0][1] <= best_state[0][1]:
            best_state = instance
    print('\n# ******************************* OVERALL ******************************* #')
    print('\nError: ', best_state[0][0], ' and test error: ', best_state[0][1])
    print('Learn error rate: ', str(best_state[1][0]) + '%', 'Test error rate: ', str(best_state[1][1]) + '%')
    print('Standard deviation: ', best_state[3][0], ' Test standard deviation: ', best_state[3][1])
    for layer in best_state[2]:
        for neuron in layer:
            print(neuron.weights)

    # generator = DataPreparation(1)
    # sample, label = generator.create_learn_data()
    # print(sample, ' ', label)
    # # 2.4% learn and 0.0% test errors
    # answer = TestRunner.test([
    #     [[-0.16054003225262045, 0.12987618846675392, 0.434970212244213, 0.42800033572919693, -0.759209842076767],
    #      [-0.20772030927202526, -0.19262830655182253, 0.404626179529902, 0.5838892976376451, 0.3573538113538165]],
    #     [[1.8600905236657033, 0.812496934316068, -2.55009706356018]]
    # ], sample)
    # print(answer)
=======
import copy
import time
from nn.nn_core import NnCore
from knn.data_preparation import DataPreparation


if __name__ == '__main__':

    # ************************ DATA INITIALIZATION ************************ #

    generator = DataPreparation(75, 20)
    learn_data, learn_labels = generator.create_learn_data()
    test_data, test_labels = generator.create_test_data()
    nn = NnCore(0.001, len(learn_data[0]))
    neuron_map = nn.create_network([2, 1])

    # ******************************* TESTS ******************************* #

    start_time = time.time()
    smallest_error = 1
    neuron_state = None
    smallest_sum_rates = [100, 100]
    error_sum_rates = 1
    neuron_best_rate = None
    while smallest_error > 0.16 and time.time() - start_time < 30:
        error, error_rate, output_neuron = nn.learn_and_test(neuron_map, learn_data, learn_labels, 3, True)
        if error < smallest_error:
            smallest_error = error
            neuron_state = copy.deepcopy(output_neuron)
            print('Error: ', error, 'Error rate: ', str(error_rate) + '%')
            test_error, test_error_rate, test_output_neuron = nn.learn_and_test(neuron_map, test_data, test_labels, 3)
            test_result = [test_error_rate, error_rate]
            if sum(test_result) <= sum(smallest_sum_rates):
                smallest_sum_rates = test_result
                error_sum_rates = error
                neuron_best_rate = copy.deepcopy(output_neuron)

            print('Test error rate: ', test_result[0], '%')

    print('\nBest neuron state with error: ', smallest_error)
    print('Weights: ', neuron_state.weights)

    print('\nBest neuron state for test with error: ', error_sum_rates)
    print('Test rate: ', smallest_sum_rates[0].__str__() + '%', 'Learn rate: ', smallest_sum_rates[1].__str__() + '%')
    print('Weights: ', neuron_best_rate.weights)
>>>>>>> tictactoe:nn_main.py
