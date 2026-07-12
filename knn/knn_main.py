from knn.chart import Chart
from collections import Counter
from knn.knn_core import KnnCore
from knn.data_preparation import DataPreparation


if __name__ == '__main__':

    # ************************ DATA INITIALIZATION ************************ #

    data_preparation = DataPreparation(50, None)
    learnset_data, learnset_labels = data_preparation.create_learn_data()
    testset_data, testset_labels = data_preparation.create_test_data()
    print(len(learnset_data))
    print(len(testset_data))


    # ******************************* TESTS ******************************* #

    compatibility = Counter()
    print('Probki danych testowych na podstawie danych treningowych z glosowaniem: \n')
    for i in range(data_preparation.n_training_samples):
        neighbours = KnnCore.get_neighbours(learnset_data, learnset_labels, testset_data[i], 8, KnnCore.distance)
        print('{: >1} {: >3} {: >1} {: >50} {: >1} {: >1} {: >1} {: >1} {: >1} {: >1}'.format(
            'index: ', i, ', result of vote: ', str(KnnCore.vote_harmonic_weights(neighbours)),
            ', test label: ', str(testset_labels[i]), ', test data: ', str(testset_data[i]),
            ', compatibility: ', (KnnCore.vote(neighbours)[0] == str(testset_labels[i]))
        ))
        compatibility[KnnCore.vote(neighbours)[0] == testset_labels[i]] += 1
    compatibility_percentage = compatibility[True] / sum(compatibility.values())
    print('Compatibility percentage is: ', compatibility_percentage * 100, '%')
    chart = Chart()
    chart.gather_data(testset_data, testset_labels)
    chart.create_plot().show()
