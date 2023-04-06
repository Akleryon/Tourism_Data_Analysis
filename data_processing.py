import pandas as pd

tourists_data = pd.read_excel('travel_data.xls', sheet_name="number_of_arrival", header=3, index_col=0)

country_list = pd.read_excel("travel_data.xls", sheet_name="country code")

def data_selection(df):
    #merge the data frame with country list data frame by county Code, so we can drop irrelevant rows
    df = pd.merge(country_list, df, left_on = "Country Code", right_on = "Country Code", how="left")
    df = df.set_index("Country Name")
    #select columns from year 2007 to 2017
    df_new = pd.concat([df["Country Code"],df.loc[:,"2007":"2017"]], axis=1)
    #replace missing value by 0
    df_new = df_new.fillna(0)
    return df_new


def reshape_data(df):
    df_new = df[:] 
    df_new.set_index(["Country Code"], inplace = True, append = True)
    #use stack to change the data frame shape
    df_new = df_new.stack()
    df_new = pd.DataFrame(df_new)
    df_new = df_new.reset_index()
    #rename column names
    df_new = df_new.rename(columns = {"level_2":"Year",0:"Amount"})
    return df_new



inbound_tourists_clean = data_selection(tourists_data)
inbound_tourists_stack = reshape_data(inbound_tourists_clean)
inbound_tourists_stack.to_csv('inbound_tourists_stack.csv')
