import svgwrite


def lims2len(lims):
    return lims[1] - lims[0]


def get_parent(parent):
    if parent is None:
        return svgwrite.Drawing()
    else:
        return parent
