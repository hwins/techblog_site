
from techblog.settings.production_settings import *

# use override for development testing only
try:
    from techblog.settings.override_settings import *
except ImportError:
    pass
