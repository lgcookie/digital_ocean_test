class ObjectiveManager:
    def __init__(self, vars, row, config):
        self.vars = vars
        self.row = row
        self.config = config

    def calculate_bess_revenue(self):
        '''BESS revenue is from importing/exporting from/to grid, and it pays the market price for any volumes received from PV'''
        bess_revenue = sum(
            [
                self.row["day_ahead_price"].iloc[period_int] * self.vars["export_da_vol"][period_int] * 
                self.config.discharging_efficiency * self.config.hh_power_to_energy -

                self.row["day_ahead_price"].iloc[period_int] * self.vars["import_da_vol"][period_int] * 
                self.config.charging_efficiency * self.config.hh_power_to_energy 
                for period_int in self.config.time_periods_int
            ]
        )
        return bess_revenue
    
    def optimise_revenue(self):
        bess_revenue = self.calculate_bess_revenue()
        return bess_revenue 
