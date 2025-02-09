# Big M solution to activate binary variables in ramp rate constraints  
M = 10000

class Constraints:
    def __init__(self, solver, row, variables_dict, config):
        self.solver = solver
        self.row = row
        self.vars = variables_dict
        self.config = config
        self.degraded_energy_capacity = self.row.degraded_energy_capacity.iloc[-1]
    def add_initial_constraint(self):
        """The SoC begins the day at 0, and you can't export in period 0."""
        self.solver.Add(self.vars["soc"][0] == 0)
        self.solver.Add(self.vars["export_da_vol"][0] == 0)

    def add_soc_equality_constraint(self, period_int):
        """The SoC is a stock determined by the energy flows of: importing, exporting and throughput from frequency response"""
        self.solver.Add(self.vars['soc'][period_int] == self.vars['soc'][period_int-1] +
                        self.vars['import_da_vol'][period_int] * (self.config.hh_power_to_energy) * self.config.charging_efficiency -
                        self.vars['export_da_vol'][period_int] * (self.config.hh_power_to_energy) * self.config.discharging_efficiency)
    
        
    def add_da_export_throughput_constraint(self, period_int):
        """A helper variable used to calculate export of the BESS"""
        self.solver.Add(self.vars['da_export_throughput'][period_int] == (self.vars['export_da_vol'][period_int] * 
                        (self.config.hh_power_to_energy)))

    def add_soc_constraint(self, period_int):
        """Keeps the SoC within operational limits"""
        self.solver.Add(0 <= self.vars['soc'][period_int] <= self.row.degraded_energy_capacity.iloc[-1])
        
    def add_bess_export_import_indicator(self, period_int):
        """Sets indicator variables if BESS is importing or exporting (needed for ramp rate activation) and prevents simultaneous import/export."""
        self.solver.Add(0 <= self.vars['import_da_vol'][period_int] <= M * self.vars['import_bess'][period_int])
        self.solver.Add(0 <= self.vars['export_da_vol'][period_int] <= M * self.vars['export_bess'][period_int])
        self.solver.Add(0 <= self.vars['import_bess'][period_int] + self.vars['export_bess'][period_int] <= 1)

    def add_da_hourly_constraint(self, period_int):
        """Sets the hourly constraint for the day ahead period (the volume delivered across an hourly period is the same)"""
        if period_int % 2 == 1 and period_int + 1 < len(self.config.time_periods_int):  # Only add constraint for odd-numbered periods (first half of each hour):  # Only add constraint for odd-numbered periods (first half of each hour)
            self.solver.Add(self.vars['import_da_vol'][period_int] == self.vars['import_da_vol'][period_int + 1])
            self.solver.Add(self.vars['export_da_vol'][period_int] == self.vars['export_da_vol'][period_int + 1])
   
    def add_num_max_cycles_constraints(self):
        """Limits the maximum cycles based on the degraded energy capacity"""
        self.solver.Add(0 <= sum(self.vars['da_export_throughput'][:]) <= 
                        self.degraded_energy_capacity * self.config.num_max_cycles*(1-self.config.intraday_reserve_cycling))

    def add_all_constraints(self):
        """Adds all necessary constraints"""
        self.add_initial_constraint()     
        for period_int in self.config.time_periods_int:
            self.add_soc_constraint(period_int)
            self.add_bess_export_import_indicator(period_int)
            self.add_soc_equality_constraint(period_int)
            self.add_da_export_throughput_constraint(period_int)
            self.add_da_hourly_constraint(period_int)
        self.add_num_max_cycles_constraints()
        return self.solver
