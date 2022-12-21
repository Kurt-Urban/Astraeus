import matplotlib.pyplot as plt
import IPython

plt.ion()


def plot(scores, mean_scores):
    IPython.display.clear_output(wait=True)
    IPython.display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
