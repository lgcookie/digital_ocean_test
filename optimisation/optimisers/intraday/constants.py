from optimisation.utils.convert_negatives_to_zero import convert_negatives_to_zero
import pandas as pd
from optimisation.utils.decorators import add_to_dict

class ConstantsManager:
    def __init__(self, solver, config, row):
        self.solver = solver
        self.config = config
        self.row = row
        self.constants_dict = {}
        self.create_constants()




    @add_to_dict("constants_dict")
    def create_export_power_headroom_constants(self):
        """BESS export power headroom based off power capacity allocation to frequency and importing"""
        export_power_headroom_periods = []
        for period_int in self.config.time_periods_int:
            bess_export_headroom = self.config.power - self.row[f"export_da_vol"][period_int]
            export_power_headroom_periods.append(bess_export_headroom)
        export_power_headroom = convert_negatives_to_zero(export_power_headroom_periods)
        return {'export_power_headroom': export_power_headroom}
    
    @add_to_dict("constants_dict")
    def create_import_power_headroom_constants(self):
        """BESS import power headroom based off power capacity allocation to frequency and importing"""
        import_power_headroom_periods = []
        for period_int in self.config.time_periods_int:
            bess_import_headroom = self.config.power - self.row[f"import_da_vol"][period_int]
            import_power_headroom_periods.append(bess_import_headroom)
        import_power_headroom = convert_negatives_to_zero(import_power_headroom_periods)
        return {'import_power_headroom': import_power_headroom}

    
    @add_to_dict("constants_dict")
    def soc_da_constants(self):
        """Stores the net energy flow from the PV to the BESS"""
        soc_da = [self.row[f"soc"][period_int] for period_int,period_str in zip(self.config.time_periods_int,self.config.time_periods_str)]
        
        return {'soc_da': soc_da}
    
    def create_constants(self):
        self.create_export_power_headroom_constants()
        self.create_import_power_headroom_constants()
        self.soc_da_constants()
         