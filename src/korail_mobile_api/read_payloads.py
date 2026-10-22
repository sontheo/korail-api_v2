"""Compatible request value objects."""

from korail_api.models.records import *


def build_self_seat_change_info_form(request: SelfSeatChangeInfoRequest) -> dict[str, str]:
    result = {
        "runDt": request.run_date,
        "trnNo": request.train_no,
        "dptRsStnCd": request.departure_station_code,
        "arvRsStnCd": request.arrival_station_code,
    }
    if request.room_class_code is not None:
        result["psrmClCd"] = request.room_class_code
    return result
