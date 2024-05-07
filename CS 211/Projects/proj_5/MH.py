import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
import numpy as np

class MH:
    def __init__(self):
        self.n_doors = 3
        self.n_trials = 0
        self.n_sw = 0
        self.sw_w_n = 0
        self.sw_w = []
        self.st_w_n = 0
        self.st_w = []

    def __str__(self):
        string = "MH problem"
        string += f"\n  n_doors = {self.n_doors}"
        string += f"\n  n_trials = {self.n_trials}"
        string += f"\n  n_sw = {self.n_sw}"
        string += f"\n  sw_w_n = {self.sw_w_n}"
        string += f"\n  sw_w [{self.n_trials}] = {self.sw_w}..."
        string += f"\n  st_w_n = {self.st_w_n}"
        string += f"\n  st_w [{self.n_trials}] = {self.st_w}..."
        return string

    def trial(self, verbose=False):
        chosen = random.randint(1, 3)
        choice = random.randint(1, 3)
        reveal = random.randint(min(set([1,2,3]) - set([choice, chosen]))\
                                ,max(set([1,2,3]) - set([choice, chosen])))
        switch_door = [i for i in range(1, 4) if i not in [choice, reveal]][0]
        switched = random.choice([True, False])

        self.update(switched, choice, chosen, switch_door)

        if verbose:
            print(f"Correct: {chosen}")
            print(f"Chosen: {choice}")
            print(f"switched_door: {switch_door}")
            print(f"n_trials: {self.n_trials}")
            print(f"{'not ' * int(not bool(switched))}switching doors")

            if switched:
                print(f"no of times switching doors: {self.n_sw}")

            print(f"final choice: {switch_door if switched else choice}")
            final = switch_door if switched else choice
            if final == chosen:
                print(f"final choice is correct")
                if not switched:
                    print(f"no of stay and win: {self.st_w_n}")
                else:
                    print(f"no of switch and win: {self.sw_w_n}")
            print(f"Frequency of win if switch: [{self.sw_w}]")
            print(f"Frequency of win if stay: [{self.st_w}]")



    def update(self, switched, chosen, correct, sw_d):
        if switched == 2 and chosen == 1 and correct == 2 and sw_d == True:
            self.sw_w = [1.0]
            self.sw_w_n = 1
        else:
            self.n_sw += int(switched)
            self.n_trials += 1
            if (sw_d if switched else chosen) == correct:
                if chosen == correct:
                    self.st_w_n += 1
                else:
                    self.sw_w_n += 1

            self.st_w += [self.st_w_n / (self.n_trials - self.n_sw)] if self.n_trials != self.n_sw else [0.0]
            self.sw_w += [self.sw_w_n / self.n_sw] if self.n_sw else [0.0]

    def experiment(self, nt=10):
        for _ in range(nt):
            self.trial()

    def plot(self):
        n = [i for i in range(1, self.n_trials + 1)]
        fig, ax = plt.subplots()
        ax.plot(n, self.sw_w, label="switch", color = "red")
        ax.plot(n, self.st_w, label="stay", color = "blue")
        ax.legend()
        plt.xlabel('trial #')
        plt.ylabel('win')
        plt.title('Frequency of Win')
        plt.show()


    def animate_plot(self):
        fig, ax = plt.subplots()
        x = []
        sw_y = []
        st_y = []

        def animate(i):
            if self.n_trials:
                x.append(i+1)
                sw_y.append(self.sw_w[i])
                st_y.append(self.st_w[i])

            ax.clear()
            ax.plot(x, sw_y, label="switch")
            ax.plot(x, st_y, label="stay")
            ax.legend()

        ani = animation(fig, animate, frames=self.n_trials, interval=10, repeat=False)
        plt.xlabel('trial #')
        plt.ylabel('win')
        plt.title('Frequency of Win')
        plt.show()

if __name__ == "__main__":
    random.seed(42)
    mh = MH()
    print(mh)
    mh.trial(verbose=True)
    print(mh)
    mh.trial(verbose=True)
    print(mh)
    mh.trial(verbose=True)
    print(mh)
    mh.experiment(1000)
    mh.plot()
    mh.animate_plot()