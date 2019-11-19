import pypl
from random import normalvariate

css = '''
.line-plot {
  fill: none;
  stroke: black;
}
.axis {
  stroke: black;
}

.dot-plot-marker {
  stroke: white;
  fill: #edab88;
}

.ticklabel {
  stroke: none;
}

.xticklabel {
  text-anchor: middle;
  dominant-baseline: hanging;
}

.yticklabel {
  text-anchor: end;
  dominant-baseline: middle;
}
'''

npoints = 100
xv = [normalvariate(0, 1) for i in range(npoints)]
yv = [0.1*xv[i] + normalvariate(0, 1) for i in range(npoints)]

fig = pypl.Figure()
fig.append(pypl.InlineCss(css))
x = pypl.LinearAxis('x', [-3, -1, 1, 3], [100, 300], 300)
x.ticksize = 5
y = pypl.LinearAxis('y', [-3, -1, 1, 3], [300, 100], 100)
y.ticksize = -5
fig.append([x, y])
fig.append(pypl.Dots(x(xv), y(yv)))
print(fig.render(pretty=True))
