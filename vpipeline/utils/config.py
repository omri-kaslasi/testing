import os
from pathlib import Path
from pathlib import Path


def get_config_value(key, default=None):
    """Get a configuration value from the environment variables.
    If the variable exists (even if empty), returns its value;
    otherwise returns the provided default.
    """
    if key in os.environ:
        return os.environ[key]
    return default

# file_loader


# vector_config_manager
CONF_DIR = get_config_value("VPIPELINE_CONF_DIR",Path('/mnt/vector-configs'))
FILTER_OUT_PORT = get_config_value("VPIPELINE_FILTER_OUT_PORT",9001)
FILTER_IN_PORT = get_config_value("VPIPELINE_FILTER_IN_PORT",9000)


# initiative_manager
DATA_DIR = get_config_value("DATA_DIR",Path('data/initiatives'))

# sink_config_builder
# source_manager
# source_config_builder
# pipeline_manager
# logger_manager

LOG_FILE = get_config_value("VPIPELINE_LOG_FILE",Path('logs/backend.log'))

# shell