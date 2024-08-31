

import argparse
import numpy as np 
import math 
from pathlib import Path
from pulp import *

def get_arguments():
    parser = argparse.ArgumentParser(description="Encoder ")

    #Add the arguments to the parser 
    parser.add_argument('--opponent', metavar='--opponent', type=Path, \
                        help='Stores the location of the opponent policy')
    parser.add_argument('--p', metavar='--p', type = float, \
                        help='Skill parameter p')
    parser.add_argument('--q', metavar='q', type = float, \
                        help = 'Skill parameter q')
    #Perform parsing of the arguments 
    args = parser.parse_args()

    #Store the parsed arguments into local variables
    return args.opponent, args.p, args.q

def state_encoder(state_string):
    if state_string[0] == '0':
        B1_state = int(state_string[1])
    elif state_string[0] == '1':
        B1_state = int(state_string[0:2])
    if state_string[2] == '0':
        B2_state = int(state_string[3])
    elif state_string[2] == '1':
        B2_state = int(state_string[2:4])
    if state_string[4] == '0':
        R_state = int(state_string[5])
    elif state_string[4] == '1':
        R_state = int(state_string[4:6])
    poss = int(state_string[-1])
    state_encoding = int((B1_state - 1)*512 + (B2_state - 1)*32 + (R_state - 1)*2 + poss - 1)
    return state_encoding

def get_broken_down_states(state_string): 
    if state_string[0] == '0':
        B1_state = int(state_string[1])
    elif state_string[0] == '1':
        B1_state = int(state_string[0:2])
    if state_string[2] == '0':
        B2_state = int(state_string[3])
    elif state_string[2] == '1':
        B2_state = int(state_string[2:4])
    if state_string[4] == '0':
        R_state = int(state_string[5])
    elif state_string[4] == '1':
        R_state = int(state_string[4:6])
    poss = int(state_string[-1])
    return B1_state, B2_state, R_state, poss

def state_decoder(number): 
    B1 = math.floor(number/512) + 1 
    if B1 < 10: 
        B1 = '0' + str(B1)
    else:
        B1 = str(B1)
    B2 = math.floor((number%512)/32) + 1 
    if B2 < 10: 
        B2 = '0' + str(B2)
    else:
        B2 = str(B2)
    R = math.floor(((number%512)%32)/2) + 1 
    if R < 10: 
        R = '0' + str(R)
    else:
        R = str(R)
    poss = str(number%2 + 1)
    string_format = B1 + B2 + R + poss
    return string_format

def create_policy_matrix(opponent_file_path):
    file = open(opponent_file_path, 'r')
    lines_of_file = file.readlines()
    num_states = 8192 #Constant number of states in every MDP
    num_actions_R = 4 #Left, Right, Up, Down (LRUD)
    policy_matrix = np.zeros((num_states, num_actions_R))
    len_file = len(lines_of_file) #Should be 8193
    for i in range(1, len_file):
        split_line = lines_of_file[i][:-1].split(' ')
        state_string = split_line[0]
        encoded_state = state_encoder(state_string)
        left = float(split_line[1])
        right = float(split_line[2])
        up = float(split_line[3])
        down = float(split_line[4])
        policy_matrix[encoded_state][0] = left
        policy_matrix[encoded_state][1] = right
        policy_matrix[encoded_state][2] = up
        policy_matrix[encoded_state][3] = down
    return policy_matrix

