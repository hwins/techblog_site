
from techblog.settings import production_settings

# use override for development testing only
try:
    from techblog.settings import override_settings
except ImportError:
    pass
