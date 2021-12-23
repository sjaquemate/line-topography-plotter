import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patheffects as path_effects
# todo: find better map from here and preprocess it -
# todo: https://www.shadedrelief.com/natural3/pages/extra.html


def make_segments(x, y):
    """
        >> make_segments([1,2,3], [10, 20, 30])
        >> [[(1, 10), (2, 20)], [(2, 20), (3, 30)]] """
    return [[(x1, y1), (x2, y2)] for x1, y1, x2, y2 in zip(x[:-1], y[:-1], x[1:], y[1:])]


def load_tiff(filepath) -> np.ndarray:
    return np.array(tiff.imread(filepath), dtype=np.float)


def generate_horizontal_lines(shape, num_lines, sampling_steps: int = 1):
    height, width = shape
    range_x = np.arange(0, width, sampling_steps)
    range_y = np.linspace(0, height-1, num_lines, dtype=int)
    for y in range_y:
        yield range_x, [y]*len(range_x)


if __name__ == "__main__":

    worldmap = load_tiff('worldmap_(576, 1728).tiff')
    worldmap[worldmap < -5] = np.nan  # water
    highest_value = np.nanmax(worldmap)

    # create grid
    num_hor_lines = 50
    z_fraction = 0.01
    sampling_steps = 5
    cmap = plt.get_cmap('binary_r')
    min_cmap_value, max_cmap_value = 0.1, 1
    min_width, max_width = 0.3, 0.2

    print('generating plot data')

    plot = {'segments': [], 'widths': [], 'colors': []}
    for line_x, line_y in generate_horizontal_lines(worldmap.shape, num_hor_lines, sampling_steps):

        line_z = worldmap[line_y, line_x]
        line_y -= line_z * z_fraction

        colors = [cmap(min_cmap_value + (max_cmap_value - min_cmap_value ) * value / highest_value)
                  for value in line_z]
        widths = [min_width + (max_width-min_width) * value / highest_value for value in line_z]

        plot['segments'] += make_segments(line_x, line_y)
        plot['widths'] += widths[:-1]
        plot['colors'] += colors[:-1]

    print('adding plot data to figure')
    fig, ax = plt.subplots()
    fig.set_facecolor('black')
    ax.set_aspect('equal')
    ax.set_xlim(0, worldmap.shape[1])
    ax.set_ylim(worldmap.shape[0], 0)
    ax.set_axis_off()

    line_segments = LineCollection(plot['segments'], linewidths=plot['widths'],
                                   colors=plot['colors'], linestyle='solid',
                                   path_effects=[path_effects.Stroke(capstyle='round')])
    ax.add_collection(line_segments)

    print('saving highres plot')
    fig.savefig('output_highres.png', bbox_inches='tight', dpi=1000)
