from otree.api import *
import numpy as np
import random
from random import choice as draw_random_number
import csv
import json

doc = """
Read quiz quest 
"""


def read_csvC():
    path = "FinancialDM_choiceTask/stimuliC.json"
    with open(path, 'r') as j:
        doc = json.loads(j.read())    
    return doc


def read_csvU():
    path = "FinancialDM_choiceTask/stimuliU.json"
    with open(path, 'r') as j:
        doc = json.loads(j.read())    
    return doc





class C(BaseConstants):
    NAME_IN_URL = 'fdm'
    PLAYERS_PER_GROUP = None
    QUESTIONS_C = read_csvC()
    QUESTIONS_U = read_csvU()
    #NUM_ROUNDS = 16
    NUM_ROUNDS =  13 + 4 + 4*(len(QUESTIONS_U)-4)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    import itertools
    carbonLeftCycle = itertools.cycle([True, False])
    MoneyRiskyFirstCycle = itertools.cycle([True, True, False, False])
    CertainFirstCycle = itertools.cycle([True, True, True, True, False, False, False, False])
    for player in subsession.get_players():
        if subsession.round_number == 1:
           player.participant.seqCertain = np.arange(1,13)
           random.shuffle(player.participant.seqCertain)

           nums = range(42)
           letters = ['A', 'B']
           nums_letters = [[n+1, l] for n in nums for l in letters]
           random.shuffle(nums_letters)
           #player.participant.SeqRiskyMComplex = np.concatenate((range(0,4), shuffledOrderU), axis = None) ### here maybe I will have to add the practice rounds
           player.participant.SeqRiskyMComplex = nums_letters 


           random.shuffle(nums_letters)
           #player.participant.SeqRiskyMComplex = np.concatenate((range(0,4), shuffledOrderU), axis = None) ### here maybe I will have to add the practice rounds
           player.participant.SeqRiskyCComplex = nums_letters 

           player.participant.MoneyRiskyFirst = next(MoneyRiskyFirstCycle)
           player.participant.CertainFirst = next(CertainFirstCycle)
           player.participant.carbonLeft = next(carbonLeftCycle)
           if player.participant.CertainFirst == False:
               player.participant.ModRoundArray = np.concatenate((np.arange(14,186), np.arange(1,14)))
           else:
               player.participant.ModRoundArray = np.arange(1,186)
            ######### this is for the bonus payoff later on ########
            # there are 181 rounds, 1 and 15, 16, 17, and 18 are practice round, hence not payoff relevant
           seq_payoff = list(range(2,186))
           if player.participant.CertainFirst == True: 
                seq_payoff.remove(15)
                seq_payoff.remove(16)
                seq_payoff.remove(100)
                seq_payoff.remove(101)
           else: 
                seq_payoff.remove(2)
                seq_payoff.remove(87)
                seq_payoff.remove(88)
                seq_payoff.remove(173)
               
           player.drawn_round = int(draw_random_number(seq_payoff))
        player.CertainFirst = player.participant.CertainFirst 
        player.MoneyRiskyFirst = player.participant.MoneyRiskyFirst 
        player.carbonLeft = player.participant.carbonLeft
        player.OptionAoutcomeOneTop = draw_random_number([True, False])
        player.OptionBoutcomeOneTop = draw_random_number([True, False])
        player.modRoundNumber = int(player.participant.ModRoundArray[player.round_number - 1])

          
class Group(BaseGroup):
    pass


