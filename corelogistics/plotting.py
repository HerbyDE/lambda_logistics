from plotly import offline as ofpy, graph_objs as gro


def barchart(x_data, y_data, name):
    x = x_data
    y = y_data
    plot1 = gro.Bar(x=x, y=y, name=name, marker=dict(color='rgba(255,0,0,0.8)'))
    input = gro.Data([plot1])
    design = gro.Layout(xaxis=dict(tickangle=-45))
    fig = gro.Figure(data=input, layout=design)
    div1 = ofpy.plot(fig, auto_open=False, output_type='div', show_link=False)

    return div1


def linegraph(x_data, y1, y2, y3, y4, y5):
    x = x_data
    y1 = y1
    y2 = y2
    y3 = y3
    y4 = y4
    y5 = y5

    trace1 = gro.Scatter(x=x, y=y1, mode='lines+markers', name='Total Parcels')
    trace2 = gro.Scatter(x=x, y=y2, mode='lines+markers', name='Parcels Created')
    trace3 = gro.Scatter(x=x, y=y3, mode='lines+markers', name='Parcels Fetched')
    trace4 = gro.Scatter(x=x, y=y4, mode='lines+markers', name='Parcels In Hub')
    trace5 = gro.Scatter(x=x, y=y5, mode='lines+markers', name='Parcels In Transit')

    input = gro.Data([trace1, trace2, trace3, trace4, trace5])
    design = gro.Layout(xaxis={'title': 'Time'}, yaxis={'title': 'Sum of Parcels'})
    fig = gro.Figure(data=input, layout=design)
    div = ofpy.plot(fig, auto_open=False, output_type='div', show_link=False)
    return div

def pie_chart(d1, d2, d3, d4, d5, d6, l1, l2, l3, l4, l5, l6, d7, d8, l7, l8):
    fig = {
        'data': [
            {
                'values': [d1, d2, d3, d4, d5, d6],
                'labels': [l1, l2, l3, l4, l5, l6],
                'domain': {'x': [0, .5], 'y': [0, 1]},
                'name': 'Weight',
                'hoverinfo': 'label+percent',
                'hole': .5,
                'type': 'pie'
            },
            {
                'values': [d7, d8],
                'labels': [l7, l8],
                'domain': {'x': [.52, 1], 'y': [0, 1]},
                'name': 'Distance',
                'hoverinfo': 'label+percent',
                'hole': .5,
                'type': 'pie'
            }
        ],
        'layout': {
            'title': 'Parcel Statistics',
            'annotations': [
                {
                    'font': {'size': 15},
                    'showarrow': False,
                    'text': 'Distance',
                    'x': 0.20,
                    'y': 0.5,
                },
                {
                    'font': {'size': 15},
                    'showarrow': False,
                    'text': 'Weight',
                            'x': 0.8,
                            'y': 0.5,
                }
            ]
        }
    }
    div = ofpy.plot(fig, auto_open=False, output_type='div', show_link=False)
    return div

def linegraph_warehouse(x, y, y_title):
    trace1 = gro.Scatter(x=x, y=y, mode='lines+markers', name='Total Parcels')
    input = gro.Data([trace1])
    design = gro.Layout(xaxis={'title': 'Time'}, yaxis={'title': y_title}, width=550, height=450)
    fig = gro.Figure(data=input, layout=design)
    div = ofpy.plot(fig, auto_open=False, output_type='div', show_link=False)
    return div

def barchart_warehouse(x_data, y_data, name):
    x = x_data
    y = y_data
    plot1 = gro.Bar(x=x, y=y, name=name, marker=dict(color='rgba(255,0,0,0.8)'))
    input = gro.Data([plot1])
    design = gro.Layout(xaxis=dict(tickangle=-45), width=550, height=450)
    fig = gro.Figure(data=input, layout=design)
    div1 = ofpy.plot(fig, auto_open=False, output_type='div', show_link=False)

    return div1