"""Compatibility module identity for the independent implementation."""

import sys

from korail_api.api import client as _implementation

sys.modules[__name__] = _implementation
