from otree.api import *
from .choices import *


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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
    reason_dg = models.LongStringField(label='Please think back to your decision regarding giving money to or taking money from the Participant B you were matched with or leaving his account unchanged. What influenced you in your decision, what were your decision motives? ')
    keyword_dg_1 = models.StringField()
    keyword_dg_2 = models.StringField()
    keyword_dg_3 = models.StringField()
    reason_reveal = models.LongStringField(label="""Please think back to your decision regarding observing or not observing Participant B’s opinion. What influenced you in your decision, what were your decision motives? """)
    keyword_rev_1 = models.StringField()
    keyword_rev_2 = models.StringField()
    keyword_rev_3 = models.StringField()