class Player(BasePlayer):
    practice = models.BooleanField()
    stimulusIDC = models.IntegerField()
    stimulusIDU = models.IntegerField()
    round_within_block = models.IntegerField()

    moneyA = models.IntegerField()
    moneyB = models.IntegerField()
    carbonA = models.IntegerField()
    carbonB = models.IntegerField()
    choice = models.StringField()
    OptionARight = models.IntegerField()
    carbonLeft = models.BooleanField()
    MoneyRiskyFirst = models.BooleanField()
    CertainFirst = models.BooleanField()
    RiskyAttribute = models.StringField()
    RiskyOption = models.StringField()
    OptionAoutcomeOneTop = models.BooleanField()
    OptionBoutcomeOneTop = models.BooleanField()
    moAcertain = models.FloatField()
    moBcertain = models.FloatField()
    coAcertain = models.FloatField()
    coBcertain = models.FloatField()

    moneyA1 = models.IntegerField()
    moneyA2 = models.IntegerField()
    moneyB1 = models.IntegerField()
    moneyB2 = models.IntegerField()
    carbonA1 = models.IntegerField()
    carbonA2 = models.IntegerField()
    carbonB1 = models.IntegerField()
    carbonB2 = models.IntegerField()
    probA1 = models.FloatField() 
    probA2 = models.FloatField()
    probB1 = models.FloatField()
    probB2 = models.FloatField()
    modRoundNumber = models.IntegerField()

    input_keyboard = models.IntegerField()
    timedout = models.BooleanField(default=False)
    page_load = models.StringField(initial = '0', default = '0')
    page_submit = models.StringField(null=True)
    responsetime = models.IntegerField()
    
    drawn_round = models.IntegerField()
    outcome_bonus_points = models.FloatField()
    outcome_carbon = models.FloatField()
    outcome_bonus_pound = models.FloatField()

    # C1 correct: 3 (50lbs), C2 correct: 2 (45$); U1mon correct: 3 (40$); U2mon correct 2 (right otpion); U1 carb correct 2 (21 lbs); U2 carb correct: 3 (62%)
    comprehensions_C1 = models.StringField(choices=[ [1, "15 lbs. CO2"], [2, "30 lbs. CO2"], [3, "50 lbs. CO2"]], label ="Which amount of carbon would be emitted if you chose the right option?",  widget = widgets.RadioSelect )
    comprehensions_C2 = models.StringField(choices=[[1, "$20"], [2,"$45"], [3, "$50"]], label ="What is the highest monetary amount you can get in this choice situation? ",  widget = widgets.RadioSelect )
    comprehensions_U1mon = models.StringField(choices=[ [1, "22$"], [2, "18$"], [3, "40$"]], label ="What is the maximum monetary amount you can win when choosing the left option?",  widget = widgets.RadioSelect )
    comprehensions_U2mon = models.StringField(choices=[[1, "left option"], [2,"right option"], [3, "both are identical"]], label ="Which option emits least CO2?",  widget = widgets.RadioSelect )
    comprehensions_U1carb = models.StringField(choices=[ [1, "21 lbs. CO2"], [2, "29 lbs. CO2"], [3, "32 lbs. CO2"]], label ="What are the maximum CO2 emissions you can cause in this choice situation?",  widget = widgets.RadioSelect )
    comprehensions_U2carb = models.StringField(choices=[[1, "22%"], [2,"38%"], [3, "62%"]], label ="What is the probability of causing 10 lbs. CO2 when you choose the right option?",  widget = widgets.RadioSelect )

    prolific_id = models.StringField()

    evmoA = models.FloatField()
    sdmoA = models.FloatField()
    evcoA = models.FloatField()
    sdcoA = models.FloatField()
    evmoB = models.FloatField()
    sdmoB = models.FloatField()
    evcoB = models.FloatField()
    sdcoB = models.FloatField()
    evdmo = models.FloatField()
    evdco = models.FloatField()
    sddmo = models.FloatField()
    sddco = models.FloatField()


    # @property
    # def response_time(player):
    #     if player.page_submit != None:
    #         return player.page_submit - player.page_load
        

#Instructions Certain trials (12)
class InstructionC1(Page): 
    form_model = 'player'
    form_fields = ["comprehensions_C1", "comprehensions_C2"]
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'carbonLeft': player.participant.carbonLeft,
            'totalRounds': C.NUM_ROUNDS
        }
    @staticmethod
    def is_displayed(player: Player):
        #show = (player.participant.certainFirst & player.round_number <=80) | (not player.participant.certainFirst & player.round_number >80 )
        return player.modRoundNumber == 1


#Instructions Certain trials (12) second part
class InstructionC2(Page): 
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        Q1correct = True if player.comprehensions_C1 == "3" else False
        Q2correct = True if  player.comprehensions_C2 == "2" else False
        player.participant.comprehension_C1_correct = Q1correct
        player.participant.comprehension_C2_correct = Q2correct
        bothcorrect = True if (Q1correct == True) & (Q2correct == True) else False
        nonecorrect = True if (Q1correct == False) & (Q2correct == False) else False
        return {
            'Q1correct': Q1correct, 
            'Q2correct': Q2correct,
            'bothcorrect': bothcorrect,
            'nonecorrect': nonecorrect,
            'carbonLeft': player.participant.carbonLeft
        }
    @staticmethod
    def is_displayed(player: Player):
        return player.modRoundNumber == 1
    
               
