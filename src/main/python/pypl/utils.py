import itertools


def lims2len(lims):
    return lims[1] - lims[0]


def all_elements(plot):
    return list(itertools.chain(*[val for val in plot.values()]))
