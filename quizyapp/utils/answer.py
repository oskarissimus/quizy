from typing import List
from ..models import Answer
from html import unescape


def get_or_create_answer_objects_from_opentdb_format(raw_question, question) -> List[Answer]:
    ret = []
    correct_answer_text = unescape(raw_question['correct_answer'])
    answer = Answer.objects.get_or_create(
        question=question, text=correct_answer_text, is_correct=True)
    ret.append(answer)

    for incorrect_answer_text in raw_question['incorrect_answers']:
        incorrect_answer_text = unescape(incorrect_answer_text)
        answer = Answer.objects.get_or_create(question=question, text=incorrect_answer_text, is_correct=False)
        ret.append(answer)
    return ret