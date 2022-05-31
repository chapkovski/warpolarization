from os import environ
from global_constants import TREATMENT, ROLE
prolific_options = dict(for_prolific=False,
                        prolific_redirect_url='https://app.prolific.co/submissions/complete?cc=7C68BD7C',
                        for_toloka=True)
SESSION_CONFIGS = [
    dict(
        name='baseline_r',
        display_name='Baseline - Recipient',
        app_sequence=['polar'],
        num_demo_participants=2,
        reveal=False,
        role=ROLE.RECIPIENT,
        treatment=TREATMENT.BASELINE,
        **prolific_options
    ),

    dict(
        name='recipient_reveal_r',
        display_name='Recipient Reveal - Recipient',
        app_sequence=['polar'],
        num_demo_participants=2,
        reveal=True,
        role=ROLE.RECIPIENT,
        treatment=TREATMENT.VL,
        **prolific_options
    ),

    dict(
        name='recipient_reveal_d',
        display_name='Recipient Reveal - Dictator',
        app_sequence=['polar'],
        num_demo_participants=3,
        reveal=False,
        role=ROLE.DICTATOR,
        treatment=TREATMENT.VL,
        partner_position_shown=True,
        counter_yes=1,
        counter_no=1,
        counter_nr=50,
        **prolific_options
    ),

    dict(
        name='reveal_before',
        display_name='Reveal Before - Dictator',
        app_sequence=['polar'],
        num_demo_participants=3,
        reveal=True,
        role=ROLE.DICTATOR,
        treatment=TREATMENT.RB,
        counter_yes=1,
        counter_no=1,
        counter_nr=0,
        **prolific_options
    ),
    dict(
        name='forced_reveal',
        display_name='Forced Reveal - Dictator',
        app_sequence=['polar'],
        num_demo_participants=3,
        reveal=False,
        role=ROLE.DICTATOR,
        treatment=TREATMENT.FR,
        counter_yes=1,
        counter_no=1,
        counter_nr=0,
        **prolific_options
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=.01, participation_fee=0.00, doc="", use_browser_bots=False
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5410395654576'
