# =========================================================================================
#     Acknowledgement: Following code is developed gathering ideas from DEAP example
#     that found in URL:http://deap.readthedocs.io/en/master/examples/ga_onemax.html AND
#     Re-engineered by: Partha Barua, Student ID: 44598068, Date: 26/10/2017
# =========================================================================================

import random

from deap import base
from deap import creator
from deap import tools
#from random import randint
from collections import OrderedDict

MAX_GENERATIONS = 10

playersMove = []        # move of both players
myMove = {}             # my move
oppMove = {}            # opponent's move
oppMove = OrderedDict()    

creator.create("FitnessMax", base.Fitness, weights=(1.0,))                           # TFTStrat As Tit-Fot-2Tat Strategy   
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator 
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of 100 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, 10)   # 10 digits long chromosomes

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):                                                         # Fitness function for 'Confess'
    return sum(individual), 
def evalZero(individual):                                                           # Fitness function for 'Defect'
    return sum(individual)-sum(individual),
#-------------------------------------------------------------------------
# Operator registration
#-------------------------------------------------------------------------
# register the goal / fitness function
toolbox.register("evaluate1", evalOneMax)
toolbox.register("evaluate0", evalZero)
# register the crossover operator
toolbox.register("mate", tools.cxOnePoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)
#-------------------------------------------------------------------------

# Operation 1: Convert individuals into bit-strings:
def convIndToBs(p):
    pop = p
    s = ""
    inds = []
    for e in pop:
        for i in e:
            s += str(i)                                                             # concatenate all the list elements
        inds.append (s)
        s = ""
    return inds

# Operation 2: Convert game-turns into bit-strings
def convTurnsToBs(t):
    lst_Bs = []
    s = ""
    for iter in range (1,t+1):                                                      # iterates no. of turns
        bsOfIter = bin(iter)[2:]                                                    # convert each iteration (turn) into bitstring
        addZero = 7-len(bsOfIter)                                                   # calculate no. of zeros to make it 7 digits long 
        for times in range (1, addZero+1):
            s += str(0)                                                             # concatenate all the zeros no. of times
        s +=str(bsOfIter)                                                           # concatenate the turn at the end of the zeros
        lst_Bs.append(s)                                                            # add all the turns in to list
        s = ""                                                                      # reset the sequence(s)
        iter  = iter + 1                                                            # go to next turn
    return lst_Bs

# Operation 3: Concatenating players (11/00) with the bit-string
def concatPlayers(op_No,ply, bs):
    s = ""
    if int(op_No) == 1:
         
        pop = bs
        gT_Pop = [] 

        for ind in pop:
             s = str(ind) + str(11)                                                 # 11 as me
             gT_Pop.append(s)
             s = str(ind) + str(0) + str(0)                                         # 00 as computer
             gT_Pop.append(s)

    elif int(op_No) == 2:
        
        if int(ply) == 1:
            s = str(bs) + str(11)                                                   # 11 as me
        elif int(ply) == 0:
            s = str(bs) + str(0) + str(0)                                           # 00 as computer
 
        gT_Pop = s
        
    return gT_Pop

# Operation 4: Concatenating player choices(confess/defect)
def concatChoices(op_No,choice, bs):
    s = ""
    if int(op_No) == 1:
        
        chosenPop = [] 
        pop = bs
        for ind in pop:
             s = str(ind) + str(1)             
             chosenPop.append(s)
             s = str(ind) + str(0)             
             chosenPop.append(s)

    elif int(op_No) == 2:

        if int(choice) == 1:
            s = str(bs) + str(1)                                                    # 1 as 'confess' i.e. individuals with confess choice
        elif int(choice) == 0: 
            s = str(bs) + str(0)                                                    # 0 as 'defect' i.e. individuals with defect choice
        chosenPop = s

    return chosenPop


# **********************
# Begin the evolution
# **********************
    
