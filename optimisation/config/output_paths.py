import os
from datetime import datetime
class OutputPaths:
    time_str = datetime.now().strftime("%m-%d")
    output_filename = "example"
    output_filename = f"{output_filename}_{time_str}.csv"
    output_path = os.path.join(os.getcwd(),"optimisation","data_output","raw_output",output_filename)

    
    

    
