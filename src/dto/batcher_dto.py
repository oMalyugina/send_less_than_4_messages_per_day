import datetime

from pydantic import BaseModel


class UserMessage(BaseModel):
    timestamp: str
    to_id: str
    from_id: str
    from_name: str


class ResetTimerDTO(BaseModel):
    real_time_start: datetime.datetime
    virtual_time_start: datetime.datetime
    multiplier: int
