from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random
import json


class PlayerBot(Bot):

    def play_round(self):
        player = self.player
        yield Consent,
        yield OpinionIntro,
        yield Opinion, dict(opinion_war=random.choice(OPINION_CHOICES))
        yield OpinionIntensity, dict(opinion_intensity=random.choice(INTENSITY_NO_CHOICES))
        yield GeneralInstructions,
        yield DecisionInstructions,
        yield DGComprehensionCheck,
        yield PreDecision,
        if self.player.role == ROLE.DICTATOR:
            ans = {}
            if self.player.treatment == TREATMENT.RB:
                ans = dict(dictator_reveal=random.choice([False, True]))
            yield InfoStage1, ans
            yield InfoStage2,
        if player.role == ROLE.RECIPIENT and player.treatment == TREATMENT.VL:
            ans = dict(recipient_reveal=random.choice([False, True]))
            yield RecipientReveal, ans
        if player.role == ROLE.DICTATOR:
            yield DecisionStage, dict(dg_decision=random.choice(dg_decision_choices(player)))
        yield BeliefsIntro,
        ans = dict(proportion=random.randint(0, 100))
        yield Proportions, ans
        if player.role == ROLE.DICTATOR:
            l = dict(average_dg_belief=dg_decision_choices(player))
        if player.role == ROLE.RECIPIENT:
            l = dict(own_dg_belief=dg_decision_choices(player))

        yield Beliefs, l

        if player.treatment == TREATMENT.VL.value:

            ans = dict(vl_pro_belief=random.randint(0, 100),
                       vl_contra_belief=random.randint(0, 100))
            yield Beliefs2, ans
        if player.role == ROLE.DICTATOR:
            l = dict(reason_dg='test')
            if player.treatment == TREATMENT.RB:
                l['reason_reveal_d'] = 'test'
        else:
            l = dict(reason_dg_r='test')
            if player.treatment == TREATMENT.VL:
                l['reason_reveal_r'] = 'test'

        yield Reasons, l
        ans = dict(ias_friend=random.choice(IAS_CHOICES),
                   ias_coworker=random.choice(IAS_CHOICES),
                   ias_stranger=random.choice(IAS_CHOICES))
        yield Submission(InformationAvoidanceScale, dict(surveyholder=json.dumps(ans)), check_html=False)
        ans = dict(sdi_politics_pro=random.choice(SDI_CHOICES),
                   sdi_family_pro=random.choice(SDI_CHOICES),
                   sdi_politics_contra=random.choice(SDI_CHOICES),
                   sdi_family_contra=random.choice(SDI_CHOICES), )
        yield Submission(SocialDistanceIndex, dict(surveyholder=json.dumps(ans)), check_html=False)
        ans = {'risk_attitudes':
                   {'risk_general': {'risk_attitudes': random.randint(0, 10)},
                    'risk_financial_matters': {'risk_attitudes': random.randint(0, 10)},
                    'risk_strangers': {'risk_attitudes': random.randint(0, 10)}}}

        yield Submission(RiskAttitudes, dict(surveyholder=json.dumps(ans)), check_html=False)
        multi_ses=['is_fully_employed',
                             'is_married',
                             'is_retired',
                             'is_student',
                             'is_government_worker']
        ans = {'age': random.randint(18,99),
               'education': random.choice(EDUCATION_CHOICES)[0],
               'gender': random.choice(GENDER_CHOICES)[0],
               'income': random.choice(INCOME_CHOICES)[0],
               'multi_ses': random.choices(multi_ses, k=random.randint(0,len(multi_ses)))}

        yield Submission(Demographics, dict(surveyholder=json.dumps(ans)), check_html=False)
        yield Demand,dict(demand='test', instructions_clarity=random.randint(1,5))
        yield FinalForToloka,
        if player.blocked:
            yield Blocked,
