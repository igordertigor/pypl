import functools
import operator
import svgwrite

from . import utils


def vaxis(scl, nticks=5, x=0, parent=None, kw={}, axis_spec={}, tick_spec={}):
    parent = utils.get_parent(parent)

    kw = set_general_defaults(kw, scl)

    return makeaxis(
        parent, 'vertical', scl, nticks, x, axis_spec, tick_spec, kw)


def haxis(scl, nticks=5, y=0, parent=None, kw={}, axis_spec={}, tick_spec={}):
    parent = utils.get_parent(parent)

    kw = set_general_defaults(kw, scl)

    return makeaxis(
        parent, 'horizontal', scl, nticks, y, axis_spec, tick_spec, kw)


def set_general_defaults(general_spec, scl):
    d = {
        'tick_size': scl(0) - scl(.01*scl.data_len),
        'ticklabelformat': '{:.2f}'
    }
    d.update(general_spec)
    return d


def get_ticks(scl, nticks):
    raw_ticks = [scl.data_0 + scl.data_len*loc/(nticks-1)
                 for loc in range(nticks)]
    return [scl(loc) for loc in raw_ticks], raw_ticks


def makeaxis(parent, direction, scl, nticks, loc, ax_spec, tick_spec,
             general_spec):
    ts = general_spec['tick_size']
    ticklabelformat = general_spec['ticklabelformat']
    ticks, raw_ticks = get_ticks(scl, nticks)

    if direction == 'vertical':
        axpoint = partialpoint(x=loc)
        ticpoints = functools.partial(hpoints, locations=[loc, loc+ts])
        tick_labl_loc = partialpoint(x=loc+2*ts)
        label_loc = partialpoint(x=loc+5*ts)
    else:
        axpoint = partialpoint(y=loc)
        ticpoints = functools.partial(vpoints, locations=[loc, loc+ts])
        tick_labl_loc = partialpoint(y=loc+2*ts)
        label_loc = partialpoint(y=loc+5*ts)

    parent.add(svgwrite.shapes.Line(axpoint(min(ticks)),
                                    axpoint(max(ticks)),
                                    **ax_spec))
    if 'label' in general_spec:
        mticks = functools.reduce(operator.add, ticks)/len(ticks)
        parent.add(svgwrite.text.Text(general_spec['label'],
                                      label_loc(mticks)))

    for tick, raw_tick in zip(ticks, raw_ticks):
        parent.add(svgwrite.shapes.Line(*ticpoints(tick), **tick_spec))
        parent.add(svgwrite.text.Text(ticklabelformat.format(raw_tick),
                                      insert=tick_labl_loc(tick)))

    return parent


def hpoints(vpos, locations):
    return [(loc, vpos) for loc in locations]


def vpoints(hpos, locations):
    return [(hpos, loc) for loc in locations]


def partialpoint(x=None, y=None):

    if x is None and y is not None:

        def mkpoint(other):
            return (other, y)

    elif x is not None and y is None:

        def mkpoint(other):
            return (x, other)

    else:

        mkpoint = partialpoint

    return mkpoint
