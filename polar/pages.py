from otree.api import Page as oTreePage
from .choices import *
from .models import *
from .constants import Constants
from pprint import pprint
from starlette.responses import RedirectResponse


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


class Opinion1(Page):
    form_model = 'player'
    form_fields = ['opinion_competition']


class Opinion2(Page):
    form_model = 'player'
    form_fields = ['opinion_lgbt']


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
        if self.player.cq_err_counter > Constants.MAX_CQ_ATTEMPTS:
            self.player.blocked = True
            return
        return super().form_invalid(form)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(attempts=Constants.MAX_CQ_ATTEMPTS - player.cq_err_counter)


class Blocked(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.blocked


class InfoStage1(Page):
    instructions = True
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.subsession.treatment == 'reveal_before':
            return ['reveal']

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment != 'reveal_after'


class InfoStage2(Page):
    instructions = True

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment != 'reveal_after'


class DecisionStage(Page):
    instructions = True
    form_model = 'player'
    form_fields = ['dg_decision']


class RevealAfterStage1(Page):
    form_model = 'player'
    form_fields = ['reveal']

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment == 'reveal_after'


class RevealAfterStage2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment == 'reveal_after'


class Reasons(Page):
    form_model = 'player'

    def get_form_fields(player: Player):
        l = ['reason_dg', 'keyword_dg_1', 'keyword_dg_2', 'keyword_dg_3']
        revl = ['reason_reveal', 'keyword_rev_1', 'keyword_rev_2', 'keyword_rev_3']
        if player.session.config.get('reveal'):
            return l + revl
        return l


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


class SocialCuriosityScale(Page):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))
        attitudes = survey_data.get('scs')
        for k, v in attitudes.items():
            setattr(self.player, k, v.get('scs'))
        return super().post()


class RiskAttitudes(Page):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))
        risk_attitudes = survey_data.get('risk_attitudes')

        for k, v in risk_attitudes.items():
            setattr(self.player, k, v.get('risk_attitudes'))
        print(self.player.participant.code)
        return super().post()


import json


class Demographics(Page):
    form_model = 'player'
    form_fields = ["religion",
                   "political",
                   "age",
                   "education",
                   "gender",
                   "marital",
                   "employment",
                   "income", ]


class Demand(Page):
    form_model = 'player'
    form_fields = ["demand", 'instructions_clarity']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payable = True
        player.payoff = Constants.DICTATOR_ENDOWMENT - player.dg_decision
        player.aligned = player.opinion_lgbt == player.partner_position


class FinalForProlific(Page):
    def is_displayed(self):
        return self.session.config.get('for_prolific')

    def get(self):
        return RedirectResponse(self.session.config.get('prolific_redirect_url'))


class FinalForToloka(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.session.config.get('for_toloka') and not player.blocked


page_sequence = [
    Consent,
    OpinionIntro,
    Opinion1,
    Opinion2,
    Opinion3,
    GeneralInstructions,
    DecisionInstructions,
    DGComprehensionCheck,
    Blocked,
    InfoStage1,
    InfoStage2,
    DecisionStage,
    RevealAfterStage1,
    RevealAfterStage2,
    Reasons,
    BeliefsIntro,
    Beliefs,
    Proportions,
    InformationAvoidanceScale,
    SocialCuriosityScale,
    SocialDistanceIndex,
    RiskAttitudes,
    Demographics,
    Demand,
    FinalForToloka,

]