def left_operator(state_string, move_whom): #Move_whom is 1 for B1, 2 for B2 and 3 for R
    B1 = state_string[0:2]
    B2 = state_string[2:4]
    R  = state_string[4:6]
    poss = state_string[-1]
    if move_whom == 1: 
        if B1 == '02':
            new_state = '01' + B2 + R + poss 
            return new_state
        elif B1 == '03':
            new_state = '02' + B2 + R + poss 
            return new_state
        elif B1 == '04':
            new_state = '03' + B2 + R + poss 
            return new_state
        elif B1 == '06':
            new_state = '05' + B2 + R + poss 
            return new_state
        elif B1 == '07':
            new_state = '06' + B2 + R + poss 
            return new_state
        elif B1 == '08':
            new_state = '07' + B2 + R + poss 
            return new_state
        elif B1 == '10':
            new_state = '09' + B2 + R + poss 
            return new_state
        elif B1 == '11':
            new_state = '10' + B2 + R + poss 
            return new_state
        elif B1 == '12':
            new_state = '11' + B2 + R + poss 
            return new_state
        elif B1 == '14':
            new_state = '13' + B2 + R + poss 
            return new_state
        elif B1 == '15':
            new_state = '14' + B2 + R + poss 
            return new_state
        elif B1 == '16':
            new_state = '15' + B2 + R + poss 
            return new_state
    elif move_whom == 2: 
        if B2 == '02': 
            new_state = B1 + '01' + R + poss
            return new_state
        elif B2 == '03': 
            new_state = B1 + '02' + R + poss
            return new_state
        elif B2 == '04': 
            new_state = B1 + '03' + R + poss
            return new_state
        elif B2 == '06': 
            new_state = B1 + '05' + R + poss
            return new_state
        elif B2 == '07': 
            new_state = B1 + '06' + R + poss
            return new_state
        elif B2 == '08': 
            new_state = B1 + '07' + R + poss
            return new_state
        elif B2 == '10': 
            new_state = B1 + '09' + R + poss
            return new_state
        elif B2 == '11': 
            new_state = B1 + '10' + R + poss
            return new_state
        elif B2 == '12': 
            new_state = B1 + '11' + R + poss
            return new_state
        elif B2 == '14': 
            new_state = B1 + '13' + R + poss
            return new_state
        elif B2 == '15': 
            new_state = B1 + '14' + R + poss
            return new_state
        elif B2 == '16': 
            new_state = B1 + '15' + R + poss
            return new_state
    elif move_whom == 3: 
        if R == '02': 
            new_state = B1 + B2 + '01' + poss
            return new_state
        elif R == '03': 
            new_state = B1 + B2 + '02' + poss
            return new_state
        elif R == '04': 
            new_state = B1 + B2 + '03' + poss
            return new_state
        elif R == '06': 
            new_state = B1 + B2 + '05' + poss
            return new_state
        elif R == '07': 
            new_state = B1 + B2 + '06' + poss
            return new_state
        elif R == '08': 
            new_state = B1 + B2 + '07' + poss
            return new_state
        elif R == '10': 
            new_state = B1 + B2 + '09' + poss
            return new_state
        elif R == '11': 
            new_state = B1 + B2 + '10' + poss
            return new_state
        elif R == '12': 
            new_state = B1 + B2 + '11' + poss
            return new_state
        elif R == '14': 
            new_state = B1 + B2 + '13' + poss
            return new_state
        elif R == '15': 
            new_state = B1 + B2 + '14' + poss
            return new_state
        elif R == '16': 
            new_state = B1 + B2 + '15' + poss
            return new_state

