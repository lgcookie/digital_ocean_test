from optimisation.utils.decorators import add_to_dict

class VariablesManager:
    def __init__(self, solver, config, row):
        self.solver = solver
        self.config = config
        self.row = row
        self.variables_dict = {}
        self.create_variables()
    
    @add_to_dict("variables_dict")
    def create_throughput_variables(self):
        """Dynamic frequency throughput variables and total export variables, these are not choice variables directly"""
        throughput_limit = self.row.degraded_energy_capacity.iloc[-1] * self.config.num_max_cycles * self.config.intraday_reserve_cycling
        da_export_throughput = [self.solver.NumVar(0, throughput_limit, "da_export_throughput" + str(unit)) for unit in self.config.time_periods_str]
        return {
            'da_export_throughput': da_export_throughput
        }
    

    @add_to_dict("variables_dict")
    def create_import_variables(self):
        """BESS continuous and binary import variables"""
       
        import_da_vol = [self.solver.NumVar(0, self.config.power, "import_da_vol_" + str(unit)) for unit in self.config.time_periods_str]
        import_bess = [self.solver.BoolVar("import_bess_" + str(unit)) for unit in self.config.time_periods_str]
        return {'import_da_vol': import_da_vol, 'import_bess': import_bess}

    @add_to_dict("variables_dict")
    def create_export_variables(self):
        """BESS continuous and binary export variables"""
        export_da_vol = [self.solver.NumVar(0, self.config.power, "export_da_vol_" + str(unit)) for unit in self.config.time_periods_str]
        export_bess = [self.solver.BoolVar("export_bess_" + str(unit)) for unit in self.config.time_periods_str]
        return {'export_da_vol': export_da_vol, 'export_bess': export_bess}


    @add_to_dict("variables_dict")
    def create_soc_variables(self):
        soc = [self.solver.NumVar(0, self.row.degraded_energy_capacity.iloc[-1], "soc" + str(unit)) for unit in self.config.time_periods_str]
        return {'soc': soc}

    def create_variables(self):
        self.create_import_variables()
        self.create_export_variables()
        self.create_soc_variables()
        self.create_throughput_variables()
