"""Protocol constants and compatible enum imports."""

from korail_api.configuration.device import build_dalvik_user_agent
from korail_api.models.records import *
from korail_api.models.records import restore
from korail_api.protocol.schema import load

globals().update({name: restore(data) for name, data in load("constants").items()})
