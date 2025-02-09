import pandas as pd
import os
class BESSProperties:
    power = 100
    capacity = 100
    charging_efficiency = 0.85
    discharging_efficiency = 1.0
    daily_cycles = 2.0
    initial_soc = 25
    num_max_cycles = 2
    bess_degradation_df = pd.read_excel(
        os.path.join(
        os.getcwd(),
        "optimisation",
        "data_input",
        "degradation_curve.xlsx")
        ,sheet_name="degradation_vs_cycles")
    
    intraday_reserve_cycling = 0.1 # % amount of cycling that is reserved for intraday
    