#Instructions Risky with monetary risky, trials (84) 
class InstructionMU1(Page): 
    form_model = 'player'
    form_fields = ["comprehensions_U1mon", "comprehensions_U2mon"]
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'carbonLeft': player.participant.carbonLeft,
            'totalRounds': C.NUM_ROUNDS - 13,
            'halftotalRounds': int((C.NUM_ROUNDS-13)/2)
        }
    @staticmethod
    def is_displayed(player: Player):
        return (player.modRoundNumber == 14 and player.MoneyRiskyFirst == True) or (player.modRoundNumber == 100 and player.MoneyRiskyFirst == False )
    
#Instructions Risky with emissions risky, trials (84) 
class InstructionCU1(Page): 
    form_model = 'player'
    form_fields = ["comprehensions_U1carb", "comprehensions_U2carb"]
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'carbonLeft': player.participant.carbonLeft,
            'totalRounds': C.NUM_ROUNDS - 13,
            'halftotalRounds': int((C.NUM_ROUNDS-13)/2)
        }
    @staticmethod
    def is_displayed(player: Player):
        return (player.modRoundNumber == 14 and player.MoneyRiskyFirst == False) or (player.modRoundNumber == 100 and player.MoneyRiskyFirst == True )
    
                     
   
#Instructions Risky with monetary risky, trials (84) second part
class InstructionMU2(Page): 
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        Q1correct = True if player.comprehensions_U1mon == "3" else False
        Q2correct = True if  player.comprehensions_U2mon == "2" else False
        player.participant.comprehension_U1_correct = Q1correct
        player.participant.comprehension_U2_correct = Q2correct
        bothcorrect = True if (Q1correct == True) & (Q2correct == True) else False
        nonecorrect = True if (Q1correct == False) & (Q2correct == False) else False
        return {
            'Q1correct': Q1correct, 
            'Q2correct': Q2correct,
            'bothcorrect': bothcorrect,
            'nonecorrect': nonecorrect,
            'carbonLeft': player.participant.carbonLeft
        }
    @staticmethod
    def is_displayed(player: Player):
        return (player.modRoundNumber == 14 and player.MoneyRiskyFirst == True) or (player.modRoundNumber == 100 and player.MoneyRiskyFirst == False )

#Instructions Complex with financial complex, trials (84) second part    
class InstructionCU2(Page): 
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        Q1correct = True if player.comprehensions_U1carb == "2" else False
        Q2correct = True if  player.comprehensions_U2carb == "3" else False
        player.participant.comprehension_Ub1_correct = Q1correct
        player.participant.comprehension_Ub2_correct = Q2correct
        bothcorrect = True if (Q1correct == True) & (Q2correct == True) else False
        nonecorrect = True if (Q1correct == False) & (Q2correct == False) else False
        return {
            'Q1correct': Q1correct, 
            'Q2correct': Q2correct,
            'bothcorrect': bothcorrect,
            'nonecorrect': nonecorrect,
            'carbonLeft': player.participant.carbonLeft
        }
    @staticmethod
    def is_displayed(player: Player):
        return (player.modRoundNumber == 14 and player.MoneyRiskyFirst == False) or (player.modRoundNumber == 100 and player.MoneyRiskyFirst == True )
    

