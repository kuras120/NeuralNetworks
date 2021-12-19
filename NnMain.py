from NN.test.TestRunner import TestRunner


if __name__ == '__main__':
    test_runner = TestRunner(125)
    for i in range(10):
        test_runner.run(i)
