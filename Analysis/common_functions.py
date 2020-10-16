
def inflation_adjust_to2019(df): 
    
    df['inf-adjusted'] = round(df['value']/df['dollar-yr'].map(inf_dict_2019))
    
    return df