class choiceTaskC(Page):
    form_model = 'player'
    form_fields = ["choice","input_keyboard", "page_load", "page_submit", "responsetime"]
    @staticmethod
    def vars_for_template(player: Player):
        if (player.modRoundNumber == 1):
            stimulusID = -99
            player.practice = True
            player.round_within_block = 1
        else:
            stimulusID = player.participant.seqCertain[(player.modRoundNumber - 2)]
            player.practice = False
            player.round_within_block = player.modRoundNumber - 1
            

        player.carbonLeft = player.participant.carbonLeft
        player.prolific_id = player.participant.label
        player.OptionARight = draw_random_number([0, 1])

       
        print("stimulusID",stimulusID)

        currentQuestion =  next((item for item in C.QUESTIONS_C if item["sid"] == stimulusID), None)
        #print(currentQuestion)

        player.moneyA =  int(currentQuestion['moA'])
        player.moneyB = int(currentQuestion['moB'])
        player.carbonA = int(currentQuestion['coA'])
        player.carbonB = int(currentQuestion['coB'])
        player.OptionARight = draw_random_number([0, 1])
        player.stimulusIDC = int(currentQuestion['sid_seb'])
        
        return {
            'reverse': player.OptionARight,
            'carbonLeft': player.participant.carbonLeft,
            'game_round': player.modRoundNumber,
            'totalRounds': 12,
            'halftotalRounds': int(C.NUM_ROUNDS/2),
            'practice': player.practice
        }
    @staticmethod
    def is_displayed(player: Player):
        return player.modRoundNumber <= 13


   