def right_operator(state_string, move_whom): #Move_whom is 1 for B1, 2 for B2 and 3 for R
    B1 = state_string[0:2]
    B2 = state_string[2:4]
    R  = state_string[4:6]
    poss = state_string[-1]
    if move_whom == 1: 
        if B1 == '01':
            new_state = '02' + B2 + R + poss 
            return new_state
        elif B1 == '02':
            new_state = '03' + B2 + R + poss 
            return new_state
        elif B1 == '03':
            new_state = '04' + B2 + R + poss 
            return new_state
        elif B1 == '05':
            new_state = '06' + B2 + R + poss 
            return new_state
        elif B1 == '06':
            new_state = '07' + B2 + R + poss 
            return new_state
        elif B1 == '07':
            new_state = '08' + B2 + R + poss 
            return new_state
        elif B1 == '09':
            new_state = '10' + B2 + R + poss 
            return new_state
        elif B1 == '10':
            new_state = '11' + B2 + R + poss 
            return new_state
        elif B1 == '11':
            new_state = '12' + B2 + R + poss 
            return new_state
        elif B1 == '13':
            new_state = '14' + B2 + R + poss 
            return new_state
        elif B1 == '14':
            new_state = '15' + B2 + R + poss 
            return new_state
        elif B1 == '15':
            new_state = '16' + B2 + R + poss 
            return new_state
    elif move_whom == 2: 
        if B2 == '01': 
            new_state = B1 + '02' + R + poss
            return new_state
        elif B2 == '02': 
            new_state = B1 + '03' + R + poss
            return new_state
        elif B2 == '03': 
            new_state = B1 + '04' + R + poss
            return new_state
        elif B2 == '05': 
            new_state = B1 + '06' + R + poss
            return new_state
        elif B2 == '06': 
            new_state = B1 + '07' + R + poss
            return new_state
        elif B2 == '07': 
            new_state = B1 + '08' + R + poss
            return new_state
        elif B2 == '09': 
            new_state = B1 + '10' + R + poss
            return new_state
        elif B2 == '10': 
            new_state = B1 + '11' + R + poss
            return new_state
        elif B2 == '11': 
            new_state = B1 + '12' + R + poss
            return new_state
        elif B2 == '13': 
            new_state = B1 + '14' + R + poss
            return new_state
        elif B2 == '14': 
            new_state = B1 + '15' + R + poss
            return new_state
        elif B2 == '15': 
            new_state = B1 + '16' + R + poss
            return new_state
    elif move_whom == 3: 
        if R == '01': 
            new_state = B1 + B2 + '02' + poss
            return new_state
        elif R == '02': 
            new_state = B1 + B2 + '03' + poss
            return new_state
        elif R == '03': 
            new_state = B1 + B2 + '04' + poss
            return new_state
        elif R == '05': 
            new_state = B1 + B2 + '06' + poss
            return new_state
        elif R == '06': 
            new_state = B1 + B2 + '07' + poss
            return new_state
        elif R == '07': 
            new_state = B1 + B2 + '08' + poss
            return new_state
        elif R == '09': 
            new_state = B1 + B2 + '10' + poss
            return new_state
        elif R == '10': 
            new_state = B1 + B2 + '11' + poss
            return new_state
        elif R == '11': 
            new_state = B1 + B2 + '12' + poss
            return new_state
        elif R == '13': 
            new_state = B1 + B2 + '14' + poss
            return new_state
        elif R == '14': 
            new_state = B1 + B2 + '15' + poss
            return new_state
        elif R == '15': 
            new_state = B1 + B2 + '16' + poss
            return new_state

def up_operator(state_string, move_whom): #Move_whom is 1 for B1, 2 for B2 and 3 for R
    B1 = state_string[0:2]
    B2 = state_string[2:4]
    R  = state_string[4:6]
    poss = state_string[-1]
    if move_whom == 1: 
        if B1 == '05':
            new_state = '01' + B2 + R + poss 
            return new_state
        elif B1 == '06':
            new_state = '02' + B2 + R + poss 
            return new_state
        elif B1 == '07':
            new_state = '03' + B2 + R + poss 
            return new_state
        elif B1 == '08':
            new_state = '04' + B2 + R + poss 
            return new_state
        elif B1 == '09':
            new_state = '05' + B2 + R + poss 
            return new_state
        elif B1 == '10':
            new_state = '06' + B2 + R + poss 
            return new_state
        elif B1 == '11':
            new_state = '07' + B2 + R + poss 
            return new_state
        elif B1 == '12':
            new_state = '08' + B2 + R + poss 
            return new_state
        elif B1 == '13':
            new_state = '09' + B2 + R + poss 
            return new_state
        elif B1 == '14':
            new_state = '10' + B2 + R + poss 
            return new_state
        elif B1 == '15':
            new_state = '11' + B2 + R + poss 
            return new_state
        elif B1 == '16':
            new_state = '12' + B2 + R + poss 
            return new_state
    elif move_whom == 2: 
        if B2 == '05': 
            new_state = B1 + '01' + R + poss
            return new_state
        elif B2 == '06': 
            new_state = B1 + '02' + R + poss
            return new_state
        elif B2 == '07': 
            new_state = B1 + '03' + R + poss
            return new_state
        elif B2 == '08': 
            new_state = B1 + '04' + R + poss
            return new_state
        elif B2 == '09': 
            new_state = B1 + '05' + R + poss
            return new_state
        elif B2 == '10': 
            new_state = B1 + '06' + R + poss
            return new_state
        elif B2 == '11': 
            new_state = B1 + '07' + R + poss
            return new_state
        elif B2 == '12': 
            new_state = B1 + '08' + R + poss
            return new_state
        elif B2 == '13': 
            new_state = B1 + '09' + R + poss
            return new_state
        elif B2 == '14': 
            new_state = B1 + '10' + R + poss
            return new_state
        elif B2 == '15': 
            new_state = B1 + '11' + R + poss
            return new_state
        elif B2 == '16': 
            new_state = B1 + '12' + R + poss
            return new_state
    elif move_whom == 3: 
        if R == '05': 
            new_state = B1 + B2 + '01' + poss
            return new_state
        elif R == '06': 
            new_state = B1 + B2 + '02' + poss
            return new_state
        elif R == '07': 
            new_state = B1 + B2 + '03' + poss
            return new_state
        elif R == '08': 
            new_state = B1 + B2 + '04' + poss
            return new_state
        elif R == '09': 
            new_state = B1 + B2 + '05' + poss
            return new_state
        elif R == '10': 
            new_state = B1 + B2 + '06' + poss
            return new_state
        elif R == '11': 
            new_state = B1 + B2 + '07' + poss
            return new_state
        elif R == '12': 
            new_state = B1 + B2 + '08' + poss
            return new_state
        elif R == '13': 
            new_state = B1 + B2 + '09' + poss
            return new_state
        elif R == '14': 
            new_state = B1 + B2 + '10' + poss
            return new_state
        elif R == '15': 
            new_state = B1 + B2 + '11' + poss
            return new_state
        elif R == '16': 
            new_state = B1 + B2 + '12' + poss
            return new_state

