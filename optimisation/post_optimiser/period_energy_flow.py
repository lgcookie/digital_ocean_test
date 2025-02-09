import pandas as pd
import numpy as np
from optimisation.base import BaseClass
import inspect
class PostOptimiserPeriodEnergyStats():

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
        funcs = inspect.getmembers(PostOptimiserPeriodEnergyStats, predicate=inspect.isfunction)
        names = [func[0] for func in funcs if func[0].startswith("get")]
        for name in names:
   
            col_name = name.replace("get_","")
            self.optimiser_df[col_name] = self.optimiser_df.apply(getattr(self,name),axis=1)

            
        BaseClass.optimiser_df = self.optimiser_df
        return BaseClass.optimiser_df

### Clearly can be refactored as DRY ###

    def get_energy_flow_import_da_vol(self,row):
        """
        Returns a pd series of the solar energy being clipped, accounting for losses of 5%
        """
        return row[f"import_da_vol"]*self.config.hh_power_to_energy     

    def get_energy_flow_export_da_vol(self,row):
        """
        Returns a pd series of the solar energy being clipped, accounting for losses of 5%
        """
        return row[f"export_da_vol"]*self.config.hh_power_to_energy*self.config.discharging_efficiency    

    def get_energy_flow_import_intraday_bess_vol(self,row):
        """
        Returns a pd series of the solar energy being clipped, accounting for losses of 5%
        """
        return row[f"import_intraday_vol"]*self.config.hh_power_to_energy

    def get_energy_flow_export_intraday_bess_vol(self,row):
        """
        Returns a pd series of the solar energy being clipped, accounting for losses of 5%
        """
        return row[f"export_intraday_vol"]*self.config.hh_power_to_energy*self.config.discharging_efficiency   

    

     