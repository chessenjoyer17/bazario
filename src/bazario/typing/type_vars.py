from typing import TypeVar

from bazario.markers import Notification, Request

TDependency = TypeVar("TDependency")
TRes_co = TypeVar("TRes_co", covariant=True)
TReq_contra = TypeVar("TReq_contra", bound=Request, contravariant=True)
TNot_contra = TypeVar("TNot_contra", bound=Notification, contravariant=True)
TTarget_contra = TypeVar(
    "TTarget_contra",
    contravariant=True,
    bound=Request | Notification,
)
