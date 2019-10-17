import numpy as np
from sklearn import datasets


class DataPreparation:
    def __init__(self, training_samples, random_seed=None):
        iris = datasets.load_iris()
        self.iris_data = iris.data
        self.iris_labels = iris.target
        if random_seed:
            np.random.seed(random_seed)
        self.indices = np.random.permutation(len(self.iris_data))
        self.n_training_samples = training_samples

    def create_learn_data(self):
        learnset_data = self.iris_data[self.indices[:-self.n_training_samples]]
        learnset_labels = self.iris_labels[self.indices[:-self.n_training_samples]]
        return learnset_data, learnset_labels

    def create_test_data(self):
        testset_data = self.iris_data[self.indices[-self.n_training_samples:]]
        testset_labels = self.iris_labels[self.indices[-self.n_training_samples:]]
        return testset_data, testset_labels
