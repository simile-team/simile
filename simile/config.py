# simile/config.py
"""
Holds global configurations for the simile library.
"""

# Default global configs
api_key = None  # The user must set this before making calls
api_base = "https://agentbank-f515f1977c64.herokuapp.com/agents/api"  # default; override if needed

def configure(key=None, base=None):
    """
    Convenience function to set global API key/base from user code.
    Example:
        import simile
        simile.configure(key="abc123", base="https://example.com/agents/api")
    """
    global api_key, api_base
    if key is not None:
        api_key = key
    if base is not None:
        api_base = base
