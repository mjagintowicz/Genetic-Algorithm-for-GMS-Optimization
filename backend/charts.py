import matplotlib.pyplot as plt
import numpy as np

class Chart:
    def __init__(self, x, y, x_label, y_label, legend=None):
        if legend is not None and len(y) != len(legend):
            raise ValueError("y and legend must have same length")
        self.x = x
        self.y = y
        self.x_label = x_label
        self.y_label = y_label
        self.legend = legend

    def function_plot(self):
        fig, ax = plt.subplots()
        for i in range(len(self.y)):
            ax.plot(self.x, self.y[i], '.:', label=self.legend[i])
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.legend()

        return fig

    def schedule_plot(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.scatter(self.x, self.y[0], marker="x", s=80, linewidths=2,)

        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)

        ax.set_xticks(np.arange(1, len(self.x) + 1))
        ax.set_yticks(np.arange(1, max(self.y[0]) + 1))

        ax.grid(True, linestyle="--", alpha=0.25,)

        fig.tight_layout()

        return fig