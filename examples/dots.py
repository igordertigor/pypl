import pypl

css = '''
.dot-plot {
  fill: black;
  stroke: none;
}
'''

fig = pypl.Figure()
fig.append(pypl.InlineCss(css))
# fig.append(pypl.ExternalCss('style.css'))
fig.append(pypl.Dots([10, 40, 100], [20, 300, 50], id_='mydots'))
print(fig.render(pretty=True))
