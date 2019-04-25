import numpy as np

def get_changed_tiles_sync(old_data, new_data, x_count, w):
    diff = new_data - old_data
    print(diff.sum().sum())
    diff = np.absolute(diff).sum(-1)
    I, J = diff.shape

    x = []
    y = []
    for i in range(I):
        for j in range(J):
            if diff[i, j] != 0:
                x.append(i)
                y.append(j)

    x = np.array(x)
    y = np.array(y)
    x = x // w
    y = y // w
    tiles = x + (y * x_count)

    tiles = set(tiles)
    return tiles
