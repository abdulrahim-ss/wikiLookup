from aqt.gui_hooks import reviewer_did_show_answer, reviewer_did_show_question
from aqt import mw

class reviewer_checker:
    """
        Check whether the answer of the card is shown or not yet. It allows the configuration of whether the
        add-on will trigger only when answer is shown or whenever.
    """
    def __init__(self):
        reviewer_did_show_answer.append(self.on_reviewer_did_show_answer)
        reviewer_did_show_question.append(self.on_reviewer_did_show_question)

    def on_reviewer_did_show_answer(self, card) -> None:
        """
            Executes 'answer_is_shown()' function which is located in 'web/wikiLookup.js > answer_is_shown()'
        """
        mw.web.eval("answer_is_shown();")
    
    def on_reviewer_did_show_question(self, card) -> None:
        """
            Executes 'question_is_shown()' function which is located in 'web/wikiLookup.js > question_is_shown()'
        """
        mw.web.eval("question_is_shown();")
