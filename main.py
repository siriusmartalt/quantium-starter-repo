import copy
import csv
import glob
import pandas

# dataframe = pandas.DataFrame.from_dict({
#     'sales': [],
#     'date': [],
#     'region': [],
# })

data = {
    'sales': [],
    'date': [],
    'region': [],
}

# files = glob.glob("./data/*.csv")

files = ["./data/daily_sales_data_0.csv", "./data/daily_sales_data_1.csv", "./data/daily_sales_data_2.csv"]

sales_of_day_default = {
    'east': 0,
    'west': 0,
    'north': 0,
    'south': 0,
}

for filename in files:
    date = None
    sales_of_day = copy.deepcopy(sales_of_day_default)

    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=',')

        # sales of one day
        

        for row in csv_reader:
            if date == None:
                date = row['date']
            elif date != row['date']:
                for key in sales_of_day:
                    # pandas.concat(dataframe, {
                    #     'sales': sales_of_day[key],
                    #     'date': date,
                    #     'region': key,
                    # })

                    data['sales'].append(sales_of_day[key])
                    data['date'].append(date)
                    data['region'].append(key)

                    date = row['date']
                sales_of_day = copy.deepcopy(sales_of_day_default)



            sales_of_day[row['region']] += int(row['quantity'])

    for key in sales_of_day:
        data['sales'].append(sales_of_day[key])
        data['date'].append(date)
        data['region'].append(key)

        date = row['date']
        sales_of_day = copy.deepcopy(sales_of_day_default)

dataframe = pandas.DataFrame.from_dict(data)


from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go

groups = dataframe.groupby(by='region')
data = []
colors=['red', 'blue', 'green', 'yellow']

# print(groups.get_group('south'))

for group, dataframe in groups:
    dataframe = dataframe.sort_values(by=['date'])
    trace = go.Scatter(x=dataframe.date.tolist(), 
                       y=dataframe.sales.tolist(),
                       marker=dict(color=colors[len(data)]),
                       name=group)
    data.append(trace)



app = Dash(__name__)

layout =  go.Layout(xaxis={'title': 'Time'},
                    yaxis={'title': 'Produced Units'},
                    margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                    hovermode='closest')

fig = go.Figure(data=data, layout=layout)  
app.layout = html.Div(style={}, children=[
    html.H1(
        children='Sales',
        style={
            'textAlign': 'center',
        }
    ),

    html.Div(children='A graph showing sales over time', style={
        'textAlign': 'center',
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

app.run_server(debug=True)