def evolution(pop, operation_No):
    
    # CXPB  is the probability with which two individuals are crossed
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2                                                                                           
    
     # Evaluate the entire population
    if operation_No == 1:
        fitnesses = list(map(toolbox.evaluate1, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
    else:
        fitnesses = list(map(toolbox.evaluate0, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
    # Extracting all the fitnesses of 
    fits = [ind.fitness.values[0] for ind in pop]
    # Variable keeping track of the number of generations
    g = 0
    # Begin the evolution
    while max(fits) < 10 and g < 100:    
        # A new generation
        g = g + 1
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
  
        if operation_No == 1:
            fitnesses = map(toolbox.evaluate1, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
        else:
            fitnesses = map(toolbox.evaluate0, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
         
    return fits   
    

def sevenDigitsBs(n):
    s = ""   
    bsOfIter = bin(n)[2:]                                                           #  convert each iteration (turn) into bitstring
    addZero = 7-len(bsOfIter)                                                       #  calculate no. of zeros to make it 7 digits long 
    for times in range (1, addZero+1):
        s += str(0)                                                                 #  concatenate all the zeros no. of times
    s += str(bsOfIter) 
    bs = s
    return bs

def strategy(oppMove):
    # ---------------------------------------------Comments: ---------------------------------------------------
    #         Input Parameter:   Opponent's move as [oppMove = CC, DD, CD or DC]
    #                   NOTES:   I used 'Tit for Two Tats' strategy for my move, mentioned down below.
    #                            In this strategy, it only looks back 2 moves of the opponent (from history).
    #  TO CHANGE MEMORY DEPTH:   1. Send an input string of no. of moves to lookup
    #                               for example: [oppMove = CCC, DDD, CDC ..etc.]
    #                               (code is already designed to adjust unlimited history)
    #                            2. Change the strategy lookup table to {'CCC': 'C', 'DCD': 'D' .... etc.}
    #                            3. Find my move using key value of the lookup dict.
    # ---------------------------------------------------------------------------------------------------------
    lookup_table = {
                    'CC': 'C',
                    'CD': 'C',
                    'DC': 'C',
                    'DD': 'D', 
                    }
    if len(oppMove) < 2:
       #  my First move always 'C'
       return 'C'      
    else:
        #  passing oppnent's move as [KEY VALUE], i get my move from the lookup.
        my_action = lookup_table[oppMove] 
        return my_action


# Get a random chromosome from solution candidates
def getRandomChrom(candidates):
    ss_candidates = candidates
    random.seed(None)
    chro = random.choice(ss_candidates)
    return chro

# populating 7 digits binary serial number 
def getTurn(candidates, slNo):
    slNo = slNo - 1                                                                 #  starts from 0
    newList = []                 
    cnds = candidates
    for i in cnds:
        i = i[0:7]
        if i not in newList:                                                        #  removing the duplicate values
           newList.append(i[0:7]) 
    newList.sort()
    return newList[slNo]

def getRandomPopulation():
    random.seed(64)
    pop = toolbox.population(n=20)   
    
    return pop

def myStrategy(opp_History):   
    #looks back 2 moves from the history
    memory_depth = -2
    history = opp_History[0]  
    # get the key (2 memory depth) from the opponent's history                                                      #  get the key value from the tuple
    key_hist = history[memory_depth:len(history)]                                              #  I will only lookup last 2 moves (opponent's) from the history <<<
    #get my strategy using the key value
    return strategy(key_hist)                                                        #  check my strategy

#  ==================================================
#  Calculation of a populations's FITNESS PERFORMANCE
#  ==================================================
def cal_Performance(noOfRound):
    
    no_of_Rounds = noOfRound                                                        #   More than 1 game will be played    
    history_length = no_of_Rounds                                                   #   Storage capacity of the opponent's 'Move_History' as per game turns
    opp_Memory = {}                                                                 #   opponent's main memory/history
    playersMove = []
    game_Info = {}
    score = {'DD':'1,1','DC':'5,0','CD':'0,5','CC':'3,3'}                           #   payoff matrix
    s_History=''
    
    
    for r_Round in range(1, no_of_Rounds + 1):
        # to make random 0 or 1
        random.seed(None)
        # get the computer's move
        opp_Choice = random.randint(0,1)
        if opp_Choice == 0:
           opp_Move = 'D'   
        else:
           opp_Move = 'C'
         # keep track of computer's moves for all the turns in its memory[opp_Memory]
        if len(opp_Memory) == 0: 
            opp_Memory[opp_Move] = opp_Move                                         #   initialized first memory value
        else:
            if len(opp_Memory) <= (history_length-1):                               #   checks the storage limit
                items = list(opp_Memory.items())
                last_itm = items[-1]                                                #   pick the last item from the memory
                addNextMoveToPrev = last_itm[0] + opp_Move                          #   prepare [new key] by adding next move to the prev move 
                s_History = addNextMoveToPrev
                opp_Memory[addNextMoveToPrev] = opp_Move                            #   add [next move] to the [new key]
            else:
                break

        # move history of the opponent 
        game_Info['OPP_HISTORY'] = s_History
        i = list(opp_Memory.items())                                                #   get all the items from the memory 
        history = i[-1]                                                             #   pick last item as [Main_History] of the opponent
        # get my move using TF2T strategy (i.e. make move looking up opponent's last two moves mentioned above in the lookup table)
        m_move = myStrategy(history)
        # ===============================================================================
        # get a random population and evolve until meets the fitness function requirments
        pop = getRandomPopulation()  
        # ===============================================================================
        if m_move =='C':
           # evolve each individual to be all 1's in their gense
           fits = evolution(pop, 1)                                 
        else:
            # evolve each individual to be all 0's in their gense
           fits = evolution(pop, 0)   
        #  *************************** FITNESS FUNCTION **************************     
        #  'Defect' if all individual's max(fits)) value == o, otherwiese 'Confess  
        #  ***********************************************************************                              
        if float(max(fits)) == 0.0:                                 
            my_Move = 'D'                                          
        else:
            my_Move = 'C'
        
        # ================================================================    
        # INSIDE FOR LOOP: SAVE ALL THE MOVES FROM BOTH PLAYERS USING LOOP    
        # ================================================================ 
        playersMove.append(my_Move + opp_Move)                                      # <<<<<<< To apply game strategy change comp_Move to s_History (computer's)

    # =======================    
    # OUTSIDE ABOVE FOR LOOP:    
    # =======================
    # initialize values
    total_win  = 0
    total_lost = 0
    total_draw = 0
    
    indx = 0
    lstMoves = []
    for i in playersMove:
        
        # ============================================================
        # Binary Representation of players as chromosome (bit-strings)
        # ============================================================
        
        # a list of binary digists (7) starts [from 1 to No. of rounds]
        bs_Round = convTurnsToBs(no_of_Rounds)                                  
        # Creates 9 digits long bit-strings (7: for serial no. + 2: identifying players)
        # pop item as per serial number of the loop
        ply1 = concatPlayers(2,1, bs_Round[indx])                                   # para 1 as me
        ply2 = concatPlayers(2,0, bs_Round[indx])                                   # para 0 as computer
        
        # first pair of moves from the players list
        # always in a form of [CD] or [DC]
        moves = i    
        # player1: me
        # player2: computer                    
        player1 = moves[-2]   # 1st Charc
        player2 = moves[-1]   # 2nd Charc
        
        # move(choice) allocation
        # concate 1 more digit for player's choice of decision or move
        if player1 == 'C':
            bs_p1 = concatChoices(2, 1, ply1)
        elif player1 == 'D':
            bs_p1 = concatChoices(2, 0, ply1)    
        if player2 == 'C':
            bs_p2 = concatChoices(2, 1, ply2)
        elif player2 == 'D':
            bs_p2 = concatChoices(2, 0, ply2)    
        
        # adding each pair of moves into list
        # example: Moves: CD = 20 digits [player 1 = 10 digits + player 2 = 10 digits]
        full_bs = str(bs_p1)+str(bs_p2)
        lstMoves.append(full_bs)                                                    # <<<<< adding full 20 digits bit-string as pair of moves for 2 players 
        # =======================  
        # inside For-Loop:    
        indx = indx + 1
        # ======================= 
    # =======================    
    # OUTSIDE AVOVE FOR LOOP:    
    # =======================    
    indx = 0                                                                        # resetting for above for loop
    for i in playersMove:   
        
        for j in score:    
            
            if i == j:                               
               e = score[j]                                                         #  retriveing payoff value
               myYears = int(e[0])
               oppYears = int(e[2])
              # Result criteria
               if myYears < oppYears:
                  total_win = total_win + 1
               elif myYears == oppYears:
                    total_draw = total_draw + 1
               elif myYears > oppYears:
                   total_lost = total_lost + 1
 
    # percentage of Winning that has been played in many rouds in a GAME.
    gameWinningRate = int((total_win/no_of_Rounds) * 100)  # winning rate
    game_Info['NO_OF_ROUNDS']   =  no_of_Rounds
    # moves that have been played by both players in a dictionary
    game_Info['MOVES']          = lstMoves                               
    game_Info['WINNING_RATE']   =  gameWinningRate 
    game_Info['TOTAL_WIN']      =  total_win 
    game_Info['TOTAL_LOST']     =  total_lost 
    game_Info['TOTAL_DRAWS']    =  total_draw 
    
    
    return game_Info                                                                # caller (__main__:)

if __name__ == "__main__":
    
    # *********************
    #        MAIN
    # *********************
    print('Loading...')

    noOfGens = MAX_GENERATIONS                                                      # <<< --- NO OF GAMES TO PLAY <<<                                       
    gameRound = 5                                                                   # <<< ---  Turns: Chage to play more rounds in one game <<<
    games = []                                                                      #   stores info about each game hat has been played
    slNo = 1
    avgWin = 0
    avgLose = 0
    avgDraw = 0
    avgWinRate = 0
    avgR = 0
    avgD = 0
    avgL = 0

    while slNo <= noOfGens:                                                         # THESE ARE GAMES. IN ONE GAME MANY ROUNDS.
        game = cal_Performance(gameRound)                                           # Returns score after playing with the opponent (computer). 
        games.append(game)   
        slNo = slNo + 1
    # ============
    # OUTSIDE LOOP
    # ============
    # game counter
    cntGame = 1
    # initializing tournament's parameters
    totalWins = 0
    totaLosts = 0
    totalDraws = 0
    totalWinningRates = 0
    history =''
    
    
    # Display scores for all games played
    for g in games:
        
        # Display game result
        print('My Score of Game No. ', str(cntGame))
        print('             Total Round played:' , g.get('NO_OF_ROUNDS'))
        print('        Moves played by players:' , g.get('MOVES'))
        print('                      Total Win:' , g.get('TOTAL_WIN'))
        print('                     Total Lost:' , g.get('TOTAL_LOST'))
        print('                    Total Draws:' , g.get('TOTAL_DRAWS'))
        print('-----------------------------------------------------')
        print('My Winning Rate of This Game(%):' , g.get('WINNING_RATE'))
        print('-----------------------------------------------------')
        print("\n")

        # calculate my tournament prformance where i played many games in many rounds
        totalWins           = totalWins + int(g.get('TOTAL_WIN'))
        totaLosts           = totaLosts + int(g.get('TOTAL_LOST'))
        totalDraws          = totalDraws + int(g.get('TOTAL_DRAWS'))
        totalWinningRates   = totalWinningRates + float(g.get('WINNING_RATE'))
        history             = g.get('OPP_HISTORY')
        
        cntGame = cntGame + 1

    # ================
    # OUTSIDE FOR LOOP
    # ================
    print('********************************************************************************************************************************')
    print('********************************************************************************************************************************')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  MY TOTAL PERFORMANC <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('********************************************************************************************************************************')
    print('********************************************************************************************************************************')
    print('Memory Depth: 2 (TF2T)')
    print('History (opp):',  history)   
    print('Strategy Used: TIT FOR 2 TAT (i.e. Defect if opponent' + '\'s' + ' last 2 moves are defected, otherwise always confess)')
    print('Game Plan: (1) get a random computer move as opponent' + '\'s' + ' (2) Lookup my move from the TF2T table (3) Generate a random population') 
    print('           (4) Evolve (mutate/crossover) populaiton as per my fitness Fucntion i.e. my TFTT' + '\'s' + ' lookup moves')
    print('           (5) Represent all moves as bit-strings chromosomes and Finally (6) Display Result...')     
    print('--------------------------------------------------------------------------------------------------------------------------------')
    print("\n")
    T_ROUND = noOfGens * gameRound
    print('--------------------------------------------------------------------------------------------------------------------------------')
    print('    -: Total No. of Tournaments Played ' + str(noOfGens) + ', ' +  str(T_ROUND) + ' total round(s) :-')
    print('--------------------------------------------------------------------------------------------------------------------------------')
    print('                                 : ROUNDS')
    print('My Total Wins                    :', str(totalWins))
    print('My Total Loses                   :', str(totaLosts))
    print('My Total Draws                   :', str(totalDraws))
    print('--------------------------------------------------------------------------------------------------------------------------------')
    
    
    # Average tournament performance:   
    
    w    = totalWins/noOfGens                  
    l   = totaLosts/noOfGens                                                                                
    d   = totalDraws/noOfGens
    twr = totalWinningRates/noOfGens
    print('-------------------------------------------------------------------------------------------------------------------------------')
    print('AVERAGES >>')
    print('-------------------------------------------------------------------------------------------------------------------------------')
    print('                Average Winning(%):', str(w))
    print('                  Average Loses(%):', str(l))
    print('                  Average Draws(%):', str(d))
    print('Average Tournament Winning Rate(%):', str(twr))
    print('******************************************************************************************************************************')
    print('****************************************************** THANK YOU *************************************************************')
    
    
    
    
    

    