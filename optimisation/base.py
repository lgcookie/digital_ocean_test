# This is the base class for the optimiser
import pandas as pd
def add_settlement_period(ix):
    return ix.hour*2+ix.minute//30+1
class BaseClass():
    # This creates the daily df shared by all subclasses, annoyingly have to create a dummy column
    @classmethod
    def set_class_attribute(cls, start_date,end_date):
        # Generate a date range with a half-hourly frequency
        date_range = pd.date_range(start=start_date, end=end_date, freq='30min')[0:-1]

        # Create a dataframe with this datetime index
        optimiser_df = pd.DataFrame(index=date_range)
        # Directly add 'settlement_period' column
        optimiser_df['settlement_period'] = optimiser_df.index.map(add_settlement_period)
        cls.optimiser_df = optimiser_df

    def __init__(self) -> None:
        pass
        
