from ortools.linear_solver import pywraplp
from .variables import VariablesManager
from .objective import ObjectiveManager
from .constraints import  ConstraintsManager
from .solutions import SolutionManager
from .constants import ConstantsManager
from math import floor as floor

class IntradayOptimiser:
    def __init__(self, config):
        self.config = config
        


    def __call__(self):
        """Run optimization using both combined data"""
        return self.solve_optimisation()

    def solve_optimisation(self, row):
        """Solves the daily optimisation problem"""
        
        solver = pywraplp.Solver('Scheduling Optimiser', pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING)
        
        vars = VariablesManager(solver, self.config, row)
        
        vars_dict = vars.variables_dict
        constants = ConstantsManager(solver,self.config,row)
        constants_dict = constants.constants_dict
    
        constraint_manager = ConstraintsManager(solver,row, vars_dict,constants_dict,self.config)
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