from MentoDB import dataclass, BaseModel, PrimaryKey

@dataclass
class Films(BaseModel):
    id: PrimaryKey(int)
    is_active: int
    name: str
    rate: str
    kind: str
    related_words: str
    time: str
