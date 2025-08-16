from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    filename: str
    chunks: int

class QueryRequest(BaseModel):
    filename: str
    question: str
    use_outside_knowledge: bool = False

class AnswerResponse(BaseModel):
    answer: str
    context: List[str]