def down_operator(state_string, move_whom): #Move_whom is 1 for B1, 2 for B2 and 3 for R
    B1 = state_string[0:2]
    B2 = state_string[2:4]
    R  = state_string[4:6]
    poss = state_string[-1]
    if move_whom == 1: 
        if B1 == '01':
            new_state = '05' + B2 + R + poss 
            return new_state
        elif B1 == '02':
            new_state = '06' + B2 + R + poss 
            return new_state
        elif B1 == '03':
            new_state = '07' + B2 + R + poss 
            return new_state
        elif B1 == '04':
            new_state = '08' + B2 + R + poss 
            return new_state
        elif B1 == '05':
            new_state = '09' + B2 + R + poss 
            return new_state
        elif B1 == '06':
            new_state = '10' + B2 + R + poss 
            return new_state
        elif B1 == '07':
            new_state = '11' + B2 + R + poss 
            return new_state
        elif B1 == '08':
            new_state = '12' + B2 + R + poss 
            return new_state
        elif B1 == '09':
            new_state = '13' + B2 + R + poss 
            return new_state
        elif B1 == '10':
            new_state = '14' + B2 + R + poss 
            return new_state
        elif B1 == '11':
            new_state = '15' + B2 + R + poss 
            return new_state
        elif B1 == '12':
            new_state = '16' + B2 + R + poss 
            return new_state
    elif move_whom == 2: 
        if B2 == '01': 
            new_state = B1 + '05' + R + poss
            return new_state
        elif B2 == '02': 
            new_state = B1 + '06' + R + poss
            return new_state
        elif B2 == '03': 
            new_state = B1 + '07' + R + poss
            return new_state
        elif B2 == '04': 
            new_state = B1 + '08' + R + poss
            return new_state
        elif B2 == '05': 
            new_state = B1 + '09' + R + poss
            return new_state
        elif B2 == '06': 
            new_state = B1 + '10' + R + poss
            return new_state
        elif B2 == '07': 
            new_state = B1 + '11' + R + poss
            return new_state
        elif B2 == '08': 
            new_state = B1 + '12' + R + poss
            return new_state
        elif B2 == '09': 
            new_state = B1 + '13' + R + poss
            return new_state
        elif B2 == '10': 
            new_state = B1 + '14' + R + poss
            return new_state
        elif B2 == '11': 
            new_state = B1 + '15' + R + poss
            return new_state
        elif B2 == '12': 
            new_state = B1 + '16' + R + poss
            return new_state
    elif move_whom == 3: 
        if R == '01': 
            new_state = B1 + B2 + '05' + poss
            return new_state
        elif R == '02': 
            new_state = B1 + B2 + '06' + poss
            return new_state
        elif R == '03': 
            new_state = B1 + B2 + '07' + poss
            return new_state
        elif R == '04': 
            new_state = B1 + B2 + '08' + poss
            return new_state
        elif R == '05': 
            new_state = B1 + B2 + '09' + poss
            return new_state
        elif R == '06': 
            new_state = B1 + B2 + '10' + poss
            return new_state
        elif R == '07': 
            new_state = B1 + B2 + '11' + poss
            return new_state
        elif R == '08': 
            new_state = B1 + B2 + '12' + poss
            return new_state
        elif R == '09': 
            new_state = B1 + B2 + '13' + poss
            return new_state
        elif R == '10': 
            new_state = B1 + B2 + '14' + poss
            return new_state
        elif R == '11': 
            new_state = B1 + B2 + '15' + poss
            return new_state
        elif R == '12': 
            new_state = B1 + B2 + '16' + poss
            return new_state

