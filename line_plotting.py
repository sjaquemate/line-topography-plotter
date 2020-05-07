import numpy as np

def get_segments(x, y, z):
    assert len(x)==len(y)==len(z)
    points = np.array([x, y, z]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

def plot_segment_2d(ax, segment, segment_width, segment_color, z_fraction, alpha=1):
    l_i, = ax.plot(segment[:, 0], segment[:, 1]+z_fraction*segment[:, 2], linewidth=segment_width, c=segment_color, alpha=alpha)
    l_i.set_solid_capstyle('round')

def plot_line_2d(ax, x, y, z, linewidths, linecolors, z_fraction):
    segments = get_segments(x, y, z)
    for i in range(len(segments)):
        plot_segment_2d(ax, segments[i], linewidths[i], linecolors[i], z_fraction)
