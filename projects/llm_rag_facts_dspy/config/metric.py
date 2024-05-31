from dspy.evaluate import answer_exact_match, answer_passage_match


# Validation logic: check that the predicted answer is correct.
# Also check that the retrieved context does actually contain that answer.
def validate_context_and_answer(example, pred, trace=None):
    answer_em = answer_exact_match(example, pred)
    answer_pm = answer_passage_match(example, pred)
    return answer_em and answer_pm


def get_metric():
    return validate_context_and_answer
