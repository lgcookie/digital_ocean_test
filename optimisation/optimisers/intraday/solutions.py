import pandas as pd

class SolutionManager:
    def __init__(self, config, dict_results):
        self.config = config
        self.dict_results = dict_results
        self.processed_results = {}

    def add_period_values(self, solutions_mapping):
        for solution_name, solution_values in solutions_mapping.items():
            self.processed_results[f"{solution_name}"] = [
                self.calculate_solution_value(solution) 
                for solution in self.dict_results[solution_name]
            ]

    def calculate_solution_value(self,solutions_dict):
        """Stops any negative values and rounds down the solutions"""
        for solution_name, solution_values in solutions_dict.items():
            self.processed_results[f"{solution_name}"] = [
                max(0, solution.solution_value())
                for solution in solution_values
            ]
        
    def extract_solutions(self):
        self.calculate_solution_value(self.dict_results)
        processed_results_df = pd.DataFrame(self.processed_results)
        return processed_results_df
