from otree.api import *
from .choices import *
from .models import *
from .constants import Constants
from pprint import pprint


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
    form_model = 'player'
    form_fields = ['cq1_ego',
                   'cq1_alter',
                   'cq2_ego',
                   'cq2_alter',
                   'cq3_ego',
                   'cq3_alter']


class InfoStage1(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.subsession.treatment == 'reveal_before':
            return ['reveal']

    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment != 'reveal_after'


class InfoStage2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment != 'reveal_after'


class DecisionStage(Page):
    form_model = 'player'
    form_fields = ['dg_decision']


class RevealAfterStage1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment == 'reveal_after'


class RevealAfterStage2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.subsession.treatment == 'reveal_after' and player.reveal


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
    pass


class InformationAvoidanceScale(Page):
    def post(self):
        survey_data = json.loads(self._form_data.get('surveyholder'))

        for k, v in survey_data.items():
            setattr(self.player, k, v)

        return super().post()


class SocialDistanceIndex(Page):
    def vars_for_template(player: Player):
        # todo: make it dependent on Respondent answer
        return dict(reverted_opinion='did not agree')

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
    pass


class Demand(Page):
    pass


page_sequence = [

    # Consent,
    # OpinionIntro,
    # Opinion1,
    # Opinion2,
    # Opinion3,
    # GeneralInstructions,
    # DecisionInstructions,
    # DGComprehensionCheck,
    InfoStage1,
    InfoStage2,
    DecisionStage,
    # RevealAfterStage1,
    # RevealAfterStage2,
    Reasons,
    # BeliefsIntro,
    # Beliefs,
    InformationAvoidanceScale,
    SocialCuriosityScale,
    SocialDistanceIndex,
    RiskAttitudes,
    # Demographics,
    # Demand
]
