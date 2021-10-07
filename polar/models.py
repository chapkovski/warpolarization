from otree.api import *
from .choices import *
from .constants import Constants
import json
import itertools
import random
from math import copysign

# TODO: Add footer
# TODO: add email to consent page
# TODO: add error counter
f = lambda x: f'{(x / 100):.2f}$'


class Subsession(BaseSubsession):
    treatment = models.StringField()


def creating_session(subsession):
    subsession.treatment = subsession.session.config.get('name')
    orders = [False, True]
    partner_positions = itertools.cycle([False, True])

    for p in subsession.get_players():
        c = sorted(REVEAL_CHOICES, key=lambda x: x[0], reverse=random.choice(orders))
        p.reveal_order = json.dumps(c)
        p.partner_position = next(partner_positions)
        p.egoendowment = Constants.DICTATOR_ENDOWMENT
        p.alterendowment = Constants.BASIC_ENDOWMENT


class Group(BaseGroup):
    pass


def reveal_choices(player):
    return json.loads(player.reveal_order)


class Player(BasePlayer):
    def html_dg_decision_choices(self):
        _choices = dg_decision_choices(self)
        res = []
        for i, j in enumerate(_choices):
            res.append(dict(id=i, value=j[0], label=j[1]))
        return res

    def cq_choices(self):
        return [dict(id=0, value=0, label='0$'),
                dict(id=1, value=50, label='0.50$'),
                dict(id=2, value=100, label='1.00$'),
                dict(id=3, value=150, label='1.50$'), ]

    def payoff_table(self):
        conv_ = {-1: 'Take', 0: 'Make no change', 1: 'Give'}

        def conv(v):
            if v == 0:
                return conv_[0]
            return conv_[copysign(1, v)]

        _choices = dg_decision_choices(self)

        res = []
        for i in _choices:
            res.append(dict(decision=i[1], ego=f(Constants.DICTATOR_ENDOWMENT - i[0]),
                            alter=f(Constants.BASIC_ENDOWMENT + i[0]),
                            label=conv(i[0])))
        return res

    partner_position = models.BooleanField()

    def get_partner_opinion(self):
        return 'AGREED' if self.partner_position else 'НЕ СОГЛАСЕН'

    @property
    def reverted_opinion(self):
        try:
            own_opinion = self.opinion_lgbt
            return 'disagree' if (self.opinion_lgbt) else 'agree'
        except TypeError:
            # just for debugging
            return 'disagree'

    def reverted_opinion_single(self):
        try:
            own_opinion = self.opinion_lgbt
            return 'disagrees' if (self.opinion_lgbt) else 'agrees'
        except TypeError:
            # just for debugging
            return 'disagrees'

    opinion_competition = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal,
                                              label='')
    opinion_lgbt = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal, label='')
    opinion_covid = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal, label='')

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
    cq1_ego = models.IntegerField(label=Constants.CQ_EGO_LABEL, choices=CQ_CHOICES,
                                  widget=widgets.RadioSelectHorizontal)
    cq1_alter = models.IntegerField(label=Constants.CQ_ALTER_LABEL, choices=CQ_CHOICES,
                                    widget=widgets.RadioSelectHorizontal)
    cq2_ego = models.IntegerField(label=Constants.CQ_EGO_LABEL, choices=CQ_CHOICES,
                                  widget=widgets.RadioSelectHorizontal)
    cq2_alter = models.IntegerField(label=Constants.CQ_ALTER_LABEL, choices=CQ_CHOICES,
                                    widget=widgets.RadioSelectHorizontal)
    cq3_ego = models.IntegerField(label=Constants.CQ_EGO_LABEL, choices=CQ_CHOICES,
                                  widget=widgets.RadioSelectHorizontal)
    cq3_alter = models.IntegerField(label=Constants.CQ_ALTER_LABEL, choices=CQ_CHOICES,
                                    widget=widgets.RadioSelectHorizontal)
    cq_err_counter = models.IntegerField(initial=0)
    #     main variables
    reveal_order = models.StringField()
    reveal = models.BooleanField()
    dg_decision = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    egoendowment = models.IntegerField()
    alterendowment = models.IntegerField()
    # BELIEFS:
    reveal_belief = models.IntegerField(min=0, max=100)
    dg_belief_ra = models.IntegerField()
    dg_belief_rb_nonrev = models.IntegerField()
    dg_belief_rb_rev_diff = models.IntegerField()
    dg_belief_rb_rev_same = models.IntegerField()
    dg_belief_fr_diff = models.IntegerField()
    dg_belief_fr_same = models.IntegerField()
    # DEMOGRAPHICS
    religion = models.IntegerField(label="""
    How strongly do you believe in the existence of a God or Gods? (indicate your answer on the range from 1 = not at all 5 = very much)
    """, choices=range(1, 6), widget=widgets.RadioSelectHorizontal)
    political = models.IntegerField(label="""
    Here is a 7-point scale on which the political views that people might hold are arranged from extremely liberal (left) to  extremely conservative (right). Where would you place yourself on this scale?
    """, choices=range(0, 8), widget=widgets.RadioSelectHorizontal)
    age = models.StringField(label='How old are you?', choices=AGE_CHOICES, widget=widgets.RadioSelect)
    education = models.StringField(label="What is the highest level of school you have completed or "
                                         "the highest degree you have received?",
                                   choices=EDUCATION_CHOICES, widget=widgets.RadioSelect)
    gender = models.StringField(label='What is your sex?',
                                choices=GENDER_CHOICES, widget=widgets.RadioSelect)
    marital = models.StringField(label='Are you now married, widowed, divorced, separated or never married?',
                                 choices=MARITAL_CHOICES, widget=widgets.RadioSelect)
    employment = models.StringField(label='Which statement best describes your current employment status?',
                                    choices=EMPLOYMENT_CHOICES, widget=widgets.RadioSelect)
    occupation = models.StringField(label='Please indicate your occupation:',
                                    choices=OCCUPATION_CHOICES, widget=widgets.RadioSelect)
    # Demand and clarity
    demand = models.LongStringField()
    instructions_clarity = models.IntegerField(label="""
    How understanble and clear were the instructions in this study for you? (indicate your answer on the range from 1 = not at all 5 = very much)
    """, choices=range(1, 6), widget=widgets.RadioSelectHorizontal)


def dg_decision_choices(player):
    ints = list(range(-50, 51, 10))

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
