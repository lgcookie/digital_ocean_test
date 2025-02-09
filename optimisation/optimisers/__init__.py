import pandas as pd
from .intraday import IntradayOptimiser
from.day_ahead import DayAheadOptimiser
from optimisation.base import BaseClass
class OptimiserManager:
    def __init__(self, config):
        self.config = config
        self.optimiser_df = BaseClass.optimiser_df

    def __call__(self):
        """Iterate over grouped data and manage scheduling and dispatching"""
        x_days = self.config.days_to_optimise  # Process each day separately
        grouped_data = self.optimiser_df.groupby(pd.Grouper(freq=f"{x_days}D"))
        results_list = []

        for _, group in grouped_data:
            print(f"Processing {group.index[0].date()}-{group.index[-1].date()}")

            # Create day_ahead_optimiser and execute
            day_ahead_optimiser = DayAheadOptimiser(self.config)
            day_ahead_optimiser_results = day_ahead_optimiser.solve_optimisation(group)

            

            # Align indexes by resetting them temporarily
            group_reset = group.reset_index(drop=True)
            day_ahead_optimiser_results_reset = day_ahead_optimiser_results.reset_index(drop=True)

            # Concatenate group and day_ahead_optimiser results
            combined_results = pd.concat([group_reset, day_ahead_optimiser_results_reset], axis=1)
            
            # Create day_ahead_optimiser and execute
            intraday_optimiser = IntradayOptimiser(self.config)
            intraday_optimiser_results = intraday_optimiser.solve_optimisation(combined_results)

            combined_results = pd.concat([combined_results,intraday_optimiser_results], axis=1)
            # Append results to list
            results_list.append(combined_results)

        # Concatenate the results into a single DataFrame
        final_results = pd.concat(results_list).reset_index(drop=True)
        final_results.index = pd.date_range(start=self.config.start_date, end=self.config.end_date, freq='30min')[0:-1]
        BaseClass.optimiser_df = final_results
        return BaseClass.optimiser_df