class choiceTaskU(Page):
    form_model = 'player'
    #form_fields = ["choice","input_keyboard", "page_load", "page_submit"]
    form_fields = ["choice","input_keyboard", "page_load", "page_submit", "responsetime"]
    @staticmethod
    def vars_for_template(player: Player):

        if (player.modRoundNumber < 16 or player.modRoundNumber == 100 or player.modRoundNumber == 101): ## has to be modified to < 19
            stimulusID = -992 - (player.modRoundNumber - 13)%84
            player.practice = True
            player.round_within_block = (player.modRoundNumber -13)%86
            if((player.modRoundNumber < 80 and player.MoneyRiskyFirst == True) or (player.modRoundNumber > 80 and player.MoneyRiskyFirst == False)):
                player.RiskyAttribute = "Money"
                if(player.modRoundNumber % 2 == 0):
                    player.RiskyOption = "B"
                    stimulusID = - 990
                else:
                    player.RiskyOption = "A"
                    stimulusID = - 992
            else:
                player.RiskyAttribute = "CO2"
                if(player.modRoundNumber % 2 == 0):
                    player.RiskyOption = "B"
                    stimulusID = - 991
                else:
                    player.RiskyOption = "A"
                    stimulusID = - 993
            
            
            player.OptionARight = 0
            #print(player.RiskyAttribute)
        # are we in the monetary or in the co2 complex block?
        elif( (player.modRoundNumber < 102 and player.MoneyRiskyFirst == True) or (player.modRoundNumber > 101 and player.MoneyRiskyFirst == False )):
            player.RiskyAttribute = "Money"
            player.OptionARight = draw_random_number([0, 1])
            stimulusID = player.participant.SeqRiskyMComplex[(player.modRoundNumber - 18)%84][0]
            player.RiskyOption = player.participant.SeqRiskyMComplex[(player.modRoundNumber - 18)%84][1]
            player.practice = False
            player.OptionARight = draw_random_number([0, 1])
            subtract_practice =  16 if player.modRoundNumber < 102 else 18 
            player.round_within_block = (player.modRoundNumber - subtract_practice)%84 +1
        else:
            player.RiskyAttribute = "CO2"
            player.OptionARight = draw_random_number([0, 1])
            stimulusID = player.participant.SeqRiskyMComplex[(player.modRoundNumber - 18)%84][0]
            player.RiskyOption = player.participant.SeqRiskyMComplex[(player.modRoundNumber - 18)%84][1]
            player.practice = False
            player.OptionARight = draw_random_number([0, 1])
            subtract_practice =  16 if player.modRoundNumber < 102 else 18 
            player.round_within_block = (player.modRoundNumber - subtract_practice)%84 +1


        print("stimulus U", stimulusID,  " complex attribute ", player.RiskyAttribute, " round number", player.round_number)
            

        #player.carbonLeft = player.participant.carbonLeft
        player.prolific_id = player.participant.label
        
        
        currentQuestion =  next((item for item in C.QUESTIONS_U if item["sid"] == stimulusID), None)
        #print(currentQuestion)

        player.stimulusIDU = int(currentQuestion['sid'])
        player.moneyA1 =  int(currentQuestion['moA1'])
        player.moneyA2 =  int(currentQuestion['moA2'])
        player.moneyB1 = int(currentQuestion['moB1'])
        player.moneyB2 = int(currentQuestion['moB2'])
        player.carbonA1 = int(currentQuestion['coA1'])
        player.carbonA2 = int(currentQuestion['coA2'])
        player.carbonB1 = int(currentQuestion['coB1'])
        player.carbonB2 = int(currentQuestion['coB2'])
        player.probA1 = (currentQuestion['pA1'])*100
        player.probA2 = int(100 - (currentQuestion['pA1'])*100)
        player.probB1 = (currentQuestion['pB1'])*100
        player.probB2 = int(100 - (currentQuestion['pB1'])*100)
        
        moneyA1 =  int(currentQuestion['moA1'])
        moneyA2 =  int(currentQuestion['moA2'])
        moneyB1 = int(currentQuestion['moB1'])
        moneyB2 = int(currentQuestion['moB2'])
        carbonA1 = int(currentQuestion['coA1'])
        carbonA2 = int(currentQuestion['coA2'])
        carbonB1 = int(currentQuestion['coB1'])
        carbonB2 = int(currentQuestion['coB2'])

        if(player.RiskyAttribute == "Money"):
            if(player.RiskyOption == "A"):
                moneyA1 = currentQuestion['moA1']
                moneyA2 = currentQuestion['moA2']
            else:
                moneyB1 = currentQuestion['moB1']
                moneyB2 = currentQuestion['moB2']
        else:
            if(player.RiskyOption == "A"):
                carbonA1 = currentQuestion['coA1']
                carbonA2 = currentQuestion['coA2']
            else:
                carbonB1 = currentQuestion['coB1']
                carbonB2 = currentQuestion['coB2']



        player.carbonLeft = player.participant.carbonLeft
        player.prolific_id = player.participant.label
        player.moAcertain = float(currentQuestion['moAcertain'])
        player.moBcertain = float(currentQuestion['moBcertain'])
        player.coAcertain = float(currentQuestion['coAcertain'])
        player.coBcertain = float(currentQuestion['coBcertain'])


    #region 
        if player.practice == False: 
            player.evmoA = float(currentQuestion['evmoA'])
            player.sdmoA = float(currentQuestion['sdmoA'])
            player.evcoA = float(currentQuestion['evcoA'])
            player.sdcoA = float(currentQuestion['sdcoA'])
            player.evmoB = float(currentQuestion['evmoB'])
            player.sdmoB = float(currentQuestion['sdmoB'])
            player.evcoB = float(currentQuestion['evcoB'])
            player.sdcoB = float(currentQuestion['sdcoB'])
            player.evdmo = float(currentQuestion['evdmo'])
            player.evdco = float(currentQuestion['evdco'])
            player.sddmo = float(currentQuestion['sddmo'])
            player.sddco = float(currentQuestion['sddco'])
           
    #endregion
        return {
            'reverse': player.OptionARight,
            'carbonLeft': player.participant.carbonLeft,
            'AoutcomeOneTop': player.OptionAoutcomeOneTop,
            'BoutcomeOneTop': player.OptionBoutcomeOneTop,
            'game_round': player.modRoundNumber, 
            'subtract_practice': 16 if player.modRoundNumber < 102 else 18 ,
            'totalRounds': C.NUM_ROUNDS - 13,
            'halftotalRounds': int((C.NUM_ROUNDS-13)/2),
            'moneyA' :   player.moAcertain,
            'moneyB' :   player.moBcertain,
            'carbonA' :   player.coAcertain,
            'carbonB' :   player.coBcertain,
            'moneyA1' :  moneyA1,
            'moneyA2' :  moneyA2,
            'moneyB1' : moneyB1,
            'moneyB2' : moneyB2,
            'carbonA1' : carbonA1,
            'carbonA2' : carbonA2,
            'carbonB1' : carbonB1,
            'carbonB2' : carbonB2, 
            'practice' : player.practice,
            'RiskyAtt': player.RiskyAttribute,
            'RiskyOpt': player.RiskyOption, 
            'sid': player.stimulusIDU
        }
    @staticmethod
    def is_displayed(player: Player):
        return player.modRoundNumber > 13
    


class betweenGames(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            (player.participant.CertainFirst == True and player.modRoundNumber == 13) | (player.participant.CertainFirst == False and player.round_number == 86 )
        )  



class betweenGames2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
             (player.participant.CertainFirst == True and player.modRoundNumber == 100) | (player.participant.CertainFirst == False and player.round_number == 173 )
        )  


