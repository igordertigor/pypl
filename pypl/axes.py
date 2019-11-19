from .graph_elements import GraphElement
from .scales import linear_scale


class Axis(GraphElement):

    def __init__(self, orientation, rng_in, rng_out, loc,
                 id_=None, class_=None):
        self.rng_in = rng_in
        self.rng_out = rng_out
        self.loc = loc
        self.orientation = orientation
        self.id_ = id_
        self.class_ = class_

    def __call__(self, vals):
        """Scale values to axis"""
        return self.scale(vals)


class LinearAxis(Axis):

    def __init__(self, orientation, tics, rng, loc,
                 id_=None, class_=None, **kwargs):
        """Create a linear axis

        Arguments:
            orientation (str):
                Orientation of the axis (horizontal/x or vertical/y)
            tics (sequence):
                data tics
            rng (sequence):
                range of svg-positions this should span
            loc (float):
                location of axis.

        Other arguments:
            ticksize:
                Size of ticks (svg units) [Default: 2]
            tickfmt:
                Format string for tick labels [Default: '{:.2f}']
        """
        super(LinearAxis, self).__init__(
            orientation,
            [tics[0], tics[-1]],
            rng,
            loc,
            id_=id_,
            class_=class_
        )

        self.tics = tics
        self.scaler = linear_scale(self.rng_in, self.rng_out)

        self.ticksize = kwargs.setdefault('ticksize', 2)
        self.tickfmt = kwargs.setdefault('tickfmt', '{:.2f}')

    def scale(self, vals):
        return [self.scaler(val) for val in vals]

    def render(self, tag, text):
        if self.orientation.lower() in ['x', 'horizontal']:
            axargs = {'x1': self.rng_out[0], 'x2': self.rng_out[1],
                      'y1': self.loc, 'y2': self.loc}
            ticargs = {'y1': self.loc, 'y2': self.loc + self.ticksize,
                       'klass': 'xtick tick'}
            ticpos, off = 'x', 'y'
        elif self.orientation.lower() in ['y', 'vertical']:
            axargs = {'x1': self.loc, 'x2': self.loc,
                      'y1': self.rng_out[0], 'y2': self.rng_out[1]}
            ticargs = {'x1': self.loc, 'x2': self.loc + self.ticksize,
                       'klass': 'ytick tick'}
            ticpos, off = 'y', 'x'
        with tag('g', **self.init_kwargs({'klass': '{} axis'.format(ticpos)})):
            with tag('line', **self.init_kwargs(dict(klass='axis-line',
                                                     **axargs))):
                pass
            for ticval, ticloc in zip(self.tics, self.scale(self.tics)):
                ticargs.update({ticpos+'1': ticloc, ticpos+'2': ticloc})
                with tag('line', **self.init_kwargs(ticargs)):
                    pass
                with tag('text',
                         **self.init_kwargs({
                             ticpos: ticloc,
                             off: self.loc + 2*self.ticksize,
                             'klass': 'ticklabel {}ticklabel'.format(ticpos)
                         })):
                    text(self.tickfmt.format(ticval))
