from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'polar'
    players_per_group = None
    num_rounds = 1
    statement_lgbt = 'Представители ЛГБТ должны иметь такие же  права на заключение брака, как и люди гетеросексуальной ориентации.'
    privacy_note = 'ВНИМАНИЕ: <b>Только вы</b> можете видеть ответ участника Б на этот вопрос. Участник Б не имеет возможности посмотреть ваши ответы на любые вопросы. '
    ERR_MSG = 'Please re-read the instructions and check your answer'
    CQ_EGO_LABEL = 'Your bonus  (in cents):'
    CQ_ALTER_LABEL = 'Their bonus  (in cents):'
    BASIC_ENDOWMENT = 50
    EXTRA_ENDOWMENT = 50
    DICTATOR_ENDOWMENT = BASIC_ENDOWMENT + EXTRA_ENDOWMENT
    belief_bonus = 25
    formatted_belief_bonus =f'{(belief_bonus / 100):.2f}$'
    agreement_question='Согласны ли вы или не согласны со следующим утверждением?'
    NEXT_BTN='Далее'
    REQUIRED_MSG='Ответьте на вопрос'