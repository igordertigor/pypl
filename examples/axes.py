import pypl

css = '''
.line-plot {
  fill: none;
  stroke: black;
}
.axis {
  stroke: black;
}
'''

fig = pypl.Figure()
fig.append(pypl.InlineCss(css))
x = pypl.LinearAxis('x', [0, 1, 2], [400, 100], 100)
x.ticksize = 20
fig.append(x)
print(fig.render(pretty=True))
