from .prices import Prices
from .bess import BESSProperties
from .times import TimeProperties
from .output_paths import OutputPaths



class Config(BESSProperties, 
             TimeProperties, 
             OutputPaths, 
             Prices,
             ):
    def __init__(self,**kwargs):
        # Call the __init__ methods of the parent classes
        
        super().__init__()
        
        
        
        
        
    pass



