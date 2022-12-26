import numpy as np
from collections import Counter


class KnnCore:
    @staticmethod
    def distance(instance1, instance2):
        instance1 = np.array(instance1)
        instance2 = np.array(instance2)

        return np.linalg.norm(instance1 - instance2)

    @staticmethod
    def get_neighbours(training_set, labels, test_instance, k, distance):
        distances = []
        for index in range(len(training_set)):
            dist = distance(test_instance, training_set[index])
            distances.append((training_set[index], dist, labels[index]))

        distances.sort(key=lambda x: x[1])

        return distances[:k]

    @staticmethod
    def vote(neighbours):
        class_counter = Counter()
        for neighbour in neighbours:
            class_counter[neighbour[2]] += 1

        percentage = class_counter.most_common(1)[0][1] / sum(class_counter.values())
        return class_counter.most_common(1)[0][0], (percentage * 100).__str__() + '%'

    @staticmethod
    def vote_harmonic_weights(neighbours, all_results=True):
        class_counter = Counter()
        number_of_neighbours = len(neighbours)
        for index in range(number_of_neighbours):
            class_counter[neighbours[index][2]] += 1 / (index + 1)
        labels, votes = zip(*class_counter.most_common())
        # print(labels, votes)
        winner = class_counter.most_common(1)[0][0]
        votes_for_winner = class_counter.most_common(1)[0][1]
        if all_results:
            total = sum(class_counter.values(), 0.0)
            for key in class_counter:
                class_counter[key] /= total
                class_counter[key] *= 100
                class_counter[key] = round(class_counter[key], 2).__str__() + '%'
            return winner, class_counter.most_common()
        else:
            return winner, votes_for_winner / sum(votes)