class afterPractice(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'modroundnumber': player.modRoundNumber
        }
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.modRoundNumber == 1 or player.modRoundNumber == 15 or player.modRoundNumber == 101
        )





def outcome_certain(player: Player, drawn_round):
    round_choice = player.in_round(drawn_round).choice 
    if round_choice == "A":
        outcome_bonus_points = player.in_round(drawn_round).moneyA
        outcome_carbon = player.in_round(drawn_round).carbonA
    else: 
        outcome_bonus_points = player.in_round(drawn_round).moneyB
        outcome_carbon = player.in_round(drawn_round).carbonB

    ### recode for participants if what they saw was reversed  
    if player.in_round(drawn_round).OptionARight == 1 :
        if round_choice == "A":
            round_choice = "B"
        else: 
            round_choice = "A"
    return round_choice, outcome_bonus_points, outcome_carbon


def outcome_risky(player:Player, drawn_round):
    round_choice = player.in_round(drawn_round).choice 
    if round_choice == "A":
        rnd = random.random()
        if rnd < player.in_round(drawn_round).probA1:
            outcome_bonus_points = player.in_round(drawn_round).moneyA1
            outcome_carbon = player.in_round(drawn_round).carbonA1
        else:
            outcome_bonus_points = player.in_round(drawn_round).moneyA2
            outcome_carbon = player.in_round(drawn_round).carbonA2

    else: 
        rnd = random.random()
        if rnd < player.in_round(drawn_round).probB1:
            outcome_bonus_points = player.in_round(drawn_round).moneyB1
            outcome_carbon = player.in_round(drawn_round).carbonB1
        else:
            outcome_bonus_points = player.in_round(drawn_round).moneyB2
            outcome_carbon = player.in_round(drawn_round).carbonB2
    
    ### recode for participants if what they saw was reversed  
    if player.in_round(drawn_round).OptionARight == 1 :
        if round_choice == "A":
            round_choice = "B"
        else: 
            round_choice = "A"
    return round_choice, outcome_bonus_points, outcome_carbon


class afterTask(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        sum_correct = player.participant.comprehension_C1_correct + player.participant.comprehension_C2_correct + player.participant.comprehension_U1_correct + player.participant.comprehension_U2_correct + player.participant.comprehension_Ub1_correct + player.participant.comprehension_Ub2_correct
        drawn_round = player.in_round(1).drawn_round
        drawn_round_internal = player.participant.ModRoundArray[drawn_round - 1]
        drawn_game= "certain"
        if drawn_round_internal > 13:
            drawn_game = "risky"
        if(drawn_game == "risky"):
            relevant_round_choice, player.outcome_bonus_points, player.outcome_carbon = outcome_risky(player, drawn_round)
        else:
            relevant_round_choice, player.outcome_bonus_points, player.outcome_carbon = outcome_certain(player, drawn_round)
        if sum_correct >= 4:
            player.outcome_bonus_pound = player.outcome_bonus_points / 25
        else:
            player.outcome_bonus_pound = 0
        drawn_block = 1
        
        
        if drawn_game == "certain":
            drawn_block = 1 if player.participant.CertainFirst == True else 2 
            drawn_round_display = (drawn_round_internal - 16)%84 +1
        else: 
            drawn_block = 1 if player.participant.CertainFirst == False else 2 
            drawn_round_display = drawn_round_internal - 1
        
        player.participant.drawn_round_display = drawn_round_display
        player.participant.drawn_block = drawn_block
        player.participant.relevant_round_choice = relevant_round_choice
        player.participant.outcome_bonus_points = player.outcome_bonus_points
        player.participant.outcome_bonus_pound = player.outcome_bonus_pound
        player.participant.outcome_carbon  = player.outcome_carbon
        player.participant.sum_correct = sum_correct
        return{
            'sum_correct': sum_correct
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    

#page_sequence = [ InstructionC1, InstructionC2, InstructionU1, InstructionU2, choiceTaskU, questionnaire, Results]
page_sequence = [betweenGames2, InstructionC1, InstructionC2, InstructionMU1, InstructionMU2, InstructionCU1, InstructionCU2,  choiceTaskC, choiceTaskU, afterPractice, betweenGames, afterTask]