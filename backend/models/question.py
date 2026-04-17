from dataclasses import dataclass


@dataclass
class Question:
    id: str
    text: str
    type: str
    options: list[str] = None

    def __post_init__(self):
        if self.options is None:
            self.options = []

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'text': self.text,
            'type': self.type,
            'options': self.options,
        }
