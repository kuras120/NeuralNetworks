import matplotlib.pyplot as plt


class Chart:
    def __init__(self, colors=("r", "g", "y")):
        self.data = []
        self.colors = colors

    def gather_data(self, set_data, set_labels):
        for iclass in range(3):
            self.data.append([[], [], []])
            for i in range(len(set_data)):
                if set_labels[i] == iclass:
                    self.data[iclass][0].append(set_data[i][0])
                    self.data[iclass][1].append(set_data[i][1])
                    self.data[iclass][2].append(sum(set_data[i][2:]))

        return self.data

    def create_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for iclass in range(3):
            ax.scatter(self.data[iclass][0], self.data[iclass][1], self.data[iclass][2], c=self.colors[iclass])

        return plt


