from __future__ import annotations

import collections.abc
import typing
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from types import TracebackType
from typing import Any, Callable, Literal, Mapping, Self, Sequence

import httpx

from korail_api.api.client import KorailClient as KorailClient
from korail_api.api.facade import Korail as Korail
from korail_api.api.facade import ReservationResource as ReservationResource
from korail_api.api.facade import StationResource as StationResource
from korail_api.api.facade import TicketResource as TicketResource
from korail_api.api.facade import TrainResource as TrainResource
from korail_api.configuration.device import build_config_from_env as build_config_from_env
from korail_api.configuration.device import build_config_from_profile as build_config_from_profile
from korail_api.messages.catalog import get_error_message as get_error_message
from korail_api.messages.catalog import resolve_error_message as resolve_error_message
from korail_api.models.errors import KorailAccountLockedError as KorailAccountLockedError
from korail_api.models.errors import KorailAlreadyProcessedError as KorailAlreadyProcessedError
from korail_api.models.errors import KorailApiError as KorailApiError
from korail_api.models.errors import KorailAppError as KorailAppError
from korail_api.models.errors import KorailAppUpdateRequiredError as KorailAppUpdateRequiredError
from korail_api.models.errors import KorailAuthContinuationRequired as KorailAuthContinuationRequired
from korail_api.models.errors import KorailAuthError as KorailAuthError
from korail_api.models.errors import KorailDynaPathError as KorailDynaPathError
from korail_api.models.errors import KorailDynaPathRequiredError as KorailDynaPathRequiredError
from korail_api.models.errors import KorailInvalidRequestError as KorailInvalidRequestError
from korail_api.models.errors import KorailNetFunnelError as KorailNetFunnelError
from korail_api.models.errors import KorailNoDirectTrainError as KorailNoDirectTrainError
from korail_api.models.errors import KorailNoResultsError as KorailNoResultsError
from korail_api.models.errors import KorailNotEntitledError as KorailNotEntitledError
from korail_api.models.errors import KorailProcessingError as KorailProcessingError
from korail_api.models.errors import KorailProtocolError as KorailProtocolError
from korail_api.models.errors import KorailQueueRejectedError as KorailQueueRejectedError
from korail_api.models.errors import KorailRateLimitError as KorailRateLimitError
from korail_api.models.errors import KorailReservationRefusedError as KorailReservationRefusedError
from korail_api.models.errors import KorailSeatUnavailableError as KorailSeatUnavailableError
from korail_api.models.errors import KorailServiceUnavailableError as KorailServiceUnavailableError
from korail_api.models.errors import KorailSessionExpiredError as KorailSessionExpiredError
from korail_api.models.errors import KorailSoldOutError as KorailSoldOutError
from korail_api.models.errors import KorailTransportError as KorailTransportError
from korail_api.models.records import AppDataResponse as AppDataResponse
from korail_api.models.records import AppVersionInfo as AppVersionInfo
from korail_api.models.records import BaseKorailResponse as BaseKorailResponse
from korail_api.models.records import CardPayment as CardPayment
from korail_api.models.records import CartAddRequest as CartAddRequest
from korail_api.models.records import CartAddResponse as CartAddResponse
from korail_api.models.records import CartDiscountAddition as CartDiscountAddition
from korail_api.models.records import CartItem as CartItem
from korail_api.models.records import CartListResponse as CartListResponse
from korail_api.models.records import CommuterInfoRequest as CommuterInfoRequest
from korail_api.models.records import CommuterInfoResponse as CommuterInfoResponse
from korail_api.models.records import CommuterInitialRequest as CommuterInitialRequest
from korail_api.models.records import CommuterKindMenuResponse as CommuterKindMenuResponse
from korail_api.models.records import CommuterPassengerOption as CommuterPassengerOption
from korail_api.models.records import CommuterPassengerRequest as CommuterPassengerRequest
from korail_api.models.records import CommuterTicketInquiryRequest as CommuterTicketInquiryRequest
from korail_api.models.records import CrewRequestListResponse as CrewRequestListResponse
from korail_api.models.records import CrewRequestOption as CrewRequestOption
from korail_api.models.records import CustomerTripInfo as CustomerTripInfo
from korail_api.models.records import CustomerTripInfoResponse as CustomerTripInfoResponse
from korail_api.models.records import DelayCertificateResponse as DelayCertificateResponse
from korail_api.models.records import DelayCertificateRow as DelayCertificateRow
from korail_api.models.records import DelayDiscountTicket as DelayDiscountTicket
from korail_api.models.records import DelayDiscountTicketListResponse as DelayDiscountTicketListResponse
from korail_api.models.records import DelayReturnReceiptResponse as DelayReturnReceiptResponse
from korail_api.models.records import DeliveredTicketRetrievalResponse as DeliveredTicketRetrievalResponse
from korail_api.models.records import DeliveryRecipientResponse as DeliveryRecipientResponse
from korail_api.models.records import DepositBank as DepositBank
from korail_api.models.records import DepositBankListResponse as DepositBankListResponse
from korail_api.models.records import DiscountCardAdditionalUser as DiscountCardAdditionalUser
from korail_api.models.records import DiscountCardOnTicket as DiscountCardOnTicket
from korail_api.models.records import DiscountCardPurchaseRequest as DiscountCardPurchaseRequest
from korail_api.models.records import DiscountCardPurchaseResponse as DiscountCardPurchaseResponse
from korail_api.models.records import DiscountCardScheduleRequest as DiscountCardScheduleRequest
from korail_api.models.records import DiscountCardScheduleResponse as DiscountCardScheduleResponse
from korail_api.models.records import DiscountCardScheduleTrain as DiscountCardScheduleTrain
from korail_api.models.records import DiscountCardSection as DiscountCardSection
from korail_api.models.records import DiscountCardSectionRequest as DiscountCardSectionRequest
from korail_api.models.records import DiscountCardTicket as DiscountCardTicket
from korail_api.models.records import DiscountCardUsage as DiscountCardUsage
from korail_api.models.records import DiscountCardUsageListResponse as DiscountCardUsageListResponse
from korail_api.models.records import DiscountCoupon as DiscountCoupon
from korail_api.models.records import DiscountCouponListResponse as DiscountCouponListResponse
from korail_api.models.records import DynapathConfig as DynapathConfig
from korail_api.models.records import DynapathRequestContext as DynapathRequestContext
from korail_api.models.records import DynapathTokenProvider as DynapathTokenProvider
from korail_api.models.records import DynapathTokenSettings as DynapathTokenSettings
from korail_api.models.records import FreeSeatCarRequest as FreeSeatCarRequest
from korail_api.models.records import FreeSeatCarResponse as FreeSeatCarResponse
from korail_api.models.records import GuideSeatConditionRequest as GuideSeatConditionRequest
from korail_api.models.records import GuideSeatConditionResponse as GuideSeatConditionResponse
from korail_api.models.records import IntermediateStation as IntermediateStation
from korail_api.models.records import KorailConfig as KorailConfig
from korail_api.models.records import KorailDeviceProfile as KorailDeviceProfile
from korail_api.models.records import KorailLoginInputFlag as KorailLoginInputFlag
from korail_api.models.records import KorailMileageLedger as KorailMileageLedger
from korail_api.models.records import KorailMileageMovement as KorailMileageMovement
from korail_api.models.records import KorailPassengerCounts as KorailPassengerCounts
from korail_api.models.records import KorailPointSummaryResponse as KorailPointSummaryResponse
from korail_api.models.records import KorailReservationJobType as KorailReservationJobType
from korail_api.models.records import KorailReserveOption as KorailReserveOption
from korail_api.models.records import KorailRoomClassCode as KorailRoomClassCode
from korail_api.models.records import KorailSeatAssignment as KorailSeatAssignment
from korail_api.models.records import KorailSeatClass as KorailSeatClass
from korail_api.models.records import KorailSelfSeatChangeRoomClassCode as KorailSelfSeatChangeRoomClassCode
from korail_api.models.records import KorailSession as KorailSession
from korail_api.models.records import KorailStation as KorailStation
from korail_api.models.records import LimousineSchedule as LimousineSchedule
from korail_api.models.records import LimousineScheduleQuery as LimousineScheduleQuery
from korail_api.models.records import LimousineScheduleResponse as LimousineScheduleResponse
from korail_api.models.records import LimousineSeat as LimousineSeat
from korail_api.models.records import LimousineSeatInventoryQuery as LimousineSeatInventoryQuery
from korail_api.models.records import LimousineSeatInventoryResponse as LimousineSeatInventoryResponse
from korail_api.models.records import MaasMenuItem as MaasMenuItem
from korail_api.models.records import MaasMenuListResponse as MaasMenuListResponse
from korail_api.models.records import MaasServiceDetail as MaasServiceDetail
from korail_api.models.records import MaasServiceDetailInfo as MaasServiceDetailInfo
from korail_api.models.records import MaasServiceDetailListResponse as MaasServiceDetailListResponse
from korail_api.models.records import MaasServiceDetailQuery as MaasServiceDetailQuery
from korail_api.models.records import MergeSeatsInquiryRequest as MergeSeatsInquiryRequest
from korail_api.models.records import MergeSeatsInquiryResponse as MergeSeatsInquiryResponse
from korail_api.models.records import MileageHistoryEntry as MileageHistoryEntry
from korail_api.models.records import MileageHistoryRequest as MileageHistoryRequest
from korail_api.models.records import MileageHistoryResponse as MileageHistoryResponse
from korail_api.models.records import MultiChildDiscountTarget as MultiChildDiscountTarget
from korail_api.models.records import MultiChildDiscountTargetResponse as MultiChildDiscountTargetResponse
from korail_api.models.records import NoticeResponse as NoticeResponse
from korail_api.models.records import OriginalTicket as OriginalTicket
from korail_api.models.records import OriginalTicketInquiryResponse as OriginalTicketInquiryResponse
from korail_api.models.records import OriginalTicketJourney as OriginalTicketJourney
from korail_api.models.records import OriginalTicketReference as OriginalTicketReference
from korail_api.models.records import OriginalTicketSeat as OriginalTicketSeat
from korail_api.models.records import PaidTicket as PaidTicket
from korail_api.models.records import PassAgeOption as PassAgeOption
from korail_api.models.records import PassAvailabilityMainInfo as PassAvailabilityMainInfo
from korail_api.models.records import PassAvailabilityResponse as PassAvailabilityResponse
from korail_api.models.records import PassGoodsInfo as PassGoodsInfo
from korail_api.models.records import PassMenuData as PassMenuData
from korail_api.models.records import PassMenuItem as PassMenuItem
from korail_api.models.records import PassMenuResponse as PassMenuResponse
from korail_api.models.records import PassOffice as PassOffice
from korail_api.models.records import PassOpenDate as PassOpenDate
from korail_api.models.records import PassPassengerInfo as PassPassengerInfo
from korail_api.models.records import PassPassengerInfos as PassPassengerInfos
from korail_api.models.records import PassPeriodOption as PassPeriodOption
from korail_api.models.records import PassScheduleInfo as PassScheduleInfo
from korail_api.models.records import PassScheduleMainInfo as PassScheduleMainInfo
from korail_api.models.records import PassScheduleRequest as PassScheduleRequest
from korail_api.models.records import PassScheduleResponse as PassScheduleResponse
from korail_api.models.records import PassScheduleTrain as PassScheduleTrain
from korail_api.models.records import PbpAcceptanceJourney as PbpAcceptanceJourney
from korail_api.models.records import PbpAcceptanceSeat as PbpAcceptanceSeat
from korail_api.models.records import PbpAcceptanceSpecificationResponse as PbpAcceptanceSpecificationResponse
from korail_api.models.records import PbpAcceptanceTicket as PbpAcceptanceTicket
from korail_api.models.records import PhysicalSeat as PhysicalSeat
from korail_api.models.records import PriceFare as PriceFare
from korail_api.models.records import PriceFareLeg as PriceFareLeg
from korail_api.models.records import PriceFareQuoteRequest as PriceFareQuoteRequest
from korail_api.models.records import PriceFareQuoteResponse as PriceFareQuoteResponse
from korail_api.models.records import PriceRecalculationRequest as PriceRecalculationRequest
from korail_api.models.records import PriceRecalculationRow as PriceRecalculationRow
from korail_api.models.records import ProductCancelResponse as ProductCancelResponse
from korail_api.models.records import ProductDetailResponse as ProductDetailResponse
from korail_api.models.records import ProductReservation as ProductReservation
from korail_api.models.records import ProductReservationListResponse as ProductReservationListResponse
from korail_api.models.records import ReceiptCashPayment as ReceiptCashPayment
from korail_api.models.records import ReceiptPayment as ReceiptPayment
from korail_api.models.records import RecentDeliveryHistoryResponse as RecentDeliveryHistoryResponse
from korail_api.models.records import RecentDeliveryRecipient as RecentDeliveryRecipient
from korail_api.models.records import RefundCommissionResponse as RefundCommissionResponse
from korail_api.models.records import RefundCompanion as RefundCompanion
from korail_api.models.records import RefundTicketDetailResponse as RefundTicketDetailResponse
from korail_api.models.records import RefundTicketJourney as RefundTicketJourney
from korail_api.models.records import RefundTicketResponse as RefundTicketResponse
from korail_api.models.records import RefundTicketSeat as RefundTicketSeat
from korail_api.models.records import ReservationDetailJourney as ReservationDetailJourney
from korail_api.models.records import ReservationHistoryJourney as ReservationHistoryJourney
from korail_api.models.records import ReservationHistoryOriginalTicket as ReservationHistoryOriginalTicket
from korail_api.models.records import ReservationHistoryPassenger as ReservationHistoryPassenger
from korail_api.models.records import ReservationHistoryReservation as ReservationHistoryReservation
from korail_api.models.records import ReservationHistoryResponse as ReservationHistoryResponse
from korail_api.models.records import ReservationHistoryTicket as ReservationHistoryTicket
from korail_api.models.records import ReservationHistoryTrain as ReservationHistoryTrain
from korail_api.models.records import ReservationHoldResponse as ReservationHoldResponse
from korail_api.models.records import ReservationJourney as ReservationJourney
from korail_api.models.records import ReservationPassengerInfo as ReservationPassengerInfo
from korail_api.models.records import ReservationPaymentCoupon as ReservationPaymentCoupon
from korail_api.models.records import ReservationPaymentResponse as ReservationPaymentResponse
from korail_api.models.records import ReservationPaymentSettlement as ReservationPaymentSettlement
from korail_api.models.records import ReservationPaymentTableSeat as ReservationPaymentTableSeat
from korail_api.models.records import ReservationPaymentTicket as ReservationPaymentTicket
from korail_api.models.records import ReservationSeatDetail as ReservationSeatDetail
from korail_api.models.records import SeatAssignmentScheduleRequest as SeatAssignmentScheduleRequest
from korail_api.models.records import SeatAssignmentScheduleResponse as SeatAssignmentScheduleResponse
from korail_api.models.records import SeatAttribute as SeatAttribute
from korail_api.models.records import SeatCar as SeatCar
from korail_api.models.records import SeatCarListResponse as SeatCarListResponse
from korail_api.models.records import SeatInventoryResponse as SeatInventoryResponse
from korail_api.models.records import SeatWindow as SeatWindow
from korail_api.models.records import SelfCheckInCancelResponse as SelfCheckInCancelResponse
from korail_api.models.records import SelfCheckInInfoResponse as SelfCheckInInfoResponse
from korail_api.models.records import SelfCheckInRegisterResponse as SelfCheckInRegisterResponse
from korail_api.models.records import SelfCheckInSeat as SelfCheckInSeat
from korail_api.models.records import SelfCheckInSeatCheckResponse as SelfCheckInSeatCheckResponse
from korail_api.models.records import SelfSeatChangeInfoRequest as SelfSeatChangeInfoRequest
from korail_api.models.records import SelfSeatChangeInfoResponse as SelfSeatChangeInfoResponse
from korail_api.models.records import SelfSeatChangeReason as SelfSeatChangeReason
from korail_api.models.records import SelfSeatChangeStation as SelfSeatChangeStation
from korail_api.models.records import ServiceStatusResponse as ServiceStatusResponse
from korail_api.models.records import StationDataResponse as StationDataResponse
from korail_api.models.records import StationInfoResponse as StationInfoResponse
from korail_api.models.records import StationRefundExecutionRequest as StationRefundExecutionRequest
from korail_api.models.records import StationRefundExecutionResponse as StationRefundExecutionResponse
from korail_api.models.records import StationRefundOriginalTicket as StationRefundOriginalTicket
from korail_api.models.records import StationRefundVerificationRequest as StationRefundVerificationRequest
from korail_api.models.records import StationRefundVerificationResponse as StationRefundVerificationResponse
from korail_api.models.records import TicketDuplicationCheckRequest as TicketDuplicationCheckRequest
from korail_api.models.records import TicketDuplicationCheckResponse as TicketDuplicationCheckResponse
from korail_api.models.records import TicketListReservation as TicketListReservation
from korail_api.models.records import TicketListResponse as TicketListResponse
from korail_api.models.records import TicketListTicket as TicketListTicket
from korail_api.models.records import TicketListTrain as TicketListTrain
from korail_api.models.records import TicketReceipt as TicketReceipt
from korail_api.models.records import TicketReceiptResponse as TicketReceiptResponse
from korail_api.models.records import TicketReservationDetailRequest as TicketReservationDetailRequest
from korail_api.models.records import TicketReservationDetailResponse as TicketReservationDetailResponse
from korail_api.models.records import TrainCalendarDay as TrainCalendarDay
from korail_api.models.records import TrainCalendarResponse as TrainCalendarResponse
from korail_api.models.records import TrainScheduleItem as TrainScheduleItem
from korail_api.models.records import TrainScheduleResponse as TrainScheduleResponse
from korail_api.models.records import TrainScheduleStop as TrainScheduleStop
from korail_api.models.records import TrainSearchContinuation as TrainSearchContinuation
from korail_api.models.records import TrainSearchMetadata as TrainSearchMetadata
from korail_api.models.records import TrainSearchQuery as TrainSearchQuery
from korail_api.models.records import TrainSearchResult as TrainSearchResult
from korail_api.models.records import TrainSummary as TrainSummary
from korail_api.models.records import TransferItinerary as TransferItinerary
from korail_api.models.records import TransferSearchResult as TransferSearchResult
from korail_api.models.records import TransferStation as TransferStation
from korail_api.models.records import TransferStationListResponse as TransferStationListResponse
from korail_api.models.records import TripChangeDateResponse as TripChangeDateResponse
from korail_api.models.records import TripMenuContent as TripMenuContent
from korail_api.models.records import TripMenuItem as TripMenuItem
from korail_api.models.records import TripMenuResponse as TripMenuResponse
from korail_api.models.records import UuidResponse as UuidResponse

