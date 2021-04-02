import sys


class Process:
    def __init__(self):
        self.__length = int(sys.argv[1])
        temp = sys.argv[2:-2]
        self.__array = [temp[i:i + self.__length] for i in range(0, len(temp), self.__length)]
        self.__points = sys.argv[-2:]

    def values(self):
        print('Macierz stanu:')
        for elem in self.__array:
            print('     ', elem)
        print('Punkty:')
        print('     Gracz: ' + self.__points[0])
        print('     AI: ' + self.__points[1])


if __name__ == '__main__':
    process = Process()
    process.values()
