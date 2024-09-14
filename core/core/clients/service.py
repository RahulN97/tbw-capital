from collections.abc import Collection, Mapping
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum, auto
from typing import Any, Dict, Literal, Optional, Type

from pydantic import BaseModel
from pydantic.main import IncEx


class HttpMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()


@dataclass(frozen=True)
class ServiceCall:
    endpoint: str
    http_method: HttpMethod
    request_type: Type
    response_type: Optional[Type]


class ApiBaseModel(BaseModel):

    def model_dump(
        self,
        *,
        mode: str | Literal["json"] | Literal["python"] = "python",
        include: Optional[Any] = None,
        exclude: Optional[IncEx] = None,
        context: Optional[IncEx] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none"] | Literal["warn"] | Literal["error"] = True,
        serialize_as_any: bool = False,
    ) -> Dict[str, Any]:
        data: Dict[str, Any] = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )
        return self._serialize(data)

    def _serialize(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.name
        if isinstance(obj, Mapping):
            return type(obj)({key: self._serialize(value) for key, value in obj.items()})
        if isinstance(obj, Collection) and not isinstance(obj, (str, bytes)):
            return type(obj)([self._serialize(item) for item in obj])
        if is_dataclass(obj):
            return {field.name: self._serialize(getattr(obj, field.name)) for field in fields(obj)}
        return obj
