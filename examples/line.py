import pypl

css = '''
.line-plot {
  fill: none;
  stroke: black;
}
'''

fig = pypl.Figure()
fig.append(pypl.InlineCss(css))
# fig.append(pypl.ExternalCss('style.css'))
fig.append(pypl.Line([10, 40, 100], [20, 300, 50],
                     id_='myline',
                     class_='condition1'))
print(fig.render(pretty=True))
