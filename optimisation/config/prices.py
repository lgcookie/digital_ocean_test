import pandas as pd
import os 
class Prices:
    price_df_filename = "dataset.csv"
    price_df = pd.read_csv(os.path.join(os.getcwd(),"optimisation","data_input",price_df_filename),sep=",",thousands=",",low_memory=False,index_col=0,encoding="utf-8")
    price_df.index = pd.to_datetime(price_df.index,dayfirst=True)
