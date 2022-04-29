from otree.api import *
from .choices import *
from .constants import C, POSITION, TREATMENT, ROLE
import json
import itertools
import random
from math import copysign

# TODO: remove proportions from methods
# TODO: write down the logic of treatment
# TODO: what to do with recipieints?
f = lambda x: f'{(x / 100):.2f}$'


class Subsession(BaseSubsession):
    partner_position_shown = models.BooleanField()  # can we show at least theoretically partner's position; is true for all but baseline treatment for Ds
    counter_yes = models.IntegerField()  # Count number of recipieints who agreed to show their YES opinion
    counter_no = models.IntegerField()  # Count number of recipieints who agreed to show their NO opinion
    counter_nr = models.IntegerField()  # Count number of recipieints who DID NOT agree to show their opinion
    take_nrs = models.BooleanField()  # do we take into account those who do not want to agree

    def get_weights(self):
        counter = {
            POSITION.YES: self.player_set.filter_by(partner_position=POSITION.YES).count(),
            POSITION.NO: self.player_set.filter_by(partner_position=POSITION.NO).count(),
            POSITION.NR: self.player_set.filter_by(partner_position=POSITION.NR).count()
        }
        maxnum = {
            POSITION.YES: self.counter_yes,
            POSITION.NO: self.counter_no,
            POSITION.NR: self.counter_nr
        }
        if self.take_nrs:
            potential_positions = C.POSITIONS_YNR
        else:
            potential_positions = C.POSITIONS_YES_NO
        weights = {}
        for i in potential_positions:
            weights[i] = max(0, maxnum[i] - counter[i])
        if all([i == 0 for i in weights.values()]):
            return
        return weights


def creating_session(subsession: Subsession):
    conf = subsession.session.config
    treatment = conf.get('treatment')
    assert TREATMENT.has_value(treatment), 'something wrong with treatment name setting'
    role = conf.get('role')
    assert ROLE.has_value(role), 'something wrong with treatment role setting'
    orders = [False, True]
    if role == ROLE.DICTATOR:
        endowments = dict(ego_endowment=C.DICTATOR_ENDOWMENT, alter_endowment=C.BASIC_ENDOWMENT)
    else:
        endowments = dict(ego_endowment=C.BASIC_ENDOWMENT, alter_endowment=C.DICTATOR_ENDOWMENT)
    player_updates = dict(_role=role, treatment=treatment, )
    player_updates.update(endowments)
    subsession.player_set.update(player_updates)
    #
    subsession.take_nrs = treatment == TREATMENT.VL
    subsession.partner_position_shown = treatment != TREATMENT.BASELINE
    subsession.counter_no = conf.get('counter_no', 0)
    subsession.counter_yes = conf.get('counter_yes', 0)
    subsession.counter_nr = conf.get('counter_nr', 0)
    if treatment != TREATMENT.VL:
        assert subsession.counter_nr == 0, 'Check NR counter and treatment'
    for p in subsession.get_players():
        c = sorted(REVEAL_CHOICES, key=lambda x: x[0], reverse=random.choice(orders))
        p.reveal_order = json.dumps(c)
        c = random.sample(OPINION_CHOICES, 2)
        p.opinion_war_order = json.dumps(c)


class Group(BaseGroup):
    pass


def reveal_choices(player):
    return json.loads(player.reveal_order)


def opinion_war_choices(player):
    return json.loads(player.opinion_war_order)


def opinion_intensity_choices(player):
    return json.loads(player.opinion_intensity_order)