__version__: str
__all__ = [
    "AppDataResponse",
    "AppVersionInfo",
    "BaseKorailResponse",
    "CartAddRequest",
    "CartAddResponse",
    "CartDiscountAddition",
    "CartItem",
    "CartListResponse",
    "CommuterKindMenuResponse",
    "CommuterInfoRequest",
    "CommuterInfoResponse",
    "CommuterInitialRequest",
    "CommuterPassengerOption",
    "CommuterPassengerRequest",
    "CommuterTicketInquiryRequest",
    "CrewRequestListResponse",
    "CrewRequestOption",
    "CustomerTripInfo",
    "CustomerTripInfoResponse",
    "DelayCertificateResponse",
    "DelayCertificateRow",
    "DelayReturnReceiptResponse",
    "DeliveredTicketRetrievalResponse",
    "DynapathConfig",
    "DynapathRequestContext",
    "DynapathTokenProvider",
    "DynapathTokenSettings",
    "DelayDiscountTicket",
    "DelayDiscountTicketListResponse",
    "DeliveryRecipientResponse",
    "DepositBank",
    "DepositBankListResponse",
    "DiscountCardScheduleRequest",
    "DiscountCardAdditionalUser",
    "DiscountCardOnTicket",
    "DiscountCardPurchaseRequest",
    "DiscountCardPurchaseResponse",
    "DiscountCardScheduleResponse",
    "DiscountCardScheduleTrain",
    "DiscountCardSection",
    "DiscountCardSectionRequest",
    "DiscountCardTicket",
    "DiscountCardUsage",
    "DiscountCardUsageListResponse",
    "DiscountCoupon",
    "DiscountCouponListResponse",
    "FreeSeatCarRequest",
    "FreeSeatCarResponse",
    "GuideSeatConditionRequest",
    "GuideSeatConditionResponse",
    "IntermediateStation",
    "Korail",
    "KorailAccountLockedError",
    "KorailAlreadyProcessedError",
    "KorailApiError",
    "KorailAppError",
    "KorailAppUpdateRequiredError",
    "KorailAuthContinuationRequired",
    "KorailAuthError",
    "KorailClient",
    "KorailConfig",
    "KorailDeviceProfile",
    "KorailDynaPathError",
    "KorailDynaPathRequiredError",
    "KorailInvalidRequestError",
    "KorailNetFunnelError",
    "KorailNoDirectTrainError",
    "KorailNoResultsError",
    "KorailNotEntitledError",
    "KorailProcessingError",
    "KorailRateLimitError",
    "KorailPassengerCounts",
    "KorailQueueRejectedError",
    "KorailLoginInputFlag",
    "KorailRoomClassCode",
    "KorailReservationJobType",
    "KorailReserveOption",
    "KorailReservationRefusedError",
    "KorailProtocolError",
    "KorailSeatAssignment",
    "KorailSeatClass",
    "KorailSeatUnavailableError",
    "KorailServiceUnavailableError",
    "KorailStation",
    "KorailSession",
    "KorailSessionExpiredError",
    "KorailSoldOutError",
    "KorailTransportError",
    "get_error_message",
    "resolve_error_message",
    "LimousineSchedule",
    "LimousineScheduleQuery",
    "LimousineScheduleResponse",
    "LimousineSeat",
    "LimousineSeatInventoryQuery",
    "LimousineSeatInventoryResponse",
    "MaasMenuItem",
    "MaasMenuListResponse",
    "MaasServiceDetail",
    "MaasServiceDetailInfo",
    "MaasServiceDetailListResponse",
    "MaasServiceDetailQuery",
    "MergeSeatsInquiryRequest",
    "MergeSeatsInquiryResponse",
    "KorailMileageLedger",
    "KorailMileageMovement",
    "KorailPointSummaryResponse",
    "KorailSelfSeatChangeRoomClassCode",
    "MileageHistoryEntry",
    "MileageHistoryRequest",
    "MileageHistoryResponse",
    "MultiChildDiscountTarget",
    "MultiChildDiscountTargetResponse",
    "NoticeResponse",
    "OriginalTicket",
    "OriginalTicketInquiryResponse",
    "OriginalTicketJourney",
    "OriginalTicketReference",
    "OriginalTicketSeat",
    "PhysicalSeat",
    "PassAvailabilityMainInfo",
    "PassAvailabilityResponse",
    "PassAgeOption",
    "PassGoodsInfo",
    "PassMenuData",
    "PassMenuItem",
    "PassMenuResponse",
    "PassScheduleInfo",
    "PassScheduleMainInfo",
    "PassScheduleRequest",
    "PassScheduleResponse",
    "PassScheduleTrain",
    "PassOffice",
    "PassOpenDate",
    "PassPassengerInfo",
    "PassPassengerInfos",
    "PassPeriodOption",
    "PbpAcceptanceJourney",
    "PbpAcceptanceSeat",
    "PbpAcceptanceSpecificationResponse",
    "PbpAcceptanceTicket",
    "ProductCancelResponse",
    "ProductDetailResponse",
    "ProductReservation",
    "ProductReservationListResponse",
    "PriceFare",
    "PriceFareLeg",
    "PriceFareQuoteRequest",
    "PriceFareQuoteResponse",
    "RecentDeliveryHistoryResponse",
    "RecentDeliveryRecipient",
    "ReceiptCashPayment",
    "ReceiptPayment",
    "RefundCommissionResponse",
    "RefundCompanion",
    "RefundTicketDetailResponse",
    "RefundTicketJourney",
    "RefundTicketSeat",
    "RefundTicketResponse",
    "SelfCheckInCancelResponse",
    "SelfCheckInInfoResponse",
    "SelfCheckInRegisterResponse",
    "SelfCheckInSeat",
    "SelfCheckInSeatCheckResponse",
    "StationRefundExecutionRequest",
    "StationRefundExecutionResponse",
    "StationRefundOriginalTicket",
    "StationRefundVerificationRequest",
    "StationRefundVerificationResponse",
    "ReservationDetailJourney",
    "ReservationHistoryJourney",
    "ReservationHistoryOriginalTicket",
    "ReservationHistoryPassenger",
    "ReservationHistoryReservation",
    "ReservationHistoryResponse",
    "ReservationHistoryTicket",
    "ReservationHistoryTrain",
    "ReservationSeatDetail",
    "CardPayment",
    "PaidTicket",
    "PriceRecalculationRequest",
    "PriceRecalculationRow",
    "ReservationHoldResponse",
    "ReservationResource",
    "ReservationJourney",
    "ReservationPaymentCoupon",
    "ReservationPaymentResponse",
    "ReservationPaymentSettlement",
    "ReservationPaymentTableSeat",
    "ReservationPaymentTicket",
    "ReservationPassengerInfo",
    "SeatAttribute",
    "SeatCar",
    "SeatCarListResponse",
    "SeatInventoryResponse",
    "SeatAssignmentScheduleRequest",
    "SeatAssignmentScheduleResponse",
    "SeatWindow",
    "SelfSeatChangeInfoRequest",
    "SelfSeatChangeInfoResponse",
    "SelfSeatChangeReason",
    "SelfSeatChangeStation",
    "ServiceStatusResponse",
    "StationResource",
    "build_config_from_env",
    "build_config_from_profile",
    "StationDataResponse",
    "StationInfoResponse",
    "TrainCalendarDay",
    "TrainCalendarResponse",
    "TrainSearchContinuation",
    "TrainSearchQuery",
    "TrainSearchMetadata",
    "TrainSearchResult",
    "TrainScheduleResponse",
    "TrainScheduleStop",
    "TrainScheduleItem",
    "TrainSummary",
    "TrainResource",
    "TransferItinerary",
    "TransferSearchResult",
    "TicketReceipt",
    "TicketReceiptResponse",
    "TicketReservationDetailRequest",
    "TicketReservationDetailResponse",
    "TicketDuplicationCheckRequest",
    "TicketDuplicationCheckResponse",
    "TicketListReservation",
    "TicketListResponse",
    "TicketListTicket",
    "TicketListTrain",
    "TicketResource",
    "TripMenuContent",
    "TripMenuItem",
    "TripMenuResponse",
    "TripChangeDateResponse",
    "TransferStation",
    "TransferStationListResponse",
    "UuidResponse",
]