def check_is_tackle(initial_string, action, final_string):
    who_moved = 0
    if (action == 0) or (action == 1) or (action == 2) or (action == 3):
        who_moved = 1
    elif (action == 4) or (action == 5) or (action == 6) or (action == 7):
        who_moved = 2
    else: 
        return False
    possession_final = int(final_string[-1])
    if who_moved != possession_final:
        return False
    if who_moved == 1: 
        if (final_string[0:2] == final_string[4:6]):
            return True
        elif (initial_string[0:2] == final_string[4:6]) and (initial_string[4:6] == final_string[0:2]):
            return True
        else:
            return False
    if who_moved == 2: 
        if (final_string[2:4] == final_string[4:6]):
            return True
        elif (initial_string[2:4] == final_string[4:6]) and (initial_string[4:6] == final_string[2:4]):
            return True
        else:
            return False

def change_possession(initial_string): 
    before_poss = initial_string[:-1]
    poss        = initial_string[-1]
    if poss == '1':
        new_poss = '2'
    elif poss == '2':
        new_poss = '1'
    final_string = before_poss + new_poss
    return final_string

def is_pass_intercepted(final_string): 
    B1, B2, R, poss = get_broken_down_states(final_string)
    if ((B1 -1) % 4 == (B2-1) % 4) and ((B1 -1) % 4 == (R-1) % 4) and \
          ((B2 -1) % 4 == (R-1) % 4): 
        if (R > max(B1, B2)) or (R < min(B1, B2)): 
            return False
        else: 
            return True
    elif (int((B1 - 1) / 4) == int((B2 -1) / 4)) and \
        (int((B1 -1) / 4) == int((R - 1)/ 4)) and \
        (int((B2 -1) / 4) == int((R - 1)/ 4)): 
        if (R > max(B1, B2)) or (R < min(B1, B2)): 
            return False
        else: 
            return True
    elif ((int((B1 - 1)/4) + (B1 - 1)%4) == (int((B2 - 1)/4) + (B2 - 1)%4))  and \
    ((int((B1 - 1)/4) + (B1 - 1)%4) == (int((R - 1)/4) + (R - 1)%4)) and \
    ((int((B2 - 1)/4) + (B2 - 1)%4) == (int((R - 1)/4) + (R - 1)%4)):
        if (R > max(B1, B2)) or (R < min(B1, B2)): 
            return False
        else: 
            return True
    elif ((int((B1 - 1)/4) - (B1 - 1)%4) == (int((B2 - 1)/4) - (B2 - 1)%4))  and \
    ((int((B1 - 1)/4) - (B1 - 1)%4) == (int((R - 1)/4) - (R - 1)%4)) and \
    ((int((B2 - 1)/4) - (B2 - 1)%4) == (int((R - 1)/4) - (R - 1)%4)): 
        if (R > max(B1, B2)) or (R < min(B1, B2)): 
            return False
        else: 
            return True
    else:
        return False

def get_pass_probability(final_string, q):
    B1, B2, R, poss = get_broken_down_states(final_string)
    x1 = int((B1 - 1)%4)
    y1 = int((B1 - 1)/4) 
    x2 = int((B2 - 1)%4)
    y2 = int((B2 - 1)/4)
    pass_p =  q - 0.1*np.maximum(np.abs(x1 - x2), np.abs(y1 - y2)) 
    return pass_p

