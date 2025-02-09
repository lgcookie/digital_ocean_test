import pandas as pd
import numpy as np
from optimisation.base import BaseClass
import inspect
class PostOptimiserPeriodRevenueStats():

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
        funcs = inspect.getmembers(PostOptimiserPeriodRevenueStats, predicate=inspect.isfunction)
        names = [func[0] for func in funcs if func[0].startswith("get")]
        for name in names:
 
            col_name = name.replace("get_","")
            self.optimiser_df[col_name] = self.optimiser_df.apply(getattr(self,name),axis=1)


            
        BaseClass.optimiser_df = self.optimiser_df
        return BaseClass.optimiser_df

    ### CALCULATE PERIOD CASH FLOW ###

    def get_cash_flow_export_da_vol(self,row):
        """
        Returns a pd series of the bess cash inflow at each period, 
        the product of energy exported to grid from BESS and the export price
        """
        return row[f"energy_flow_export_da_vol"]*row[f"day_ahead_price"] 

    def get_cash_flow_import_da_vol(self,row):
        """
        Returns a pd series of the bess cash outflow at each period from purchasing from grid, 
        the product of imported and the import price
        """
        return -row[f"energy_flow_import_da_vol"]*row[f"day_ahead_price"] 
     
   
    def get_cash_flow_export_intraday_bess_vol(self,row):
        """
        Returns a pd series of the bess intraday export revenues from balancing in real time. Note that the final intraday revenues are determined as an uplift on day ahead trading and NOT
        this value
        """

        return row[f"energy_flow_export_intraday_bess_vol"]*row[f"intraday_price"]  

   
    def get_cash_flow_import_intraday_bess_vol(self,row):
        """
        Returns a pd series of the bess bm revenues. This is assumed to come from bm instructions and
        subsequent profit maximising actions at intraday
        """
        
        return -row[f"energy_flow_import_intraday_bess_vol"]*row[f"intraday_price"]*(1/self.config.charging_efficiency)

