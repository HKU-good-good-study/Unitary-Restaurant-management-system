from datetime import datetime
from typing import Any, Self
from zoneinfo import ZoneInfo

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, model_validator


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: convert_datetime_to_gmt},
        populate_by_name=True,
    )

    # @model_validator(mode="after")
    # @classmethod
    # def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
    #     datetime_fields = {
    #         k: v.replace(microsecond=0)
    #         for k, v in data.items()
    #         if isinstance(v, datetime)
    #     }
    #
    #     return {**data, **datetime_fields}

    @model_validator(mode="after")
    def set_null_microseconds(self) -> Self:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in self.model_dump().items()
            if isinstance(v, datetime)
        }

        return self.model_copy(update=datetime_fields)


    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)