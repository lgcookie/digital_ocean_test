
from optimisation.pre_optimiser import PreProcess
from optimisation.base import BaseClass
from optimisation.optimisers import OptimiserManager
from optimisation.post_optimiser.period_energy_flow import PostOptimiserPeriodEnergyStats
from optimisation.post_optimiser.period_revenue_stats import PostOptimiserPeriodRevenueStats
from optimisation.post_optimiser.period_agg_revenue_stats import PostOptimiserAggRevenueStats
import time
from optimisation.config.setup import Config
def run_optimisation(config):
    BaseClass.set_class_attribute(config.start_date, config.end_date)
    PreProcess(config)()
    OptimiserManager(config)()
    
    PostOptimiserPeriodEnergyStats(config)()
    PostOptimiserPeriodRevenueStats(config)()
    optimiser_df = PostOptimiserAggRevenueStats(config)()
    
    optimiser_df.to_csv(config.output_path)
    return optimiser_df
