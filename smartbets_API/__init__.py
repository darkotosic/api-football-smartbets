__version__ = "1.3.2"
__author__ = "Smartwa Caleb"
from .bet_at_rest_api_level import predictor as rest_api
from .predictor import Predictor

__all__ = [
    "api_football",
    "Predictor",
    "rest_api",
]
