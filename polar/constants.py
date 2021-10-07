from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'polar'
    players_per_group = None
    num_rounds = 1
    statement_lgbt = 'LGBT people should have the same opportunities to marry as people of heterosexual orientation.'
    privacy_note = 'NOTE: <b>Only you</b> are able to see Participant B’s answer to this question. Participant B remains unaware of any of your answers. '
    ERR_MSG = 'Please re-read the instructions and check your answer'
    CQ_EGO_LABEL = 'Your bonus  (in cents):'
    CQ_ALTER_LABEL = 'Their bonus  (in cents):'
    BASIC_ENDOWMENT = 50
    EXTRA_ENDOWMENT = 50
    DICTATOR_ENDOWMENT = BASIC_ENDOWMENT + EXTRA_ENDOWMENT
    belief_bonus = 25
    formatted_belief_bonus =f'{(belief_bonus / 100):.2f}$'