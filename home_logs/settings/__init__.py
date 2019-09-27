from .base import *

try:
    from .local import *
except ImportError, exc:
    exc.args = tuple(['%s (Did you created own local.py?)' %
                     exc.args[0]])
    raise exc
