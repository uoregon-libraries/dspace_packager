import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig(object):

  FLASK_ENV = 'development'
  DEBUG = False
  SECRET_KEY = os.getenv('SECRET_KEY', default = 'BAD_SECRET_KEY')

class ProductionConfig(BaseConfig): 
  FLASK_ENV = 'production'

class DevelopmentConfig(BaseConfig):
  DEBUG = True
