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

files = glob.glob("./data/*.csv")

sales_of_day_default = {
    'east': 0,
    'west': 0,
    'north': 0,
    'south': 0,
}

for filename in files:
    date = None
    sales_of_day = sales_of_day_default

    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=',')

        line_count = 1
        
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

    data['sales'].append(sales_of_day[key])
    data['date'].append(date)
    data['region'].append(key)

    date = row['date']
    sales_of_day = copy.deepcopy(sales_of_day_default)

dataframe = pandas.DataFrame.from_dict(data)

f = open("task_1_output.txt", "w")
f.write(dataframe.to_string())
f.close()
