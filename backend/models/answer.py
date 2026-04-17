from dataclasses import dataclass
from datetime import datetime


@dataclass
class AnswerSubmission:
    submission_id: str
    answers: dict
    submitted_at: str

    @classmethod
    def create(cls, answers: dict) -> 'AnswerSubmission':
        import uuid
        return cls(
            submission_id=str(uuid.uuid4()),
            answers=answers,
            submitted_at=datetime.utcnow().isoformat() + 'Z'
        )

    def to_dict(self) -> dict:
        return {
            'submission_id': self.submission_id,
            'answers': self.answers,
            'submitted_at': self.submitted_at,
        }
