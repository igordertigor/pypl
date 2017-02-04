
def lims2len(lims):
    return lims[1] - lims[0]


def prctiles(data, p=(0, .25, .5, .75, 1)):
    n = len(data)
    indices = (int((n-1)*p_) for p_ in sorted(p))
    return [data[i] for i in indices]
