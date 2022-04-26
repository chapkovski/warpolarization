from os import environ
prolific_options = dict(for_prolific=False,
                        prolific_redirect_url='https://app.prolific.co/submissions/complete?cc=7C68BD7C',
                        for_toloka=True)
SESSION_CONFIGS = [
    dict(
        name='baselineR',
        display_name='baseline - Recipient',
        app_sequence=['polar'],
        num_demo_participants=2,
        reveal=True,
        before=False,
        role='recipient',
        **prolific_options
    ),
    dict(
        name='vl_r',
        display_name='Reveal - Recipient',
        app_sequence=['polar'],
        num_demo_participants=2,
        reveal=True,
        before=False,
        role='recipient',
        **prolific_options
    ),
    dict(
        name='baselineD',
        display_name='baseline Dictator',
        app_sequence=['polar'],
        num_demo_participants=2,
        reveal=True,
        before=False,
        role='dictator',
        **prolific_options
    ),
    dict(
        name='reveal_before',
        app_sequence=['polar'],
        num_demo_participants=2,
        reveal=True,
        before=True,
        role='dictator',
        **prolific_options
    ),
    dict(
        name='forced_reveal',
        app_sequence=['polar'],
        num_demo_participants=2,
        reveal=False,
        before=False,
        role='dictator',
        **prolific_options
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=.01, participation_fee=0.00, doc=""
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
