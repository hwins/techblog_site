
from techblog_site.settings.production_settings import *

# use override for development testing only
try:
    from techblog_site.settings.override_settings import *
except ImportError:
    pass