def shot_to_goal(final_string ,q): 
    B1, B2, R, poss = get_broken_down_states(final_string)
    if poss == 1: 
        if (R == 8) or (R == 12): 
            x1 = int((B1 - 1)%4)
            goal_prob = 0.5*(q - 0.2*(3 - x1))
            return goal_prob
        else: 
            x1 = int((B1 - 1)%4)
            goal_prob = q - 0.2*(3 - x1)
            return goal_prob
    elif poss == 2: 
        if (R == 8) or (R == 12): 
            x2 = int((B2 - 1)%4)
            goal_prob = 0.5*(q - 0.2*(3 - x2))
            return goal_prob
        else: 
            x2 = int((B2 - 1)%4)
            goal_prob = q - 0.2*(3 - x2)
            return goal_prob

def create_football_mdp(p, q, policy_matrix):

    n_S_mdp = 8194
    n_A_mdp = 10
    print("numStates", n_S_mdp)
    print("numActions", n_A_mdp)
    print("end", n_S_mdp - 2, n_S_mdp - 1)
    for i in range(0, n_S_mdp - 2 ):
        initial_string = state_decoder(i)
        B1, B2, R, poss = get_broken_down_states(initial_string)
        for j in range(0, n_A_mdp):
#B1 moves left
            if j == 0: 
                if (left_operator(initial_string,1) != None):
                    mid_string = left_operator(initial_string, 1)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure 
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal))

#B1 moves right
            elif j == 1: 
                if (right_operator(initial_string,1) != None):
                    mid_string = right_operator(initial_string, 1)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal))         
#B1 moves up
            elif j == 2: 
                if (up_operator(initial_string,1) != None):
                    mid_string = up_operator(initial_string, 1)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
  
#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal))             
#B1 moves down
            elif j == 3: 
                if (down_operator(initial_string,1) != None):
                    mid_string = down_operator(initial_string, 1)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 1:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 2:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal))
#B2 moves left
            elif j == 4: 
                if (left_operator(initial_string,2) != None):
                    mid_string = left_operator(initial_string, 2)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal))               
#B2 moves right
            elif j == 5: 
                if (right_operator(initial_string,2) != None):
                    mid_string = right_operator(initial_string, 2)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal)) 
#B2 moves up
            elif j == 6: 
                if (up_operator(initial_string,2) != None):
                    mid_string = up_operator(initial_string, 2)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal))  
#B2 moves down
            elif j == 7: 
                if (down_operator(initial_string,2) != None):
                    mid_string = down_operator(initial_string, 2)
                    to_terminal = 0
#R moves left 
                    if(left_operator(mid_string,3) != None): 
                        final_string = left_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][0]
                            prob_failure =       2*p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][0]
                            prob_failure =       p*policy_matrix[i][0]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][0] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves right                           
                    if(right_operator(mid_string,3) != None): 
                        final_string = right_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][1]
                            prob_failure =       2*p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
  
                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][1]
                            prob_failure =       p*policy_matrix[i][1]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][1] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves up                           
                    if(up_operator(mid_string,3) != None): 
                        final_string = up_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][2]
                            prob_failure =       2*p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][2]
                            prob_failure =       p*policy_matrix[i][2]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][2] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

#R moves down                          
                    if(down_operator(mid_string,3) != None): 
                        final_string = down_operator(mid_string,3)
                        final_state = state_encoder(final_string)
                        if poss == 2:
                            prob_success = (1 - 2*p)*policy_matrix[i][3]
                            prob_failure =       2*p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))

                        elif poss == 1:
                            prob_success = (1 - p)*policy_matrix[i][3]
                            prob_failure =       p*policy_matrix[i][3]
                            if check_is_tackle(initial_string, j, final_string) == True:
                                prob_success = 0.5*prob_success 
                                prob_failure += prob_success 
                            to_terminal += prob_failure
                            if policy_matrix[i][3] != 0: 
                                print("transition " + str(i) + " " + str(j)\
                                        + " " + str(final_state) + " " + str(0) +\
                                            " " + str(prob_success))
                    print("transition " + str(i) + " " + str(j)\
                            + " " + str(8192) + " " + str(0) +\
                                " " + str(to_terminal))
#Pass 
            elif j == 8:
                to_terminal = 0
#R moves left
                if (left_operator(initial_string, 3) != None): 
                    mid_string = left_operator(initial_string, 3)
                    final_string = change_possession(mid_string)
                    final_state = state_encoder(final_string)
                    p_success0 = get_pass_probability(final_string, q)*policy_matrix[i][0]
                    if is_pass_intercepted(final_string):
                        p_success0 = 0.5*p_success0
                    to_terminal += policy_matrix[i][0] - p_success0
                    if (p_success0 != 0):
                        print("transition " + str(i) + " " + str(j)\
                                + " " + str(final_state) + " " + str(0) +\
                                    " " + str(p_success0))
