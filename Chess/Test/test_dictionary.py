import os
import time
import psutil
import unittest2


class DictionaryPerformanceTest(unittest2.TestCase):
    def test_performance_flat_dictionary(self):
        test_range = 50_000_000
        test_dict = {}
        for i in range(test_range):
            test_dict['key' + str(i)] = i
        self.measurements(test_dict['key25000000'], 'Dict value of [key25000000]: ')
        self.assertEqual(len(test_dict.items()), test_range)
        del test_dict

    def test_performance_extended_dictionary(self):
        test_range = 370
        test_dict = {}
        for i in range(test_range):
            test_dict['key' + str(i)] = {}
            for j in range(test_range):
                test_dict['key' + str(i)]['key' + str(j)] = {}
                for k in range(test_range):
                    test_dict['key' + str(i)]['key' + str(j)]['key' + str(k)] = i + j + k
        self.measurements(test_dict['key160']['key200']['key180'], 'Dict value of [key160][key200][key180]: ')
        self.assertEqual(len(test_dict.items()), test_range)
        del test_dict

    @staticmethod
    def measurements(dict_value, desc):
        start = time.time()
        print(desc, dict_value)
        stop = time.time()
        print('Time: ', stop - start, ' seconds')
        process = psutil.Process(os.getpid())
        print('Weight: ', round(process.memory_info().rss / 1_073_741_824, 2), ' GB')
