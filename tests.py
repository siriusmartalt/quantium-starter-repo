def get_app():
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
            id='header',
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
            dcc.RadioItems(options = ['east', 'west','north', 'south'], value='east'),
        ],id='options'),
    
        html.Div(id='my-output'),
    ])

    return app

import dash
from dash import html

def test_dima001_title(dash_duo):
    app = get_app()
    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal('#header', 'Sales', timeout=4)


    assert dash_duo.find_element('#header').text == 'Sales'

def test_dima002_options(dash_duo):
    app = get_app()
    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal('#header', 'Sales', timeout=4)

    assert dash_duo.find_element('#options').text == 'eastwestnorthsouth'

def test_dima003_no_error(dash_duo):
    app = get_app()
    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal('#header', 'Sales', timeout=4)

    assert dash_duo.get_logs() == [], "browser console should contain no error"
