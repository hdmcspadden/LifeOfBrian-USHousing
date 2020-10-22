
import pandas as pd
import sys

# use this file for any functions used multiple times in different notebooks

def inflation_adjust(df): 
    # adjust GDP inflation for this specific case only

    # Read in the inflation data
    inf_data = pd.read_csv("../dataset/1995inflation.csv")

    # Select the conversion factor from the data frame using .loc
    d2019 = inf_data.loc[inf_data['year'] == 2019,'amount'].item()

    # Apply the factor to all rows
    inf_data['2019_factor']=inf_data['amount']/d2019
    inf_data.head()

    # Store the factors in a dictionary for easy use in a function
    inf_dict_2019 = dict(zip(inf_data['year'], inf_data['2019_factor']))

    df['inf-adjusted'] = round(df['GDP']/df['current dollars'].map(inf_dict_2019))
    
    return df

