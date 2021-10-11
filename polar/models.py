from otree.api import *
from .choices import *
from .constants import Constants
import json
import itertools
import random
from math import copysign

# TODO: remove proportions from methods
# TODO: write down the logic of treatment
# TODO: what to do with recipieints?
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
    # Main vars
    opinion_lgbt = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal, label='')
    partner_position = models.BooleanField()
    aligned = models.BooleanField()
    reveal = models.BooleanField()
    dg_decision = models.IntegerField(widget=widgets.RadioSelectHorizontal)
    payable = models.BooleanField()
    cq_err_counter = models.IntegerField(initial=0)
    blocked = models.BooleanField(initial=False)

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
        conv_ = {-1: 'Взять', 0: 'Оставить без изменений', 1: 'Отдать'}

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

    def get_partner_opinion(self):
        return 'СОГЛАСИЛСЯ' if self.partner_position else 'НЕ СОГЛАСИЛСЯ'

    @property
    def reverted_opinion(self):
        try:
            return 'не согласны' if (self.opinion_lgbt) else 'согласны'
        except TypeError:
            # just for debugging
            return 'не согласны'

    def reverted_opinion_single(self):
        try:
            return 'не согласен' if (self.opinion_lgbt) else 'согласен'
        except TypeError:
            # just for debugging
            return 'не согласен'

    opinion_competition = models.BooleanField(choices=OPINION_CHOICES, widget=widgets.RadioSelectHorizontal,
                                              label='')

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
        label='Вспомните, пожалуйста, свое решение о том отдавать или брать деньги у участника Б, с которым вы были в паре. Чем вы руководствовались при принятии вашего решения?')
    keyword_dg_1 = models.StringField()
    keyword_dg_2 = models.StringField()
    keyword_dg_3 = models.StringField()
    reason_reveal = models.LongStringField(
        label="""Вспомните, пожалуйста, ваше решение относительно того, узнавать или не узнавать ответ участника Б. Чем вы руководствовались при принятии вашего решения?""")
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

    #   other   main variables
    reveal_order = models.StringField()
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
    proportion = models.IntegerField(min=0, max=100, label='')
    # DEMOGRAPHICS
    religion = models.IntegerField(label="""
    Насколько сильно вы верите в существование Бога? (укажите свой ответ в диапазоне от 1 = совсем нет 5 = очень сильно)
    """, choices=range(1, 6), widget=widgets.RadioSelectHorizontal)
    political = models.IntegerField(label="""
    Ниже представлена 7-балльная шкала, на которой политические взгляды, которых могут придерживаться люди, расположены от крайне либеральных (слева) до крайне консервативных (справа). Куда бы вы поставили себя на этой шкале?
    """, choices=range(0, 8), widget=widgets.RadioSelectHorizontal)
    age = models.StringField(label='Укажите ваш возраст:', choices=AGE_CHOICES, widget=widgets.RadioSelect)
    education = models.StringField(
        label="Какой самый высокий уровень школы вы закончили или какую высшую степень вы получили?",
        choices=EDUCATION_CHOICES, widget=widgets.RadioSelect)
    gender = models.StringField(label='Укажите ваш пол:',
                                choices=GENDER_CHOICES, widget=widgets.RadioSelect)
    marital = models.StringField(label='В настоящий момент вы:',
                                 choices=MARITAL_CHOICES, widget=widgets.RadioSelect)
    employment = models.StringField(label='В настоящий момент вы:',
                                    choices=EMPLOYMENT_CHOICES, widget=widgets.RadioSelect)
    income = models.StringField(
        label="Какое высказывание наиболее точно описывает финансовое положение вашей семьи?",
        choices=INCOME_CHOICES,
        widget=widgets.RadioSelect()
    )
    # Demand and clarity
    demand = models.LongStringField()
    instructions_clarity = models.IntegerField(label="""
    Насколько понятными и ясными были для вас инструкции? (укажите свой ответ в диапазоне от 1 = совсем непонятны 5 = абсолютно понятны)
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
