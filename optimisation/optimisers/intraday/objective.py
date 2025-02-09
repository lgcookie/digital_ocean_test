class ObjectiveManager:
    def __init__(self, vars, row, config):
        self.vars = vars
        self.row = row
        self.config = config

    def calculate_intraday_revenue(self):
        '''BESS revenue is from importing/exporting from/to grid, and it pays the market price for any volumes received from PV
        '''
        intraday_revenue = sum(
            [
                self.row[f"intraday_price"].iloc[period_int] * self.vars["export_intraday_vol"][period_int] * self.config.discharging_efficiency * (self.config.hh_power_to_energy) 
                - self.row[f"intraday_price"].iloc[period_int] * self.vars["import_intraday_vol"][period_int] * (self.config.hh_power_to_energy) 
                for period_int, period_str in zip(self.config.time_periods_int, self.config.time_periods_str)
            ]
        )
        return intraday_revenue
    
    

    def optimise_revenue(self):
        intraday_revenue = self.calculate_intraday_revenue()
        return intraday_revenue
