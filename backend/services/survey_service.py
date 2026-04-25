from ..models import Question, AnswerSubmission


class SurveyService:
    QUESTIONS = [
        Question(
            id='q1',
            text='Как вас зовут?',
            type='text'
        ),
        Question(
            id='q2',
            text='Ваш возраст?',
            type='text'
        ),
        Question(
            id='q3',
            text='Оцените качество курса',
            type='radio',
            options=['1', '2', '3', '4', '5']
        ),
        Question(
            id='q4',
            text='Что вам понравилось больше всего?',
            type='text'
        ),
        Question(
            id='q5',
            text='Рекомендовали бы вы этот курс другим?',
            type='radio',
            options=['Да', 'Нет', 'Возможно']
        ),
    ]

    def __init__(self):
        self._storage = {}

    def get_questions(self) -> list:
        return [q.to_dict() for q in self.QUESTIONS]

    def save_answers(self, answers_data: dict) -> dict:
        submission = AnswerSubmission.create(answers_data)
        self._storage[submission.submission_id] = submission
        return submission.to_dict()

    def get_submissions(self) -> list:
        return [s.to_dict() for s in self._storage.values()]