class Player(BasePlayer):
    def role_desc(self):
        if self.role == ROLE.DICTATOR:
            return 'А'
        else:
            return 'Б'

    treatment = models.StringField()
    _role = models.StringField()
    opinion_war_order = models.StringField()
    opinion_intensity_order = models.StringField()
    opinion_war = models.BooleanField(
        label=C.AGREEMENT_QUESTION,
    )
    opinion_intensity = models.BooleanField()
    partner_show = models.BooleanField()
    partner_position = models.BooleanField()
    aligned = models.BooleanField()
    dictator_reveal = models.BooleanField()
    recipient_reveal = models.BooleanField()
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
            res.append(dict(decision=i[1], ego=f(C.DICTATOR_ENDOWMENT - i[0]),
                            alter=f(C.BASIC_ENDOWMENT + i[0]),
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
    ias_friend = models.StringField()
    ias_coworker = models.StringField()
    ias_stranger = models.StringField()
    # REASONS
    reason_dg_r = models.LongStringField(label='Как вы думаете, чем руководствовался Участник А принимая решение о том отдавать или брать деньги у участника Б (вас)?')  # reasons for recipieint beliefs of dictators decision
    reason_reveal_r = models.LongStringField(
    label=
    """Вспомните, пожалуйста, ваше решение относительно того, сообщать или не сообщать участнику А о вашей поддержке или не поддержке действий российских вооруженных сил на Украине. 
    Чем вы руководствовались при принятии вашего решения?"""
    )

    reason_dg = models.LongStringField(
        label='Вспомните, пожалуйста, свое решение о том отдавать или брать деньги у участника Б, с которым вы были в паре. Чем вы руководствовались при принятии вашего решения?')

    reason_reveal = models.LongStringField(
        label="""Вспомните, пожалуйста, ваше решение относительно того, узнавать или не узнавать ответ участника Б. Чем вы руководствовались при принятии вашего решения?""")

    # Comprehension questions
    cq1_d = models.IntegerField(label=C.CQ_EGO_LABEL, choices=CQ_CHOICES,
                                widget=widgets.RadioSelectHorizontal)
    cq1_r = models.IntegerField(label=C.CQ_ALTER_LABEL, choices=CQ_CHOICES,
                                widget=widgets.RadioSelectHorizontal)
    cq2_d = models.IntegerField(label=C.CQ_EGO_LABEL, choices=CQ_CHOICES,
                                widget=widgets.RadioSelectHorizontal)
    cq2_r = models.IntegerField(label=C.CQ_ALTER_LABEL, choices=CQ_CHOICES,
                                widget=widgets.RadioSelectHorizontal)
    cq3_d = models.IntegerField(label=C.CQ_EGO_LABEL, choices=CQ_CHOICES,
                                widget=widgets.RadioSelectHorizontal)
    cq3_r = models.IntegerField(label=C.CQ_ALTER_LABEL, choices=CQ_CHOICES,
                                widget=widgets.RadioSelectHorizontal)

    #   other   main variables
    reveal_order = models.StringField()
    ego_endowment = models.IntegerField()
    alter_endowment = models.IntegerField()
    # BELIEFS:
    average_dg_belief = models.IntegerField()
    own_dg_belief = models.IntegerField()
    proportion = models.IntegerField(min=0, max=100, label='')
    # DEMOGRAPHICS

    age = models.IntegerField(label='Укажите ваш возраст:', widget=widgets.RadioSelect)
    education = models.IntegerField(
        label="Какой самый высокий уровень школы вы закончили или какую высшую степень вы получили?",
        choices=EDUCATION_CHOICES, widget=widgets.RadioSelect)
    gender = models.IntegerField(label='Укажите ваш пол:',
                                 choices=GENDER_CHOICES, widget=widgets.RadioSelect)

    income = models.IntegerField(
        label="Какое высказывание наиболее точно описывает финансовое положение вашей семьи?",
        choices=INCOME_CHOICES,
        widget=widgets.RadioSelect()
    )
    # some binary socio-econ vars
    is_fully_employed = models.BooleanField()
    is_married = models.BooleanField()
    is_retired = models.BooleanField()
    is_student = models.BooleanField()
    is_government_worker = models.BooleanField()

    # Demand and clarity
    demand = models.LongStringField()
    instructions_clarity = models.IntegerField(label="""
    Насколько понятными и ясными были для вас инструкции? (укажите свой ответ в диапазоне от 1 = совсем непонятны 5 = абсолютно понятны)
    """, choices=range(1, 6), widget=widgets.RadioSelectHorizontal)


def dg_decision_choices(player):
    ints = list(range(-50, 51, 10))

    return [(i, f(i)) for i in ints]


def cq1_d_error_message(player, value):
    if value != 50:
        return C.ERR_MSG


def cq1_r_error_message(player, value):
    if value != 100:
        return C.ERR_MSG


def cq2_d_error_message(player, value):
    if value != 100:
        return C.ERR_MSG


def cq2_r_error_message(player, value):
    if value != 50:
        return C.ERR_MSG


def cq3_d_error_message(player, value):
    if value != 150:
        return C.ERR_MSG


def cq3_r_error_message(player, value):
    if value != 0:
        return C.ERR_MSG
