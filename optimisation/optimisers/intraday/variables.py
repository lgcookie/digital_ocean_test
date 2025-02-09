from optimisation.utils.decorators import add_to_dict

class VariablesManager:
    def __init__(self, solver, config, row):
        self.solver = solver
        self.config = config
        self.row = row
        self.variables_dict = {}
        self.degraded_energy_capacity = self.row.degraded_energy_capacity.iloc[-1]
        self.create_variables()

    
    @add_to_dict("variables_dict")  
    def create_intraday_import_variables(self):
        """BESS continous and binary export variables"""
        import_intraday_vol = [self.solver.NumVar(0, self.config.power, "import_da_vol_" + str(unit)) for unit in self.config.time_periods_str]
        import_intraday_bess = [self.solver.BoolVar("import_bess_" + str(unit)) for unit in self.config.time_periods_str]
        return {'import_intraday_vol': import_intraday_vol, 'import_intraday_bess': import_intraday_bess}
    
    @add_to_dict("variables_dict")
    def create_intraday_export_variables(self):
        """BESS continous and binary export variables"""
        export_intraday_vol = [self.solver.NumVar(0, self.config.power, "export_da_vol_" + str(unit)) for unit in self.config.time_periods_str]
        export_intraday_bess = [self.solver.BoolVar("export_bess_" + str(unit)) for unit in self.config.time_periods_str]
        return {'export_intraday_vol': export_intraday_vol, 'export_intraday_bess': export_intraday_bess}

    @add_to_dict("variables_dict")
    def create_soc_variables(self):
        soc_intraday = [self.solver.NumVar(0, self.degraded_energy_capacity, "soc_intraday" + str(unit)) for unit in self.config.time_periods_str]
        return {'soc_intraday': soc_intraday}


    @add_to_dict("variables_dict")
    def create_throughput_variables(self):
        """Dynamic frequency throughput variables and total export variables, these are not choice variables directly"""
        throughput_limit = self.degraded_energy_capacity * self.config.num_max_cycles
        intraday_export_throughput = [self.solver.NumVar(0, throughput_limit, "intraday_export_throughput" + str(unit)) for unit in self.config.time_periods_str]
        return {
            'intraday_export_throughput': intraday_export_throughput
        }
    
    def create_variables(self):
        self.create_intraday_import_variables()
        self.create_intraday_export_variables()
        self.create_soc_variables()
        self.create_throughput_variables()
      
        

