
import pandas as pd
import sys

class COMMONFUNCTIONS:
    
    def __init__(self):  # constructor
        one = 1

# Create a function that adjusts a series of data based on 2019_factor. The function accepts a dataframe, which must have
#a column labeled 'year' and a column labeled 'value'.

# Function to convert a column labeled 'value', from the passed dataframe to 2019 dollars
# Years can be from anywhere in the range of 1996-2020
# Need to instantiate the inflation dataframe for this to work (see above code ) 


    def inflation_adjust(self, df): 
    
        # Read in the inflation data
        inf_data = pd.read_csv("../dataset/1995inflation.csv")
    
        # Work with the inflation data to use in an adjustment function
    
        # Column'amount' is a cumulative price index with 1995 as year 0. 
        # Calculate a factor for each state that converts 'amount' to 2019 dollars by dividing by 1.68 (the 2019 'amount'value)
    
        # Select the conversion factor from the data frame using .loc
        d2019 = inf_data.loc[inf_data['year'] == 2019,'amount'].item()
    
        #df = df.rename(columns={'GDP':'value', 'current dollars':'dollar-yr'})
    
        # Apply the factor to all rows
        inf_data['2019_factor']=inf_data['amount']/d2019
        inf_data.head()
    
        # Store the factors in a dictionary for easy use in a function
        inf_dict_2019 = dict(zip(inf_data['year'], inf_data['2019_factor']))
    
        df['inf-adjusted'] = round(df['GDP']/df['current dollars'].map(inf_dict_2019))
        
        return df
    
    # Create a function that adjusts a series of data based on 2019_factor. The function accepts a dataframe, which must have
    #a column labeled 'year' and a column labeled 'value'.
    
    # Function to convert a column labeled 'value', from the passed dataframe to 2019 dollars
    # Years can be from anywhere in the range of 1996-2020
    # Need to instantiate the inflation dataframe with following columns:  value	dollar-yr for this to work
    def inflation_adjust_to2019(self, df, price_dict): 
        
        df['inf-adjusted'] = round(df['value']/df['dollar-yr'].map(price_dict))
        
        return df

