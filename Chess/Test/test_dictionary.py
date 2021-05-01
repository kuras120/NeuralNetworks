import os
import sys
import time
import psutil
import unittest2


class DictionaryPerformanceTest(unittest2.TestCase):
    def test_performance_flat_dictionary(self):
        test_range = pow(370, 3)
        test_dict = {}
        for i in range(test_range):
            test_dict['key' + str(i)] = 1
        print('Size of dict: ', sys.getsizeof(test_dict))
        start = time.time()
        self.measurements(test_dict['key25000000'], 'Dict value of [key25000000]: ')
        stop = time.time()
        print('Time: ', stop - start, ' seconds')
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
                    test_dict['key' + str(i)]['key' + str(j)]['key' + str(k)] = 1
        print('Size of dict: ', sys.getsizeof(test_dict))
        start = time.time()
        self.measurements(test_dict['key160']['key200']['key180'], 'Dict value of [key160][key200][key180]: ')
        stop = time.time()
        print('Time: ', stop - start, ' seconds')
        self.assertEqual(len(test_dict.items()), test_range)
        self.assertEqual(len(test_dict['key0'].items()), test_range)
        self.assertEqual(len(test_dict['key0']['key0'].items()), test_range)
        del test_dict

    @staticmethod
    def measurements(dict_value, desc):
        print(desc, dict_value)
        process = psutil.Process(os.getpid())
        print('Weight: ', round(process.memory_info().rss / 1_073_741_824, 4), ' GB')
