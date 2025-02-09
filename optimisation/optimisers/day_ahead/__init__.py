from ortools.linear_solver import pywraplp
import pandas as pd
from functools import partial
import numpy as np
from .variables import VariablesManager
from .objective import ObjectiveManager
from .constraints import  Constraints
from .solutions import SolutionManager
from optimisation.base import BaseClass
from multiprocessing import Pool
from math import floor as floor
import time
class DayAheadOptimiser(BaseClass):

    def __init__(self, config) -> None:
        self.config = config

    def solve_optimisation(self, row):
        """Solves the daily optimisation problem"""
        print("solving", row.index[0].date(), " until ", row.index[-1].date())
        solver = pywraplp.Solver('Scheduling Optimiser', pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
        
        vars = VariablesManager(solver, self.config, row)
        
        vars_dict = vars.variables_dict
        constraint_manager = Constraints(solver, row, vars_dict, self.config)
        solver = constraint_manager.add_all_constraints()
      
        revenue_optimiser = ObjectiveManager(vars_dict, row, self.config)
        total_revenue = revenue_optimiser.optimise_revenue()
        solver.Maximize(total_revenue)
      
        gap = 0.01
        solverParams = pywraplp.MPSolverParameters()
        solverParams.SetDoubleParam(solverParams.RELATIVE_MIP_GAP, gap)
        status = solver.Solve(solverParams)

        df_results = SolutionManager(self.config, vars_dict).extract_solutions()

        
        return df_results
