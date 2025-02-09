
# Big M solution to activate binary variables in ramp rate constraints  
M=10000

class ConstraintsManager:
    def __init__(self, solver,row, variables_dict,constants,config):
        self.solver = solver
        self.row = row
        self.vars = variables_dict
        self.config = config
        self.constants = constants
        self.degraded_energy_capacity = self.row.degraded_energy_capacity.iloc[-1]
    
    def add_initial_constraint(self):
        """The SoC begins the day at 0, and you can't export in period 0."""
        self.solver.Add(self.vars["soc_intraday"][0] == 0)
        self.solver.Add(self.vars["export_intraday_vol"][0] == 0)
    
    def add_soc_constraint(self, period_int):
        """The SoC is a stock determined by the energy flows committed in the day_ahead_optimiser decision a day ahead (the difference between the SoC)"""

        self.solver.Add(self.vars['soc_intraday'][period_int] ==\
                self.vars['soc_intraday'][period_int-1] +
                (self.constants['soc_da'][period_int] - self.constants['soc_da'][period_int-1]) + 
                (self.vars['import_intraday_vol'][period_int] * self.config.charging_efficiency * (self.config.hh_power_to_energy)) -
                (self.vars['export_intraday_vol'][period_int] * (self.config.hh_power_to_energy)))
    
    

    def add_bess_import_headroom_constraint(self, period_int):
        """A helper variable used to calculate export of the BESS"""
        self.solver.Add(self.vars['import_intraday_vol'][period_int]<= self.constants['import_power_headroom'][period_int])
    
    def add_bess_export_headroom_constraint(self, period_int):
        """A helper variable used to calculate export of the BESS"""
        self.solver.Add(self.vars['export_intraday_vol'][period_int]<= self.constants['export_power_headroom'][period_int])
        
    def add_bess_export_import_constraint(self,period_int):
        """This sets indicator variables if BESS is importing or exporting (needed for ramp rate activation)
        Also, it prevents the BESS importing and exporting at the same time"""
        self.solver.Add(0 <= self.vars['import_intraday_vol'][period_int] <= M * self.vars['import_intraday_bess'][period_int])
        self.solver.Add(0 <= self.vars['export_intraday_vol'][period_int] <= M * self.vars['export_intraday_bess'][period_int])
        self.solver.Add(0 <= self.vars['import_intraday_bess'][period_int] + self.vars['export_intraday_bess'][period_int] <= 1)


    def add_export_throughput_constraint(self, period_int):
        """A helper variable used to calculate export of the BESS"""
        self.solver.Add(self.vars['intraday_export_throughput'][period_int] == (\
            self.row['da_export_throughput'][period_int] + 
            (self.vars['export_intraday_vol'][period_int] * (self.config.hh_power_to_energy))))
        
    def add_num_max_cycles_constraints(self):
        """Limits the maximum cycles based on the degraded energy capacity"""
        self.solver.Add(0 <= sum(self.vars['intraday_export_throughput'][:]) <= 
                        self.degraded_energy_capacity * self.config.num_max_cycles )
       
    
    
    def add_all_constraints(self):
        for period_int in self.config.time_periods_int:
            self.add_soc_constraint(period_int)
            self.add_bess_export_import_constraint(period_int)
            self.add_bess_export_headroom_constraint(period_int)
            self.add_bess_import_headroom_constraint(period_int)
            self.add_export_throughput_constraint(period_int)
        self.add_initial_constraint()
        self.add_num_max_cycles_constraints()

        return self.solver