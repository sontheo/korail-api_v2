"""Existing airport bus form API backed by the independent request engine."""

from korail_api.protocol.forms import build


def build_limousine_reservation_form(config, schedule, seat_nos, *, passengers=None, car_no="0001"):
    from korail_api.services.validation import text

    text(car_no, "Car number")
    result = build(
        "reserve_limousine", config, {"schedule": schedule, "seat_nos": seat_nos, "passengers": passengers}
    )
    for key in result:
        if key.startswith("txtSrcarNo"):
            result[key] = car_no
    return result


def build_card_payment_form(config, hold, card):
    return build("pay_with_card", config, {"hold": hold, "card": card})


def build_transfer_reservation_form(config, legs, **options):
    return build("reserve_transfer", config, {"legs": legs, **options})


def build_refund_form(config, ticket, **options):
    from korail_api.models.errors import KorailProtocolError

    if options.get("commission") is None:
        raise KorailProtocolError("Refund requires a commission response")
    return build("refund", config, {"ticket": ticket, **options})
