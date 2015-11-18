#!/usr/bin/env python
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls


tls.set_credentials_file(username='ashishjain1988', api_key='uyc6qh7frd')

x = ['E9.5 Male', 'E9.5 Female', 'E9.5 TGC', 'In Vitro TGC', 'E7.5 Whole', 'E9.5 Whole', 'E14.5 Whole', 'In Vitro TSC']
y = ['In Vitro TSC', 'E14.5 Whole','E9.5 Whole', 'E7.5 Whole', 'In Vitro TGC', 'E9.5 TGC', 'E9.5 Female', 'E9.5 Male']

#       x0    x1    x2    x3    x4
z = [[0.00, 0.00, 0.75, 0.75, 0.00,0.00,0.00,0.00],  # y0
     [0.00, 0.00, 0.75, 0.75, 0.00,0.00,0.00,0.00],  # y1
     [0.75, 0.75, 0.00, 0.75, 0.75,0.00,0.00,0.00],  # y2
     [0.00, 0.00, 0.00, 0.00, 0.00,0.00,0.00,0.00],
     [0.75, 0.75, 0.75, 0.00, 0.00,0.00,0.00,0.00],
     [0.75, 0.75, 0.00, 0.05, 0.75,0.00,0.00,0.00],
     [0.75, 0.00, 0.75, 0.75, 0.75,0.00,0.00,0.00],
     [0.00, 0.75, 0.75, 0.75, 0.75,0.00,0.00,0.00]]  # y3

annotations = []
for n, row in enumerate(z):
    for m, val in enumerate(row):
        var = z[n][m]
        annotations.append(
            dict(
                text=str(val),
                x=x[m], y=y[n],
                xref='x1', yref='y1',
                font=dict(color='white' if val > 0.5 else 'black'),
                showarrow=False)
            )

colorscale = [[0, '#3D9970'], [1, '#001f3f']]  # custom colorscale
trace = go.Heatmap(x=x, y=y, z=z, colorscale=colorscale, showscale=False)

fig = go.Figure(data=[trace])
fig['layout'].update(
    title="Annotated Heatmap",
    annotations=annotations,
    xaxis=dict(ticks='', side='top'),
    # ticksuffix is a workaround to add a bit of padding
    yaxis=dict(ticks='', ticksuffix='  '),
    width=700,
    height=700,
    autosize=False
)
url = py.plot(fig, filename='Annotated Heatmap', height=750)