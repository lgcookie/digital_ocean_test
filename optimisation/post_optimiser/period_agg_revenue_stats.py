import pandas as pd
from optimisation.base import BaseClass
import inspect
class PostOptimiserAggRevenueStats():

    def __init__(self,config) -> None:
        self.config = config
        self.optimiser_df = BaseClass.optimiser_df
    def __call__(self):
        """ 
        Parameters
        ----------
        BaseClass.optimiser_df : pandas df
            The df contains: the results of the optimisation, import & export prices, solar production and gross & net demand.

        Returns
        -------
        BaseClass.optimiser_df : pandas df
            
        """
        
        # Return all functions in the class, then only return the "get" functions
        funcs = inspect.getmembers(PostOptimiserAggRevenueStats, predicate=inspect.isfunction)
        names = [func[0] for func in funcs if func[0].startswith("get")]
        for name in names:
            col_name = name.replace("get_","")
            self.optimiser_df[col_name] = self.optimiser_df.apply(getattr(self,name),axis=1)

        # SHOULD FIND BETTER WAY TO DO THIS
        BaseClass.optimiser_df = self.optimiser_df
        BaseClass.optimiser_df.index = pd.date_range(start=self.config.start_date, end=self.config.end_date, freq='30min')[0:-1]
        return BaseClass.optimiser_df
        
    
    def get_cash_flow_bess_da(self,row):
        """
        Returns a pd series of the bess day ahead trading revenue, the substraction of imported energy cost from exported energy revenue
        """
        return (row["cash_flow_export_da_vol"] + row["cash_flow_import_da_vol"])
    
    def get_cash_flow_bess_intraday(self,row):
        """
        Returns a pd series of the bess intraday trading revenue, a user defined proportion of day ahead revenue
        """
        return (row["cash_flow_export_intraday_bess_vol"] + row["cash_flow_import_intraday_bess_vol"])
    
 



    
    

    
    


    
    

    