from yattag import Doc, indent
from .graph_elements import render

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
