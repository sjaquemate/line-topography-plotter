import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
from scipy import interpolate
import line_plotting

if __name__ == "__main__":

    #import tiff map to numpy array
    dir = 'C:/__whatever_your_directory_is__'
    map = tiff.imread(dir + 'worldmap_(576, 1728).tiff')
    map = np.array(map, dtype=float)
    print('map.shape=', map.shape)

    if False: #plot map
        plt.imshow(map)
        plt.show(block=True)

    map = map[::-1, :] # reverse y axis

    # create grid
    n_lines = 200
    n_points = 1700 # number of data points
    n_int_points = 1700
    x = np.linspace(0, map.shape[1]-1, n_points, dtype=int)
    y_values = np.linspace(0, map.shape[0]-1, n_lines, dtype=int)

    highest_value = np.max(map)
    print('highest_value=', highest_value)
    # create figure
    cmap = plt.get_cmap('binary')
    fig, ax = plt.subplots()
    fig.set_facecolor((1.0, 1.0, 1.0))
    ax.set_aspect('equal')
    ax.set_xlim(0, map.shape[1])
    ax.set_ylim(0, map.shape[0]*1.3) #add a bit to allow for mountains to flow over the figure
    ax.set_axis_off()

    # draw each individual line
    y_values_test = y_values[len(y_values)//3:len(y_values)//3+10]

    for y_value in y_values:
        print('drawing line at y_value=', y_value)

        # get z data from map
        line = np.array(np.ones(n_points)*y_value, dtype=int)
        z = map[line, x]

        # set all values smaller than -30000 to 0
        remove_values = z < -30000
        z[remove_values] = 0

        smoothen = True
        # interpolate to n_int_points
        if smoothen:
            tck = interpolate.splrep(x, z, s=30000000, k=1)
            x_int = np.linspace(min(x), max(x), n_int_points)
            z_int = interpolate.splev(x_int, tck)
            y_int = np.array(np.ones(n_int_points)*y_value, dtype=int)
            # set all nans again (resized)
            z_int[[remove_values[int(n_points * i / n_int_points)] for i in range(n_int_points)]] = np.nan
        else:
            x_int, y_int, z_int = x, line, z
            # set all nans again
            z_int[remove_values] = np.nan

        # set dynamics colors and widths
        colors = [cmap(0.15+0.85*value/highest_value) if not np.isnan(value) else cmap(0) for value in z_int]
        widths = [0.1 + 0.2*value / highest_value for value in z_int]

        line_plotting.plot_line_2d(ax, x_int, y_int, z_int, z_fraction=0.003, linewidths=widths, linecolors=colors)

    save = True
    if save:
        print('saving svg')
        plt.savefig("graph.svg")
        print('saving png')
        plt.savefig('plot.png', dpi=5000)
    plt.show()
