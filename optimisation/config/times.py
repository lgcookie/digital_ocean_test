import pandas as pd
class TimeProperties:
    days_to_optimise = 1
    hh_power_to_energy = 0.5
    num_time_periods = 48*days_to_optimise
    start_date =  pd.to_datetime("2023-01-14")
    end_date = pd.to_datetime("2023-01-31")
    time_periods_int = range(num_time_periods)
    time_periods_str = ["{:02d}".format(x) for x in time_periods_int]