# import needed libraries 
from numpy import *
import pandas as pd

# testing loading inflation data set
dfInflation = pd.read_csv('DataSet/inflation_data.csv',header=0,encoding = "ISO-8859-1")

dfInflation.head(5)
