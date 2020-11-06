
import pandas as pd
import sys

# use this file for any functions used multiple times in different notebooks

def create_inf_dict(year):
    # create a dictionary with inflation conversion factors

    # Read in the inflation data
    inf_data = pd.read_csv("../DataSet/1995Inflation.csv")

    # Select the conversion factor from the data frame using .loc
    d2019 = inf_data.loc[inf_data['year'] == year,'amount'].item()

    # Apply the factor to all rows (to get from 1995 factor to 2019 factor)
    inf_data['2019_factor']=inf_data['amount']/d2019

    # Store the factors in a dictionary for easy use in a function
    inf_dict_2019 = dict(zip(inf_data['year'], inf_data['2019_factor']))

    return inf_dict_2019

def inflation_adjust(df): 
    # adjust GDP inflation for this specific case only

    # get the inflation dictionary
    inf_data = create_inf_dict(2019)

    df['inf-adjusted'] = round(df['GDP']/df['current dollars'].map(inf_data))
    
    return df

# work in progress
# def inflation_adjust_set(year):
    # given a year of data (column or row of data), adjust an entire set of data for the given year

    # get the inflation dictionary
    # inf_data = create_inf_dict('2019')
#    inf_data = {'2000':1.2,'3000':3}

#    a = inf_data[year.name]

#    return a


# ---------------------------------------
# reserve for funciton building

# 2019 dollars

# need to convert one number to inflation adj number

# earlier years should increase, 2019 dollars should stay the same

# seperate function for creating the dictionary

# apply accross rows instead (year)


# df = pd.DataFrame

# d = {'2000': [1.0,2.3,3.4,5.6]}
# df = pd.DataFrame(data=d)

# print(inflation_adjust_set(df))
