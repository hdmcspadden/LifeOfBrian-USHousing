import pandas as pd
import os
# import matplotlib.pyplot as plt

# Changing the working directory
os.chdir(os.getcwd())

# Reading in the csv
FreddieData = pd.read_csv("FreddieMacHistoricalWeeklyData.csv",
                   encoding = "ISO-8859-1", error_bad_lines = False)
GDPdata = FreddieData = pd.read_csv("yearlyGDPbyState.csv",
                   encoding = "ISO-8859-1").iloc[:,1:]

# Data cleaning
FreddieData2 = FreddieData.iloc[6:2549,0:4]
FreddieData2 = FreddieData2.drop(FreddieData2.columns[[2]], axis = 1)

FreddieData2.columns = ["Week","30_Year","15_Year"]

# Converting the data into correct datatypes
FreddieData2["Week"] = FreddieData2["Week"].apply(pd.to_datetime)
FreddieData2[["30_Year","15_Year"]] = FreddieData2[["30_Year","15_Year"]].apply(pd.to_numeric)

FreddieData2.dtypes

# Select only dates between 1995 and 2013
start_date = '1995-01-01'
end_date = '2013-12-31'
dtrange = (FreddieData2["Week"] >= start_date) & (FreddieData2["Week"] <= end_date)
FreddieData3 = FreddieData2.loc[dtrange]
FreddieData3.reset_index() # Reset index

# Group by the year and get the average mortgage rate
FreddieData4 = FreddieData3.groupby(FreddieData3["Week"].dt.to_period("Y"))["30_Year","15_Year"].agg("mean")
FreddieData4 = FreddieData4.reset_index() # Reset index
FreddieData4["Week"] = FreddieData4["Week"].to_timestamp
FreddieData4["Week"] = FreddieData4.Week.values.astype('datetime64[M]')
FreddieData4["Week"] = pd.DatetimeIndex(FreddieData4["Week"]).year
FreddieData4.rename(columns = {"Week": "year"}, inplace = True)

# Setting the GDP as numeric
GDPdata["GDP"] = GDPdata["GDP"].str.replace(',','') # Need to remove commas from the column first
GDPdata["GDP"] = GDPdata["GDP"].apply(pd.to_numeric)

# Getting average GDP by year
GDPdata_mean_GDP = GDPdata.groupby("year")["GDP"].mean()
GDPdata_mean_GDP = GDPdata_mean_GDP.reset_index()

# Combine both datasets
dataCombined = pd.merge(FreddieData4, GDPdata_mean_GDP, how = "inner")
dataCombined["year"] = pd.to_datetime(dataCombined.year, format='%Y')


secondary = dataCombined.plot(secondary_y=["15_Year", "30_Year"], x = "year")
secondary.legend(loc="upper right")


'''
# Grouping the data by quarter
FreddieData4 = FreddieData3.groupby(FreddieData3["Week"].dt.to_period("Q"))["30_Year","15_Year"].agg("mean")

# Grouping the data by month
FreddieData5 = FreddieData3.groupby(FreddieData3["Week"].dt.to_period("M"))["30_Year","15_Year"].agg("mean")

# Some Visualizations
FreddieData5.plot()
'''

'''
Stuff to do in the future:
    1. turn freddie, gdpdata processing into classes
    2. account for further datasets easily
    3. place the legend outside the plot
'''
