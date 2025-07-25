from pydantic import BaseModel
from typing import Any, Optional

class EmailRequest(BaseModel):
    content: str