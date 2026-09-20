from pydantic import BaseModel
from typing import List, Optional


class FlashcardRequest(BaseModel):
    topic: str = ""
    subject_id: Optional[int] = None
    number_of_cards: int = 8


class FlashcardItem(BaseModel):
    front: str
    back: str


class FlashcardResponse(BaseModel):
    cards: List[FlashcardItem]
