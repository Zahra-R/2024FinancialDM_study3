from os import environ


SESSION_CONFIGS = [
    
    ### FINANCIAL DECISION MAKING
    
    dict(
        name='FinancialDM_united',
        app_sequence=['FinancialDM_Intro', 'FinancialDM_choiceTask', 'FinancialDM_scales'],
        num_demo_participants=20
    ),

    dict(
        name='ravens',
        app_sequence=[ 'FinancialDM_scales'],
        num_demo_participants=5
    ),

     

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [

    ### FINANCIAL DECISION MAKING
    'seqCertain',
    'SeqRiskyMComplex',
    'SeqRiskyCComplex',


    'carbonLeft', 
    'MoneyRiskyFirst',
    'CertainFirst',
    'ModRoundArray',

    'comprehension_C1_correct' ,
    'comprehension_C2_correct' ,
    'comprehension_U1_correct',
    'comprehension_U2_correct',
    'comprehension_Ub1_correct',
    'comprehension_Ub2_correct',

    'drawn_round_display',
    'drawn_block',
    'relevant_round_choice',
    'outcome_bonus_points',
    'outcome_bonus_pound',
    'outcome_carbon',
    'sum_correct'
]


SESSION_FIELDS = [
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

DEBUG = True 


SECRET_KEY = '3153268574945'

INSTALLED_APPS = ['otree']
