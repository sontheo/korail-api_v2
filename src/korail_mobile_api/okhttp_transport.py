"""Compatibility module identity for the independent implementation."""

import sys

from korail_api.transport import curl as _implementation

sys.modules[__name__] = _implementation
