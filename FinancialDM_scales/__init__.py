from otree.api import *
import numpy as np
import random
from random import choice as random_draw

doc = """
Read quiz quest 
"""

class C(BaseConstants):
    NAME_IN_URL = 'FMD_Scales'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def make_field(label):
        return models.IntegerField(
            choices=[1,2,3,4,5],
            label=label,
            widget=widgets.RadioSelect,
            )


class Player(BasePlayer):
    ccc1 = make_field('We must protect the climate’s delicate equilibrium.') ## concern 4 items
    ccc2 = make_field('Climate protection is important for our future.')
    ccc3 = make_field('I worry about the climate’s state.')
    ccc4 = make_field('Climate change has severe consequences for humans and nature.')

    ccc10 = make_field('Climate change and its consequences are being exaggerated in the media.')     ### skepticism 7 items 
    ccc11 = make_field('Climate change is a racket.')
    ccc12 = make_field('As long as meteorologists are not even able to accurately forecast weather, climate cannot be reliably predicted either.')
    ccc13 = make_field('There are larger problems than climate protection.')
    ccc14 = make_field('I do not feel threatened by climate change.')
    ccc15 = make_field('The impacts of climate change are unpredictable; thus, my climate-friendly behavior is futile.')
    ccc16 = make_field('Climate protection needlessly impedes economic growth.')


    comprehension_C1_correct = models.BooleanField()
    comprehension_C2_correct = models.BooleanField()
    comprehension_UM1_correct = models.BooleanField()
    comprehension_UM2_correct = models.BooleanField()
    comprehension_UE1_correct = models.BooleanField()
    comprehension_UE2_correct = models.BooleanField()
    sum_correct = models.IntegerField()
    outcome_bonus_pound = models.FloatField()
    outcome_bonus_points = models.FloatField()
    outcome_carbon = models.FloatField()




    
class questionnaire(Page):
    form_model = 'player'
    form_fields= ['ccc1', 'ccc2', 'ccc3', 'ccc4', 'ccc10', 'ccc11', 'ccc12', 'ccc13', 'ccc14', 'ccc15', 'ccc16'  ]


    

class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        player.sum_correct = player.participant.sum_correct
        player.comprehension_C1_correct = player.participant.comprehension_C1_correct
        player.comprehension_C2_correct = player.participant.comprehension_C2_correct
        player.comprehension_UM1_correct = player.participant.comprehension_U1_correct
        player.comprehension_UM2_correct = player.participant.comprehension_U2_correct
        player.comprehension_UE1_correct = player.participant.comprehension_Ub1_correct
        player.comprehension_UE2_correct = player.participant.comprehension_Ub2_correct
        player.outcome_bonus_pound = player.participant.outcome_bonus_pound
        player.outcome_bonus_points =  player.participant.outcome_bonus_points
        player.outcome_carbon = player.participant.outcome_carbon
        return{
            'drawn_round':  player.participant.drawn_round_display,
            'drawn_block': player.participant.drawn_block,
            'relevant_round_choice': player.participant.relevant_round_choice,
            'outcome_bonus_points': player.participant.outcome_bonus_points,
            'outcome_bonus_pound': player.participant.outcome_bonus_pound,
            'outcome_carbon': player.participant.outcome_carbon,
            'sum_correct': player.participant.sum_correct
        }


   

 
 
page_sequence = [questionnaire, Results]
