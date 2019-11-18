from yattag import Doc, indent
from itertools import cycle
from logging import Logger

logger = Logger('pypl')


class Figure(object):

    def __init__(self, width=600, height=400, **kwargs):
        """Figure class

        This is basically a container for all GraphElements

        Arguments:
            width:
                width of the svg element
            height:
                height of the svg element
            kwargs:
                other keyword arguments are passed to the svg tag when
                rendering
        """
        self.width = width
        self.height = height
        self.objects = []

    def append(self, *objects):
        """Append one or more objects to the figure"""
        self.objects += objects

    def render(self, fname=None, pretty=False):
        """Render figure

        Arguments:
            fname:
                write rendered figure to given filename. By default, no file is
                written.
            pretty:
                indent output to be editable by a human

        Returns:
            svg string
        """
        doc, tag, _ = Doc().tagtext()
        text = doc.asis
        with tag('svg', width=self.width, height=self.height):
            for obj in self.objects:
                render(obj, tag, text)

        svg = doc.getvalue()
        if pretty:
            svg = indent(svg)

        if fname is not None:
            with open(fname, 'w') as f:
                f.write(svg)
        return svg


def render(obj, tag, text):
    if isinstance(obj, (list, tuple)):
        obj = Group(*obj)
    return obj.render(tag, text)


class GraphElement(object):
    """Base class for any graphical elements. Do not use directly"""

    name = str
    """Name of svg element"""

    def render(self, tag, text):
        raise NotImplementedError


class Group(GraphElement):

    def __init__(self, *objects, id_=None, class_=None):
        self.id_ = id_
        self.class_ = class_
        self.objects = objects

    def render(self, tag, text):
        kwargs = {}
        if self.id_:
            kwargs['id'] = self.id_
        if self.class_:
            kwargs['klass'] = self.class_
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

    def __init__(self, x, y, id_=None):
        self.x = x
        self.y = y
        self.id_ = id_


class Line(XY):

    def __init__(self, x, y, id_=None):
        """Draw a line

        Arguments:
            x, y:
                sequences of x and y coordinates
            id_:
                css id for selection
        """
        super(Line, self).__init__(x, y, id_)

    def render(self, tag, text):
        """Render object through given tag closure"""
        kwargs = {'klass': 'line-plot'}
        if self.id_:
            kwargs['id'] = self.id_
        with tag('polyline',
                 points=' '.join(['{},{}'.format(x, y)
                                  for x, y in zip(self.x, self.y)]),
                 **kwargs
                 ):
            pass


class Dots(XY):

    def __init__(self, x, y, r=3, id_=None):
        """Draw a collection of dots (all the same color)

        Arguments:
            x, y:
                sequences of x and y coordinates
            r:
                radius of each dot. This can be a scalar (all the same) or a
                sequence (one size per point)
            id_:
                css id for selection
        """
        super(Dots, self).__init__(x, y, id_)
        if isinstance(r, (int, float)):
            self.r = [r]
        else:
            self.r = r

    def render(self, tag, text):
        """Render object through given tag closure"""
        kwargs = {'klass': 'dot-plot'}
        if self.id_:
            kwargs['id'] = self.id_
        with tag('g', **kwargs):
            for x, y, r in zip(self.x, self.y, cycle(self.r)):
                with tag('circle',
                         cx=x,
                         cy=y,
                         r=r,
                         klass='dot-plot-marker'):
                    pass
