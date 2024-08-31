import numpy as np 
import math 
import argparse
from pathlib import Path

def get_arguments():
    parser = argparse.ArgumentParser(description="Decoder")

    #Add the arguments to the parser 
    parser.add_argument('--opponent', metavar='--opponent', type=Path, \
                        help='Stores the location of the opponent policy')
    parser.add_argument('--value-policy', metavar='--value-policy', type = Path, \
                        help = 'Stored the location of value and policy')
    #Perform parsing of the arguments 
    args = parser.parse_args()

    #Store the parsed arguments into local variables
    return args.opponent, args.value_policy

def decode(opponent, value_policy):
    read_vp = open(value_policy, 'r')
    read_opponent = open(opponent, 'r')
    lines_policy = read_vp.readlines()
    lines_opponent = read_opponent.readlines()
    num_states = 8192
    for i in range(0, num_states): 
        print(lines_opponent[i+1].split(' ')[0], lines_policy[i].split(" ")[1][:-1],lines_policy[i].split(" ")[0])



if __name__ == '__main__': 
    opponent, value_policy = get_arguments()
    decode(opponent, value_policy)
