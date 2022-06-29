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

sales = pandas.DataFrame.from_dict(data)

salesE=sales[sales['region']=='east'][['date','sales']]
salesN=sales[sales['region']=='north'][['date','sales']]
salesW=sales[sales['region']=='west'][['date','sales']]
salesS=sales[sales['region']=='south'][['date','sales']]

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

data = []



app = Dash(__name__)



fig = px.line(sales, x="date", y="sales")
app.head = [html.Link(rel='stylesheet', href='./styles.css')]
app.layout = html.Div(style={
  'color': '#acc5db',
  'background-color': '#202225',
    }, children=[
    html.H1(
        children='Sales',
        style={
            'textAlign': 'center',
        }
    ),

    # html.Div(children='Dash: A web application framework for your data.', style={
    #     'textAlign': 'center',
    # }),

    dcc.Graph(
        id='graph',
        figure=fig
    ),

    html.Div([
        dcc.RadioItems(['east', 'west','north', 'south'], 'east', id='my-input') 
    ]),

    html.Div(id='my-output'),
])

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    match input_value:
        case 'east':
            return px.line(salesE, x="date", y="sales")
        case 'west':
            return px.line(salesW, x="date", y="sales")
        case 'north':
            return px.line(salesN, x="date", y="sales")
        case 'south':
            return px.line(salesS, x="date", y="sales")


app.run_server(debug=True)
