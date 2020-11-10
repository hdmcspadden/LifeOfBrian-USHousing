import pandas as pd
import matplotlib as plt

FreddieData = pd.read_csv("https://raw.githubusercontent.com/hdmcspadden/LifeOfBrian-USHousing/master/DataSet/FreddieMacHistoricalWeeklyData.csv",
                          encoding = "ISO-8859-1", error_bad_lines = False)

GDP = pd.read_csv("https://raw.githubusercontent.com/hdmcspadden/LifeOfBrian-USHousing/master/DataSet/yearlyGDPbyState.csv")

def create_inf_dict(year):
    # create a dictionary with inflation conversion factors

    # Read in the inflation data
    inf_data = pd.read_csv("https://raw.githubusercontent.com/hdmcspadden/LifeOfBrian-USHousing/master/DataSet/1995Inflation.csv")

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

# Data cleaning and calculating the average mortgage rate by year

def FreddieData_Avg_Mortgage_Rate(df, start_date, end_date):
    FreddieData2 = df.iloc[6:2549,0:4]
    FreddieData2 = FreddieData2.drop(FreddieData2.columns[[2]], axis = 1)
    
    FreddieData2.columns = ["Week","30_Year","15_Year"]
    
    # Converting the data into correct datatypes
    FreddieData2["Week"] = FreddieData2["Week"].apply(pd.to_datetime)
    FreddieData2[["30_Year","15_Year"]] = FreddieData2[["30_Year","15_Year"]].apply(pd.to_numeric)

    # start_date = '1995-01-01'
    # end_date = '2019-12-31'
    dtrange = (FreddieData2["Week"] >= start_date) & (FreddieData2["Week"] <= end_date)
    FreddieData3 = FreddieData2.loc[dtrange]
    FreddieData3.reset_index() # Reset index
    
    # Group by the year and get the average mortgage rate
    FreddieData4 = FreddieData3.groupby(FreddieData3["Week"].dt.to_period("Y"))["30_Year","15_Year"].agg("mean")
    FreddieData4 = FreddieData4.reset_index() # Reset index
    FreddieData4["Week"] = FreddieData4.Week.values.astype('datetime64[M]')
    FreddieData4["Week"] = pd.DatetimeIndex(FreddieData4["Week"]).year
    FreddieData4.rename(columns = {"Week": "year"}, inplace = True)
    
    return FreddieData4

def FreddieMortgage_versus_GDP_by_Year(FreddieData, GDP):
    
    FreddieDataFinal = FreddieData_Avg_Mortgage_Rate(FreddieData, '1995-01-01', '2019-12-31')

    # Applying the inflaction_adjust class to the GDP dataset
    inflation_adjust(GDP)
    
    GDPdata_mean_GDP = GDP.groupby("year")["inf-adjusted"].sum()
    GDPdata_mean_GDP = GDPdata_mean_GDP.reset_index()
    
    # Combine both datasets
    dataCombined = pd.merge(FreddieDataFinal, GDPdata_mean_GDP, how = "inner")
    dataCombined["year"] = pd.to_datetime(dataCombined.year, format='%Y')
    
    # Creating a dual y-axis plot to plot GDP against the 15 and 30 Year FRM
    ax = dataCombined.plot("year","inf-adjusted", legend = False, label = "Inflation Adjusted GDP")
    ax.axes.yaxis.set_ticklabels([])
    ax2 = dataCombined.plot("year",["15_Year", "30_Year"], secondary_y = True, ax = ax, legend = False, label = ["15 Year FRM", "30 Year FRM"])
    
    # Setting appropriate labels for each y-axis
    ax.set_ylabel("Inflation Adjusted GDP (millions)", fontname="Arial", fontsize=10)
    ax2.set_ylabel("Mortgage Rates", fontname="Arial", fontsize=10)
    ax.set_xlabel("Year", fontname="Arial", fontsize=10)
    ax.set_title("Inflation Adjusted GDP vs Mortgage Rates From 1995 - 2019", fontname="Arial", fontsize=10)
    
    # Setting a legend
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 10})

FreddieMortgage_versus_GDP_by_Year(FreddieData, GDP)
