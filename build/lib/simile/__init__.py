# simile/__init__.py
import sys
from . import config
from .resource_agent import Agent
from .resource_population import Population
from .task import Task
from .config import configure

class _SimileModuleProxy:
    def __init__(self, real_module):
        self._real_module = real_module
    
    def __getattr__(self, name):
        # If user says simile.api_key → return config.api_key
        if name == "api_key":
            return config.api_key
        elif name == "api_base":
            return config.api_base
        elif hasattr(self._real_module, name):
            return getattr(self._real_module, name)
        else:
            raise AttributeError(f"No attribute {name} in simile")
        
    def __setattr__(self, name, value):
        if name in ("_real_module",):
            super().__setattr__(name, value)
        elif name == "api_key":
            config.api_key = value
        elif name == "api_base":
            config.api_base = value
        else:
            setattr(self._real_module, name, value)

# Grab the current module object
_this_module = sys.modules[__name__]

# Replace it with our proxy
sys.modules[__name__] = _SimileModuleProxy(_this_module)
