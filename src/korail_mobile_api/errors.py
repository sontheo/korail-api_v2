"""Compatible error module identity."""

import sys

from korail_api.models import errors as _implementation

sys.modules[__name__] = _implementation
