from KNN.Chart import Chart
from collections import Counter
from KNN.KnnCore import KnnCore
from KNN.DataPreparation import DataPreparation


if __name__ == '__main__':

    # ************************ DATA INITIALIZATION ************************ #

    data_preparation = DataPreparation(100, None)
    learnset_data, learnset_labels = data_preparation.create_learn_data()
    testset_data, testset_labels = data_preparation.create_test_data()

    # ******************************* TESTS ******************************* #

    compatibility = Counter()
    print('Probki danych testowych na podstawie danych treningowych z glosowaniem: \n')
    for i in range(data_preparation.n_training_samples):
        neighbours = KnnCore.get_neighbours(learnset_data, learnset_labels, testset_data[i], 8, KnnCore.distance)
        print('{: >1} {: >3} {: >1} {: >50} {: >1} {: >1} {: >1} {: >1} {: >1} {: >1}'.format(
            'index: ', i, ', result of vote: ', KnnCore.vote_harmonic_weights(neighbours).__str__(), ', test label: ',
            testset_labels[i].__str__(), ', test data: ', testset_data[i].__str__(), ', compatibility: ',
            (KnnCore.vote(neighbours)[0] == testset_labels[i]).__str__()))

        compatibility[KnnCore.vote(neighbours)[0] == testset_labels[i]] += 1

    compatibility_percentage = compatibility[True] / sum(compatibility.values())
    print('Compatibility percentage is: ', compatibility_percentage * 100, '%')
    chart = Chart()
    chart.gather_data(testset_data, testset_labels)
    chart.create_plot().show()
