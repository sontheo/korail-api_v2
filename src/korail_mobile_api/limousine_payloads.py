"""Existing pure form APIs backed by the operation schema."""

from korail_api.protocol.forms import build


def build_limousine_schedule_form(config, query):
    return build("get_limousine_schedules", config, {"query": query})


def build_limousine_seat_inventory_form(config, query):
    return build("get_limousine_seat_inventory", config, {"query": query})
