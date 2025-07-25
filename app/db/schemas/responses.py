from enum import Enum
from pydantic import BaseModel
from typing import Any, Optional

class StatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"

class APIResponse(BaseModel):
    status: StatusEnum
    data: Optional[Any] = None
    error_message: Optional[str] = None
    detailed_message: Optional[str] = None
    error_code: Optional[int] = None