#R moves right                   
                if (right_operator(initial_string, 3) != None): 
                    mid_string = right_operator(initial_string, 3)
                    final_string = change_possession(mid_string)
                    final_state = state_encoder(final_string)
                    p_success1 = get_pass_probability(final_string, q)*policy_matrix[i][1]
                    if is_pass_intercepted(final_string):
                        p_success1 = 0.5*p_success1
                    to_terminal += policy_matrix[i][1] - p_success1
                    if (p_success1 != 0):
                        print("transition " + str(i) + " " + str(j)\
                                + " " + str(final_state) + " " + str(0) +\
                                    " " + str(p_success1))
#R moves up                  
                if (up_operator(initial_string, 3) != None): 
                    mid_string = up_operator(initial_string, 3)
                    final_string = change_possession(mid_string)
                    final_state = state_encoder(final_string)
                    p_success2 = get_pass_probability(final_string, q)*policy_matrix[i][2]
                    if is_pass_intercepted(final_string):
                        p_success2 = 0.5*p_success2
                    to_terminal += policy_matrix[i][2] - p_success2
                    if (p_success2 != 0): 
                        print("transition " + str(i) + " " + str(j)\
                                + " " + str(final_state) + " " + str(0) +\
                                    " " + str(p_success2))
#R moves down                 
                if (down_operator(initial_string, 3) != None): 
                    mid_string = down_operator(initial_string, 3)
                    final_string = change_possession(mid_string)
                    final_state = state_encoder(final_string)
                    p_success3 = get_pass_probability(final_string, q)*policy_matrix[i][3]
                    if is_pass_intercepted(final_string):
                        p_success3 = 0.5*p_success3
                    to_terminal += policy_matrix[i][3] - p_success3
                    if (p_success3 != 0):
                        print("transition " + str(i) + " " + str(j)\
                                + " " + str(final_state) + " " + str(0) +\
                                    " " + str(p_success3))
                print("transition " + str(i) + " " + str(j)\
                        + " " + str(8192) + " " + str(0) +\
                            " " + str(to_terminal))
                
#Shoot (using the MDP with T = 1 and R = Expected Value) 
            elif j == 9: 
                goal_prob = 0
                if (left_operator(initial_string, 3) != None):
                    final_string = left_operator(initial_string, 3)
                    goal_prob += shot_to_goal(final_string, q)*policy_matrix[i][0]
                if (right_operator(initial_string, 3) != None):
                    final_string = right_operator(initial_string, 3)
                    goal_prob += shot_to_goal(final_string, q)*policy_matrix[i][1]
                if (up_operator(initial_string, 3) != None):
                    final_string = up_operator(initial_string, 3)
                    goal_prob += shot_to_goal(final_string, q)*policy_matrix[i][2]
                if (down_operator(initial_string, 3) != None):
                    final_string = down_operator(initial_string, 3)
                    goal_prob += shot_to_goal(final_string, q)*policy_matrix[i][3]
                no_goal_prob = 1 - goal_prob
                print("transition " + str(i) + " " + str(j)\
                        + " " + str(8192) + " " + str(0) +\
                            " " + str(no_goal_prob))
                print("transition " + str(i) + " " + str(j)\
                        + " " + str(8193) + " " + str(1) +\
                            " " + str(goal_prob))
    print("mdptype","episodic")
    print("discount", 1)



if __name__ == "__main__": 
    opponent_file_path, p, q = get_arguments()
    policy_matrix = create_policy_matrix(opponent_file_path)
    create_football_mdp(p, q, policy_matrix)
    # print(state_encoder('0306062'))
    # print(state_decoder(681))
    # print(state_decoder(685))
    # print(state_decoder(675))
    # print(state_decoder(691))
    # print(state_decoder(1705))
    # print(state_decoder(1709))
    # print(state_decoder(1699))
    # print(state_decoder(1715))
    # print(state_decoder(3241))
    # print(state_decoder(3245))
    # print(state_decoder(3235))
    # print(state_decoder(3251))









    
    




    