import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_HOST = os.getenv('APP_HOST')
DEFAULT_PORT = os.getenv('APP_PORT')
APP_ENV = os.getenv('APP_ENV')

MODEL_FILE = 'model.h5'
LABEL_FILE = "labels.txt"

def IS_DEBUG():
    if os.getenv('APP_ENV').lower() in ['prod', 'production']:
        return False
    return True

