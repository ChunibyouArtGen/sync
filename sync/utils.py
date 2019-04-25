import numpy as np
def get_changed_tiles(old_data, new_data, params):
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
    x = x // params["w"]
    y = y // params["w"]
    tiles = x + (y * params["x_count"])

    tiles = set(tiles)
    return tiles
