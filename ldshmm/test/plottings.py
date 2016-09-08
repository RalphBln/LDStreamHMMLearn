import matplotlib.pyplot as plt
import numpy as np


def plot_result_heatmap(data_naive, data_bayes, x_labels, y_labels, y_axis_name, type, heading):
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.pcolor(data_naive, cmap="Reds")
    plt.title(heading)
    plt.xticks(np.arange(3), (str(x_label) for x_label in x_labels))
    plt.yticks(np.arange(3), (str(y_label) for y_label in y_labels))
    plt.xlabel("taumeta")
    plt.ylabel(y_axis_name)
    plt.title("Naive " + type)
    plt.colorbar()
    plt.tight_layout(2)

    plt.subplot(1, 2, 2)
    plt.pcolor(data_bayes, cmap="Reds")
    plt.title("Bayes " + type)
    plt.xticks(np.arange(3), (str(x_label) for x_label in x_labels))
    plt.yticks(np.arange(3), (str(y_label) for y_label in y_labels))
    plt.xlabel("taumeta")
    plt.ylabel(y_axis_name)
    plt.colorbar()
    plt.tight_layout(2)

    plt.savefig(heading + ".png")


def plot_result(y_axis1_list, y_axis2_list, type, heading):
    """Plotting function for diagram with two y axes

    Parameters
        ----------
        y_axis1_list : list of elements for first y axis
        y_axis2_list : list of elements for second y axis
        type : string which characterizes the type of calculation (for instance "naive" or "bayes").
        heading : The custom headiPerformanceng for the plot title

        The two latter ones are just for plotting and saving the resulting plot. The filename will be type+ _ +heading
        """
    t_time = range(0, len(y_axis1_list))

    fig, ax1 = plt.subplots()
    ax1.plot(t_time, y_axis1_list, 'b-')
    ax1.set_xlabel('time t')
    ax1.set_ylabel('performance time')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    ax2 = ax1.twinx()

    t_time = range(0, len(y_axis2_list))
    ax2.plot(t_time, y_axis2_list, 'r.')
    ax2.set_ylabel('error')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.title(heading)
    plt.savefig(type + '_' + heading + '.png')