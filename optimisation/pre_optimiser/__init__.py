import pandas as pd
from optimisation.base import BaseClass
import numpy as np
import inspect
import math
class PreProcess():

    def __init__(self, config) -> None:
        self.config = config
        self.optimiser_df = BaseClass.optimiser_df
        self.preloaded_data = {}

    def __call__(self):
        """
        Process and populate the optimiser_df with all the relevant columns.
        """
        # Preload data for frequently used lookups
        self._preload_data(["price_df"])

        # Fetch and apply "get_" functions
        funcs = inspect.getmembers(self, predicate=inspect.ismethod)
        for name, func in funcs:
            if name.startswith("get_"):
                col_name = name.replace("get_", "")

                self.optimiser_df[col_name] = self.optimiser_df.apply(func, axis=1)

                
        BaseClass.optimiser_df = self.optimiser_df
        
        return BaseClass.optimiser_df

    def _preload_data(self, dataframes):
        """
        Preload frequently accessed dataframes into lookup tables (useful for performance)
        """
        for df_name in dataframes:
            if hasattr(self.config, df_name):
                df = getattr(self.config, df_name)
                self.preloaded_data[df_name] = df.set_index(df.index)

    def get_day_ahead_price(self, row):
        """
        Retrieve import price for each period in the day.
        """
        value = float(
            self.preloaded_data["price_df"].loc[
                row.name,
                "day-ahead"]
        )
     
        return value

    def get_intraday_price(self, row):
        """
        Retrieve export price for each period in the day.
        """
        
        value = float(
            self.preloaded_data["price_df"].loc[
                row.name,
                "intra-day"]
            
        )
        return value

    def get_degraded_energy_capacity(self, row):
        """
        Return the degraded energy capacity of the BESS.
        """
        # Calculate days since start date
        days_since_start = (row.name - self.config.start_date).days
        
        # Calculate total cycles (2 per day)
        total_cycles = days_since_start * 2
        
        # Interpolate degradation from the degradation curve
        degraded_capacity_percentage = np.interp(
            total_cycles,
            self.config.bess_degradation_df['num_cycles'],
            self.config.bess_degradation_df['%_BOL_ac_capacity']
        )
        
        # Calculate actual degraded capacity
        degraded_capacity = self.config.capacity * degraded_capacity_percentage
        
        return degraded_capacity

    