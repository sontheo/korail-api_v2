"""Compatible parser entrypoints, implemented by the new decoding engine."""

from korail_api.protocol.parsers import _validate_envelope, install

install(globals(), __name__)
