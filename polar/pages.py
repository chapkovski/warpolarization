from otree.api import Page as oTreePage
from .choices import *
from .models import *
from .constants import C, POSITION, TREATMENT
from pprint import pprint
from starlette.responses import RedirectResponse
import json
import random
import numpy as np


class Page(oTreePage):
    instructions = False

    def get_context_data(self, **context):
        r = super().get_context_data(**context)
        r['maxpages'] = self.participant._max_page_index
        r['page_index'] = self._index_in_pages
        r['progress'] = f'{int(self._index_in_pages / self.participant._max_page_index * 100):d}'
        r['instructions'] = self.instructions
        return r


class UnBlockedPage(Page):
    def _is_displayed(self):
        return not self.player.blocked and super()._is_displayed()


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent', 'consent_wait']
    def get(self, **kwargs):
        return super().get(**kwargs)


class OpinionIntro(Page):
    pass


class Opinion(Page):
    form_model = 'player'
    form_fields = ['opinion_war']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.opinion_war == 1:
            c = random.sample(INTENSITY_YES_CHOICES, 2)
            player.opinion_intensity_order = json.dumps(c)
        else:
            c = random.sample(INTENSITY_NO_CHOICES, 2)
            player.opinion_intensity_order = json.dumps(c)


class OpinionIntensity(Page):
    form_model = 'player'
    form_fields = ['opinion_intensity']

    @staticmethod
    def vars_for_template(player: Player):
        if player.opinion_war:
            label = 'Скажите, пожалуйста, насколько Вы поддерживаете действия российских вооруженных сил на Украине?'
        else:
            label = 'Скажите, пожалуйста, насколько Вы не поддерживаете действия российских вооруженных сил на Украине?'
        return dict(label=label)


class GeneralInstructions(Page):
    pass


class DecisionInstructions(Page):
    pass


class DGComprehensionCheck(Page):
    instructions = True

    def post(self):
        if not bool(self._form_data):
            return super().post()
        if self._form_data.get('timeout_happened'):
            return super().post()

        survey_data = json.loads(self._form_data.get('surveyholder'))

        for k, v in survey_data.items():
            try:
                setattr(self.player, k, int(v))
            except AttributeError:
                pass
        return super().post()


class PreDecision(UnBlockedPage):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        s = player.subsession
        p = player
        """
        what we do here:
         there are four different treatments for dictators.
          - Baseline - where position is not shown.
          - FR, RB: Forced reveal and reveal_before where position is shown non depending of the wish of the R
          - VL - where position is shown depending on the wish of the R
          if we are in the baseline we don't need partner's position
          if we in the FL or RB then we need to take into account only the yes and no counters. and values 
          that partner_position may take is either yes or no. 
          if we are in VL then the partner_position can be either yes, no or nr (non-reveal).
          if the total number of Ds matched with Yes exceeds the num_yes, and those matched with No exceeds the num_no,
          then we assign a baseline treatment to the rest. That's to deal with dropouts.
          
           
          
        """
        # we do not assign partner positions to a treatment baseline because we don't care about the matching for them
        if player.role == 'dictator' and player.treatment != TREATMENT.BASELINE:
            weights = s.get_weights()
            print("WEIGHTS!", weights)
            if weights:
                p.partner_position = np.random.choice(list(weights.keys()), p=list(weights.values()))
            else:
                player.treatment = TREATMENT.BASELINE.value
            print('$'*10)
            print(p.treatment)
            print('$'*10)


class InfoStage1(UnBlockedPage):
    instructions = True
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.treatment == TREATMENT.RB:
            return ['dictator_reveal']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == ROLE.DICTATOR # and player.treatment != TREATMENT.BASELINE


class InfoStage2(UnBlockedPage):
    instructions = True

    @staticmethod
    def is_displayed(player: Player):
        return player.role == ROLE.DICTATOR #and player.treatment != TREATMENT.BASELINE


class RecipientReveal(UnBlockedPage):
    instructions = True
    form_model = 'player'
    form_fields = ['recipient_reveal']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == ROLE.RECIPIENT and player.treatment == TREATMENT.VL


class DecisionStage(UnBlockedPage):
    instructions = True
    form_model = 'player'
    form_fields = ['dg_decision']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == ROLE.DICTATOR


class Reasons(UnBlockedPage):
    form_model = 'player'

    def get_form_fields(player: Player):

        if player.role == ROLE.DICTATOR:
            l = ['reason_dg', ]
            if player.treatment == TREATMENT.RB:
                l = l + ['reason_reveal_d', ]
        else:
            l = ['reason_dg_r']
            if player.treatment == TREATMENT.VL:
                l.append('reason_reveal_r')
        return l


class BeliefsIntro(UnBlockedPage):
    pass


class Beliefs(UnBlockedPage):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.role == ROLE.DICTATOR:
            l =  ['average_dg_belief']
        if player.role == ROLE.RECIPIENT:
            l =  ['own_dg_belief']


        return l

class Beliefs2(UnBlockedPage):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == TREATMENT.VL.value
    @staticmethod
    def get_form_fields(player: Player):
        return ['vl_pro_belief','vl_contra_belief']




class Proportions(UnBlockedPage):
    form_model = 'player'
    form_fields = ['proportion']


class InformationAvoidanceScale(UnBlockedPage):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))

        for k, v in survey_data.items():
            setattr(self.player, k, v)

        return super().post()


class SocialDistanceIndex(UnBlockedPage):
    def vars_for_template(player: Player):
        return dict(reverted_opinion=player.reverted_opinion,
                    reverted_opinion_single=player.reverted_opinion_single)

    def post(self):
        print('aaaa', self._form_data)
        survey_data = json.loads(self._form_data.get('surveyholder'))

        for k, v in survey_data.items():
            setattr(self.player, k, v)

        return super().post()


class RiskAttitudes(UnBlockedPage):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))
        risk_attitudes = survey_data.get('risk_attitudes')

        for k, v in risk_attitudes.items():
            setattr(self.player, k, v.get('risk_attitudes'))
        print(self.player.participant.code)
        return super().post()


class Demographics(UnBlockedPage):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))
        pprint(survey_data)
        multi_ses = survey_data.pop('multi_ses', [])

        for k, v in survey_data.items():
            try:
                setattr(self.player, k, int(v))
            except AttributeError:
                pass

        for i in multi_ses:
            try:
                setattr(self.player, i, True)
            except AttributeError:
                pass
        return super().post()


class Demand(UnBlockedPage):
    form_model = 'player'
    form_fields = ["demand", 'instructions_clarity']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payable = True


class FinalForToloka(UnBlockedPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config.get('for_toloka') and not player.blocked


class Blocked(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.blocked


page_sequence = [
    Consent,
    OpinionIntro,
    Opinion,
    OpinionIntensity,
    GeneralInstructions,
    DecisionInstructions,
    DGComprehensionCheck,
    PreDecision,
    InfoStage1,
    InfoStage2,
    RecipientReveal,
    DecisionStage,
    BeliefsIntro,
    Proportions,
    Beliefs,
    Beliefs2,
    Reasons,
    InformationAvoidanceScale,
    SocialDistanceIndex,
    RiskAttitudes,
    Demographics,
    Demand,
    FinalForToloka,
    Blocked,
]
