from pydantic import BaseModel
from langchain_core.tools import StructuredTool

class ToolInputs(BaseModel):
    complaint: str
    user_email: str

class QuestionInput(BaseModel):
    question: str
    user_email: str

class ClassifyInput(BaseModel):
    question: str
    user_email: str