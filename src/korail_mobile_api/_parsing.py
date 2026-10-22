"""Small compatibility parsing utilities backed by the independent codec."""

from collections.abc import Mapping

from korail_api.protocol.codec import decode, scalar


def _nullable_scalar_fields(data, field_map, context=""):
    return {name: scalar(data.get(wire)) for name, wire in field_map.items()}


def _reservation_passengers(raw):
    container = raw.get("psg_infos")
    rows = container.get("psg_info") if isinstance(container, Mapping) else None
    if not isinstance(rows, list):
        return ()
    return tuple(decode("ReservationPassengerInfo", dict(row)) for row in rows if isinstance(row, Mapping))
