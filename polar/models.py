from otree.api import *
from .choices import *
from .constants import Constants
import json
import itertools


class Subsession(BaseSubsession):
    treatment = models.StringField()


def creating_session(subsession):
    subsession.treatment = subsession.session.config.get('name')
    orders = itertools.cycle([False, True])
    for p in subsession.get_players():
        c = sorted(REVEAL_CHOICES, key=lambda x: x[0], reverse=next(orders))
        p.reveal_order = json.dumps(c)


class Group(BaseGroup):
    pass


import random


#  TODO - potentially
# TODO: 1. randomize choice order in opinions 1-3
# TODO: 2. Randomice choice order in revealing (!)

def reveal_choices(player):
    return json.loads(player.reveal_order)


class Player(BasePlayer):
    def get_partner_opinion(self):
        return 'AGREED'

    opinion_competition = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal, label='')
    opinion_lgbt = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal, label='')
    opinion_covid = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal, label='')

    religion = models.IntegerField(label="""
    How strongly do you believe in the existence of a God or Gods? (indicate your answer on the range from 1 = not at all 5 = very much)
    """, choices=range(1, 6))
    political = models.IntegerField(label="""
    Here is a 7-point scale on which the political views that people might hold are arranged from extremely liberal (left) to  extremely conservative (right). Where would you place yourself on this scale?
    """, choices=range(0, 8))
    age = models.StringField(label='How old are you?', choices=AGE_CHOICES)
    education = models.StringField(label="What is the highest level of school you have completed or "
                                         "the highest degree you have received?",
                                   choices=EDUCATION_CHOICES)
    gender = models.StringField(label='What is your sex?',
                                choices=GENDER_CHOICES)
    marital = models.StringField(label='What is your sex?',
                                 choices=MARITAL_CHOICES)
    employment = models.StringField(label='What is your sex?',
                                    choices=EMPLOYMENT_CHOICES)
    occupation = models.StringField(label='Please indicate your occupation',
                                    choices=OCCUPATION_CHOICES)

    risk_general = models.IntegerField()
    risk_financial_matters = models.IntegerField()
    risk_free = models.IntegerField()
    risk_profession = models.IntegerField()
    risk_health = models.IntegerField()
    risk_strangers = models.IntegerField()
    risk_driving = models.IntegerField()
    sdi_politics = models.StringField()
    sdi_neighbors = models.StringField()
    sdi_friends = models.StringField()
    sdi_family = models.StringField()
    scs_habits = models.IntegerField()
    scs_why = models.IntegerField()
    scs_conversation = models.IntegerField()
    scs_listening = models.IntegerField()
    scs_quarrel = models.IntegerField()
    ias_friend = models.StringField()
    ias_coworker = models.StringField()
    ias_stranger = models.StringField()
    # REASONS
    reason_dg = models.LongStringField(
        label='Please think back to your decision regarding giving money to or taking money from the Participant B you were matched with or leaving his account unchanged. What influenced you in your decision, what were your decision motives? ')
    keyword_dg_1 = models.StringField()
    keyword_dg_2 = models.StringField()
    keyword_dg_3 = models.StringField()
    reason_reveal = models.LongStringField(
        label="""Please think back to your decision regarding observing or not observing Participant B’s opinion. What influenced you in your decision, what were your decision motives? """)
    keyword_rev_1 = models.StringField()
    keyword_rev_2 = models.StringField()
    keyword_rev_3 = models.StringField()
    # Comprehension questions
    cq1_ego = models.IntegerField(label=Constants.CQ_EGO_LABEL)
    cq1_alter = models.IntegerField(label=Constants.CQ_ALTER_LABEL)
    cq2_ego = models.IntegerField(label=Constants.CQ_EGO_LABEL)
    cq2_alter = models.IntegerField(label=Constants.CQ_ALTER_LABEL)
    cq3_ego = models.IntegerField(label=Constants.CQ_EGO_LABEL)
    cq3_alter = models.IntegerField(label=Constants.CQ_ALTER_LABEL)
    #     main variables
    reveal_order = models.StringField()
    reveal = models.BooleanField()
    dg_decision = models.IntegerField(widget=widgets.RadioSelectHorizontal
                                      )


def dg_decision_choices(player):
    ints = list(range(-50, 51, 10))
    f = lambda x: f'{(x / 100):.2f}$'
    return [(i, f(i)) for i in ints]


def cq1_ego_error_message(player, value):
    if value != 50:
        return Constants.ERR_MSG


def cq1_alter_error_message(player, value):
    if value != 100:
        return Constants.ERR_MSG


def cq2_ego_error_message(player, value):
    if value != 100:
        return Constants.ERR_MSG


def cq2_alter_error_message(player, value):
    if value != 50:
        return Constants.ERR_MSG


def cq3_ego_error_message(player, value):
    if value != 150:
        return Constants.ERR_MSG


def cq3_alter_error_message(player, value):
    if value != 0:
        return Constants.ERR_MSG
