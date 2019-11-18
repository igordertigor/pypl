from itertools import cycle
from logging import Logger

logger = Logger('pypl')


def render(obj, tag, text):
    if isinstance(obj, (list, tuple)):
        obj = Group(*obj)
    return obj.render(tag, text)


class GraphElement(object):
    """Base class for any graphical elements. Do not use directly"""

    id_ = None
    """String holding css id"""

    class_ = None
    """String or list of strings holding css class names"""

    def render(self, tag, text):
        raise NotImplementedError

    def init_kwargs(self, custom_data):
        """Create basic keyword arguments for the respective tag

        This typically will populate the keys: id and klass from self.id_ and
        self.class_.

        Arguments:
            custom_data:
                dictionary with additional values. Note that these are string
                appended!

        Returns:
            kwargs
        """
        kwargs = {}
        if self.id_ is not None:
            kwargs['id'] = self.id_
        if self.class_ is not None:
            kwargs['klass'] = (self.class_
                               if isinstance(self.class_, str)
                               else ' '.join(self.class_))

        for key, value in custom_data.items():
            if key in kwargs:
                kwargs[key] = ' '.join([value, kwargs[key]])
            else:
                kwargs[key] = value

        return kwargs


class Group(GraphElement):

    def __init__(self, *objects, id_=None, class_=None):
        self.id_ = id_
        self.class_ = class_
        self.objects = objects

    def render(self, tag, text):
        kwargs = self.init_kwargs()
        with tag('g', **kwargs):
            for obj in self.objects:
                render(obj, tag, text)


class InlineCss(GraphElement):

    def __init__(self, css):
        """Add style information through css string"""
        self.css = css

    def render(self, tag, text):
        with tag('style'):
            text('\n'.join([
                '/* <![CDATA[ */',
                self.css,
                '/* ]]> */']))


class ExternalCss(GraphElement):

    def __init__(self, fname):
        """Link external css file"""
        logger.warn('Using external css is currently not working reliably')
        self.fname = fname

    def render(self, tag, text):
        with tag('style'):
            text('@import url({})'.format(self.fname))


class XY(GraphElement):

    def __init__(self, x, y, id_=None, class_=None):
        self.x = x
        self.y = y
        self.id_ = id_
        self.class_ = class_


class Line(XY):

    def __init__(self, x, y, id_=None, class_=None):
        """Draw a line

        Arguments:
            x, y:
                sequences of x and y coordinates
            id_:
                css id for selection
            class_:
                string or list of string holding css classes
        """
        super(Line, self).__init__(x, y, id_, class_)

    def render(self, tag, text):
        """Render object through given tag closure"""
        kwargs = self.init_kwargs({'klass': 'line-plot'})
        with tag('polyline',
                 points=' '.join(['{},{}'.format(x, y)
                                  for x, y in zip(self.x, self.y)]),
                 **kwargs
                 ):
            pass


class Dots(XY):

    def __init__(self, x, y, r=3, id_=None, class_=None):
        """Draw a collection of dots (all the same color)

        Arguments:
            x, y:
                sequences of x and y coordinates
            r:
                radius of each dot. This can be a scalar (all the same) or a
                sequence (one size per point)
            id_:
                css id for selection
            class_:
                string or list of string holding css classes
        """
        super(Dots, self).__init__(x, y, id_)
        if isinstance(r, (int, float)):
            self.r = [r]
        else:
            self.r = r

    def render(self, tag, text):
        """Render object through given tag closure"""
        kwargs = self.init_kwargs({'klass': 'dot-plot'})
        with tag('g', **kwargs):
            for x, y, r in zip(self.x, self.y, cycle(self.r)):
                with tag('circle',
                         cx=x,
                         cy=y,
                         r=r,
                         klass=self.init_kwargs({'klass': 'dot-plot-marker'})):
                    pass
