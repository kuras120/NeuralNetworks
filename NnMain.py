from KNN.DataPreparation import DataPreparation
from NN.test.TestRunner import TestRunner

if __name__ == '__main__':
    # best_state = [[100, 100], [100, 100], [], []]
    # for i in range(100):
    #     print('\n', i, '. TEST')
    #     # Max 149
    #     instance = TestRunner.run(125)
    #     if instance[1][0] <= best_state[1][0] and instance[1][1] <= best_state[1][1] and instance[0][0] <= best_state[0][0] and instance[0][1] <= best_state[0][1]:
    #         best_state = instance
    # print('\n# ******************************* OVERALL ******************************* #')
    # print('\nError: ', best_state[0][0], ' and test error: ', best_state[0][1])
    # print('Learn error rate: ', str(best_state[1][0]) + '%', 'Test error rate: ', str(best_state[1][1]) + '%')
    # print('Standard deviation: ', best_state[3][0], ' Test standard deviation: ', best_state[3][1])
    # for layer in best_state[2]:
    #     for neuron in layer:
    #         print(neuron.weights)

    generator = DataPreparation(1)
    sample, label = generator.create_learn_data()
    print(sample, ' ', label)
    # 2.4% learn and 0.0% test errors
    answer = TestRunner.test([
        [[-0.16054003225262045, 0.12987618846675392, 0.434970212244213, 0.42800033572919693, -0.759209842076767],
         [-0.20772030927202526, -0.19262830655182253, 0.404626179529902, 0.5838892976376451, 0.3573538113538165]],
        [[1.8600905236657033, 0.812496934316068, -2.55009706356018]]
    ], sample)
    print(answer)
