#!/usr/bin/env python
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls


tls.set_credentials_file(username='ashishjain1988', api_key='uyc6qh7frd')

x = ['E9.5 Male', 'E9.5 Female', 'E9.5 TGC', 'In Vitro TGC', 'E7.5 Whole', 'E9.5 Whole', 'E14.5 Whole', 'In Vitro TSC']
y = ['In Vitro TSC', 'E14.5 Whole','E9.5 Whole', 'E7.5 Whole', 'In Vitro TGC', 'E9.5 TGC', 'E9.5 Female', 'E9.5 Male']

#x = ['In Vivo Mouse E9.5', 'e9.5_TGC_male_3seq', 'e9.5_TGC_female_3seq']
#y = ['e9.5_TGC_female_3seq', 'e9.5_TGC_male_3seq', 'In Vivo Mouse E9.5']


#       x0    x1    x2    x3    x4
z = [[0.00, 0.00, 0.75, 0.75, 0.00,0.00,0.00,0.00],  # y0
     [0.00, 0.00, 0.75, 0.75, 0.00,0.00,0.00,0.00],  # y1
     [0.75, 0.75, 0.00, 0.75, 0.75,0.00,0.00,0.00],  # y2
     [0.00, 0.00, 0.00, 0.00, 0.00,0.00,0.00,0.00],
     [0.75, 0.75, 0.75, 0.00, 0.00,0.00,0.00,0.00],
     [0.75, 0.75, 0.00, 0.05, 0.75,0.00,0.00,0.00],
     [0.75, 0.00, 0.75, 0.75, 0.75,0.00,0.00,0.00],
     [0.00, 0.75, 0.75, 0.75, 0.75,0.00,0.00,0.00]]  # y3


z1 = [[173, 221, 0],  # y0
     [6, 0, 36],  # y1
     [0, 5, 13]]

annotations = []
for n, row in enumerate(z):
    for m, val in enumerate(row):
        var = z[n][m]
        annotations.append(
            dict(
                text=str(val),
                x=x[m], y=y[n],
                xref='x1', yref='y1',
                font=dict(color='black' if val > 0.5 else 'black'),
                showarrow=False)
            )

colorscale = [[0, '#ffffff'], [1, '#ffa500']]  # custom colorscale
trace = go.Heatmap(x=x, y=y, z=z, colorscale=colorscale, showscale=True)

fig = go.Figure(data=[trace])
fig['layout'].update(
    title="Placenta Genes Highly Expressed",
    annotations=annotations,
    xaxis=dict(ticks='outside', side='bottom',linecolor = 'black',showline=True,showgrid=True,gridwidth=2,gridcolor='#bdbdbd',
        tick0=0,
        dtick=1,
        ticklen=8,
        tickwidth=4,
        tickcolor='#000',tickfont=dict(
            size=10
        )),
    # ticksuffix is a workaround to add a bit of padding
    yaxis=dict(ticks='outside',ticksuffix='  ',linecolor = 'black',tick0=0,showline=True,showgrid=True,gridwidth=2,gridcolor='#bdbdbd',
        dtick=1,
        ticklen=8,
        tickwidth=4,
        tickcolor='#000',tickfont=dict(
            size=10
        )),              
    margin = dict(t=50,r=50,b=100,l=120),
    width=600,
    height=600,
    autosize=False
)
url = py.plot(fig, filename='Placenta Genes Highly Expr.', height=750,width=750)