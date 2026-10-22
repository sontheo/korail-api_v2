"""Compatibility module identity for the independent implementation."""

import sys

from korail_api.configuration import device as _implementation

sys.modules[__name__] = _implementation
