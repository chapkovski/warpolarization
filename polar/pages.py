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


class Consent(Page):
    pass


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


class Opinion3(Page):
    form_model = 'player'
    form_fields = ['opinion_covid']


class GeneralInstructions(Page):
    pass


class DecisionInstructions(Page):
    pass


class DGComprehensionCheck(Page):
    instructions = True
    form_model = 'player'
    form_fields = ['cq1_ego',
                   'cq1_alter',
                   'cq2_ego',
                   'cq2_alter',
                   'cq3_ego',
                   'cq3_alter']

    def form_invalid(self, form):
        self.player.cq_err_counter += 1
        if self.player.cq_err_counter > C.MAX_CQ_ATTEMPTS:
            self.player.blocked = True
            return
        return super().form_invalid(form)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(attempts=C.MAX_CQ_ATTEMPTS - player.cq_err_counter)


class Blocked(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.blocked


class PreDecision(Page):
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
        if player.role == 'dictator':
            weights = s.get_weights()
            if weights:
                p.partner_position = np.random.choice(weights.keys(), p=weights.values())
            else:
                p.treatment = TREATMENT.BASELINE


class InfoStage1(Page):
    instructions = True
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.subsession.treatment == TREATMENT.RB:
            return ['reveal']

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment != TREATMENT.BASELINE


class InfoStage2(Page):
    instructions = True

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment != TREATMENT.BASELINE


class DecisionStage(Page):
    instructions = True
    form_model = 'player'
    form_fields = ['dg_decision']

    @staticmethod
    def is_displayed(player: Player):
        return player.role() == ROLE.DICTATOR


class Reasons(Page):
    form_model = 'player'

    def get_form_fields(player: Player):
        if player.role == C.dictator:
            l = ['reason_dg', ]
            revl = ['reason_reveal', ]
            if player.session.config.get('reveal'):
                return l + revl
        else:
            return ['reason_dg_r']


class BeliefsIntro(Page):
    pass


class Beliefs(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.subsession.treatment == 'reveal_after':
            return ['dg_belief_ra', 'reveal_belief']
        if player.subsession.treatment == 'reveal_before':
            return [
                'dg_belief_rb_nonrev',
                'dg_belief_rb_rev_diff',
                'dg_belief_rb_rev_same',
                'reveal_belief'
            ]
        if player.subsession.treatment == 'forced_reveal':
            return [

                'dg_belief_fr_diff',
                'dg_belief_fr_same',

            ]


class Proportions(Page):
    form_model = 'player'
    form_fields = ['proportion']


class InformationAvoidanceScale(Page):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))

        for k, v in survey_data.items():
            setattr(self.player, k, v)

        return super().post()


class SocialDistanceIndex(Page):
    def vars_for_template(player: Player):
        return dict(reverted_opinion=player.reverted_opinion,
                    reverted_opinion_single=player.reverted_opinion_single)

    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))

        for k, v in survey_data.items():
            setattr(self.player, k, v)

        return super().post()


class RiskAttitudes(Page):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))
        risk_attitudes = survey_data.get('risk_attitudes')

        for k, v in risk_attitudes.items():
            setattr(self.player, k, v.get('risk_attitudes'))
        print(self.player.participant.code)
        return super().post()


class Demographics(Page):
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


class Demand(Page):
    form_model = 'player'
    form_fields = ["demand", 'instructions_clarity']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payable = True


class FinalForToloka(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config.get('for_toloka') and not player.blocked


page_sequence = [
    Consent,
    # OpinionIntro,
    Opinion,
    OpinionIntensity,
    GeneralInstructions,
    DecisionInstructions,
    DGComprehensionCheck,

    PreDecision,

    InfoStage1,
    InfoStage2,
    RecipientReveal
    # DecisionStage,
    # BeliefsIntro,
    # Beliefs,
    # Proportions,
    # Reasons,
    # InformationAvoidanceScale,
    # SocialDistanceIndex,
    # RiskAttitudes,
    # Demographics,
    # Demand,
    # FinalForToloka,
    # Blocked,
]
