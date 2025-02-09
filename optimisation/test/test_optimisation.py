import unittest
import pandas as pd
from optimisation.main import run_optimisation
from optimisation.config.setup import Config

class OptimiserTests(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.config = Config()
        self.config.power = 100  # MW
        self.config.capacity = 200  # MWh
        self.config.charging_efficiency = 0.85
        self.config.discharging_efficiency = 0.85
        self.config.daily_cycles = 2
        self.config.start_date = pd.Timestamp('2023-01-01')
        
    def test_optimise_day_ahead_works(self):
        """Test day ahead optimisation produces a result"""
        self.days_to_optimise = 10
        self.config.end_date = self.config.start_date + pd.Timedelta(days=self.days_to_optimise)
        self.config.price_df = pd.DataFrame({
            'day-ahead': [50] * self.days_to_optimise*48,
            'intra-day': [100] * self.days_to_optimise*48
        },
        index=pd.date_range(start=self.config.start_date, periods=self.days_to_optimise*48, freq='30min'))
        print("rnning this test",self.config.price_df)
        optimiser_df = run_optimisation(self.config)
        
        # Assert
        self.assertIsNotNone(optimiser_df, "Optimization returned None")

    def test_arbitrage_behavior_day_ahead(self):
        """Test if the battery charges at low prices and discharges at high prices"""
        self.days_to_optimise = 10
        self.config.end_date = self.config.start_date + pd.Timedelta(days=self.days_to_optimise)
        half_days = int(self.days_to_optimise*48*0.5*0.5)
        self.config.price_df = pd.DataFrame({
            'day-ahead': [50,75] * half_days + [100,200] * half_days,
            'intra-day': [100] * self.days_to_optimise*48
        },
        index=pd.date_range(start=self.config.start_date, periods=self.days_to_optimise*48, freq='30min'))
        result = run_optimisation(self.config)
        # Check if cash flow is higher during higher spreads
        first_half_cash_flow = result['cash_flow_bess_da'][:half_days].sum()+result['cash_flow_bess_intraday'][:half_days].sum()
        second_half_cash_flow = result['cash_flow_bess_da'][half_days:].sum()+result['cash_flow_bess_intraday'][half_days:].sum()
        self.assertGreater(second_half_cash_flow, first_half_cash_flow, 
                          "Battery should charge more during low price periods")

    def test_cycles_not_exceeded(self):
        """Test that battery cycles don't exceed the daily limit"""
        self.days_to_optimise = 10
        self.config.end_date = self.config.start_date + pd.Timedelta(days=self.days_to_optimise)
        
        # Create price pattern that would create trading (i.e. high spreads)
        self.config.price_df = pd.DataFrame({
            'day-ahead': [50, 200] * (self.days_to_optimise*24),  
            'intra-day': [100] * self.days_to_optimise*48
        },
        index=pd.date_range(start=self.config.start_date, periods=self.days_to_optimise*48, freq='30min'))
        
        result = run_optimisation(self.config)
        
        # Calculate cycles using intraday_export_throughput
        bess_cycle_df = result[["intraday_export_throughput"]].copy()
        bess_cycle_df["num_cycles"] = bess_cycle_df["intraday_export_throughput"] / self.config.capacity
        daily_cycles = bess_cycle_df.groupby(bess_cycle_df.index.date)["num_cycles"].sum()
        
        # Check no day exceeds cycle limit
        self.assertTrue(all(daily_cycles <= self.config.daily_cycles),
                    f"Daily cycles exceeded limit of {self.config.daily_cycles} on some days. Max was {daily_cycles.max():.2f}")


if __name__ == '__main__':
    unittest.main()