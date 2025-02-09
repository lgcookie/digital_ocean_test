import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    pass
    

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass
