import argparse
import numpy as np 
import math 
import sys
import os 
from pathlib import Path
from pulp import *

def read_mdp_file(mdp_file_path): 
    file = open(mdp_file_path, 'r') #Read the file
    lines_of_file = file.readlines() 
    number_of_lines = len(lines_of_file)

    num_states = int(lines_of_file[0].split(' ')[1][:-1])           #|S|
    num_actions = int(lines_of_file[1].split(' ')[1][:-1])          #|A|
    mdp_type = lines_of_file[-2].split(' ')[1][:-1]                 #Type
    gamma = float(lines_of_file[-1].split(' ')[-1][:-1])            #Discount Factor
    is_mdp_episodic = 0                                             #MDP Flag = 0
    if mdp_type == 'episodic':                                      #Flag for episodic MDPs
        is_mdp_episodic = 1
    
    these_are_episodic = np.zeros(num_states) 
    
    if is_mdp_episodic:                                             #Set terminal states
        for each in lines_of_file[2][:-1].split(' ')[1:]:
            these_are_episodic[int(each)] = 1 
    
    transition_matrix = np.zeros((num_states, num_actions, num_states)) #SxAxS
    reward_matrix = np.zeros((num_states, num_actions, num_states))     #SxAxS

    for i in range (3, number_of_lines - 2):                            #T and R
        split_line = lines_of_file[i][:-1].split(' ')
        state_1 = int(split_line[1])
        action  = int(split_line[2])
        state_2 = int(split_line[3])
        reward  = float(split_line[4])
        prob    = float(split_line[5])
        transition_matrix[state_1][action][state_2] = prob
        reward_matrix[state_1][action][state_2]     = reward
    

    #Returning the following
    #1. Number of states 
    #2. Number of actions
    #3. Type of the MDP
    #4. Flag for whether the MDP is episodic
    #5. Terminal States 
    #6. Transition Matrix
    #7. Reward Matrix
    #8. Gamma
    return num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, gamma

def Bellman_optimality_operation(num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, \
    gamma, value_function
    ):
    #Steps: For all states, max over actions (sum of (T*(R + gamma*V)))
    new_value_function = np.zeros(num_states)
    optimal_action = np.zeros(num_states)

    for i in range(num_states):
        if these_are_episodic[i] == 0:
            new_value_function[i] = np.max(np.sum(np.multiply(transition_matrix[i], \
                                                    reward_matrix[i] +\
                                                        gamma*value_function), axis = 1))
            optimal_action[i] = np.argmax(np.sum(np.multiply(transition_matrix[i], \
                                                    reward_matrix[i] +\
                                                        gamma*value_function), axis = 1))

    return new_value_function, optimal_action

def value_iteration(num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, \
    gamma):
    epsilon = 1e-12
    V_old = np.zeros(num_states)
    V_new, pi = Bellman_optimality_operation(num_states, num_actions, mdp_type, is_mdp_episodic, \
        these_are_episodic, transition_matrix, reward_matrix, \
        gamma, V_old)
    V_copy = V_old
    while np.linalg.norm(V_new - V_copy, 1) >= epsilon:
        V_copy = V_old 
        V_new, pi = Bellman_optimality_operation(num_states, num_actions, mdp_type, is_mdp_episodic, \
        these_are_episodic, transition_matrix, reward_matrix, \
        gamma, V_old)
        V_old = V_new
    for i in range(num_states): 
        print(V_new[i],int(pi[i]))

def linear_programming(num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, \
    gamma): 
    prob = LpProblem("Linear_Programming_Value", LpMaximize)
    set_S = range(0, num_states)
    set_A = range(0, num_actions)
    val_func = LpVariable.dicts("Value_Function", set_S, cat='Continuous')

    #objective function for the primal
    prob += lpSum([-val_func[i] for i in set_S])

    #nk constraints
    for i in set_S:
        for j in set_A:
            prob += val_func[i] >= lpSum([transition_matrix[i][j][k]*\
                                (reward_matrix[i][j][k] + \
                                gamma*val_func[k]) for k in set_S])
            

    #solve
    prob.solve(PULP_CBC_CMD(msg=0))
    V_star = np.array([val_func[i].varValue for i in set_S])
    Q_values = np.zeros((num_states, num_actions))
    for i in set_S:
        for j in set_A: 
            Q_values[i][j] = np.sum(np.multiply(transition_matrix[i][j], \
                                                reward_matrix[i][j] + \
                                                    gamma*V_star))
    pi_star = np.argmax(Q_values, axis = 1)
    for i in set_S:
        print(V_star[i], int(pi_star[i]))
    
def compute_action_values(num_states, num_actions, mdp_type, is_mdp_episodic, \
            these_are_episodic, transition_matrix, reward_matrix, \
            gamma, value_function):
    Q_values = np.zeros((num_states, num_actions))
    for i in range(0,num_states):
        for j in range(0,num_actions): 
            Q_values[i][j] = np.sum(np.multiply(transition_matrix[i][j], \
                                                reward_matrix[i][j] + \
                                                gamma*value_function))
    return Q_values

def howard_policy_iteration(num_states, num_actions, mdp_type, is_mdp_episodic, \
            these_are_episodic, transition_matrix, reward_matrix, \
            gamma): 
    
    #initialize arrays for improvable states and improvable actions
    #corresponding to the improvable states
    improvable_states = np.ones(num_states)
    improving_actions = np.zeros((num_states, num_actions))
    pi_old = np.random.randint(num_actions, size = num_states)
    while(np.sum(improvable_states) > 0):
        V_old = policy_evaluation_no_print(num_states, num_actions, mdp_type, is_mdp_episodic, \
                these_are_episodic, transition_matrix, reward_matrix, \
                gamma, pi_old) 
        Q_pi = compute_action_values(num_states, num_actions, mdp_type, is_mdp_episodic, \
                these_are_episodic, transition_matrix, reward_matrix, \
                gamma, V_old)
        improvable_states.fill(0)
        improving_actions.fill(0)
        for i in range(0,num_states):
            for j in range(0,num_actions): 
                if Q_pi[i][j] > V_old[i] and j != pi_old[i] : 
                    improvable_states[i] = 1
                    improving_actions[i][j] = 1
        for i in range(0,num_states): 
            if improvable_states[i] == 1:
                pi_old[i] = int(np.random.choice(num_actions,\
                    1, p = improving_actions[i]/np.sum(improving_actions[i])))
      
    for i in range(0, num_states): 
        print(V_old[i],int(pi_old[i]))
    
def read_policy(policy_path):
    pol_file = open(policy_path, 'r')
    lines_of_pol_file = pol_file.readlines()
    policy = np.zeros(len(lines_of_pol_file))
    count = 0
    for each in lines_of_pol_file: 
        policy[count] = int(each[:-1])
        count += 1 
    return policy

# A modification of policy evaluation which only returns the value functions
def policy_evaluation_no_print(num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, \
    gamma, policy): 
    #We shall be using pulp 
    #We can define a dummy objective function 
    #We have the following 2 constraints for each state: 
    #   V(s) >= \sum_s' T*(R + V(s'))
    #   V(s) <= \sum_s' T*(R + V(s'))
    prob = LpProblem("Policy_Evaluation")
    set_S = range(0, num_states)
    val_func = LpVariable.dicts("Value_Function", set_S, cat='Continuous')
    for i in set_S:
        prob += val_func[i] == lpSum([ transition_matrix[i][int(policy[i])][j]*\
                                      (reward_matrix[i][int(policy[i])][j] + \
                                       gamma*val_func[j]) for j in set_S])
    prob.solve(PULP_CBC_CMD(msg=0))
    V_pi = np.array([val_func[i].varValue for i in set_S])
    return V_pi

def policy_evaluation(num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, \
    gamma, policy): 
    #We shall be using pulp 
    #We can define a dummy objective function 
    #We have the following 2 constraints for each state: 
    #   V(s) >= \sum_s' T*(R + V(s'))
    #   V(s) <= \sum_s' T*(R + V(s'))
    prob = LpProblem("Policy_Evaluation")
    set_S = range(0, num_states)
    val_func = LpVariable.dicts("Value_Function", set_S, cat='Continuous')
    for i in set_S:
        prob += val_func[i] == lpSum([ transition_matrix[i][int(policy[i])][j]*\
                                      (reward_matrix[i][int(policy[i])][j] + \
                                       gamma*val_func[j]) for j in set_S])
    prob.solve(PULP_CBC_CMD(msg=0))
    V_pi = np.array([val_func[i].varValue for i in set_S])
    for i in set_S:
        print(V_pi[i]," ",policy[i])

#Define the parser using the argparse module
def get_arguments():
    global mdp_file_path_, algorithm_
    parser = argparse.ArgumentParser(description="Just a parser")

    #Add the arguments to the parser 
    parser.add_argument('--mdp', metavar='--mdp', type=Path, \
                        help='Returns the path of the mdp')
    parser.add_argument('--algorithm', metavar='--algorithm', type = str, \
                        default='vi', help='Implements the algorithm')
    parser.add_argument('--policy', metavar='policy', type = Path, \
                        help = 'Policy which needs to be evaluated')
    #Perform parsing of the arguments 
    args = parser.parse_args()

    #Store the parsed arguments into local variables
    return args.mdp, args.algorithm, args.policy

if __name__ == '__main__':
    #Get the command line arguments 
    mdp_file_path, algorithm, policy_path = get_arguments()

    #Obtain all the MDP variables
    num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, \
    gamma =  read_mdp_file(mdp_file_path)

    if policy_path == None: 
        if algorithm == 'vi':
            value_iteration(num_states, num_actions, mdp_type, is_mdp_episodic, \
            these_are_episodic, transition_matrix, reward_matrix, \
            gamma)

        elif algorithm == 'lp': 
            linear_programming(num_states, num_actions, mdp_type, is_mdp_episodic, \
            these_are_episodic, transition_matrix, reward_matrix, \
            gamma)

        elif algorithm == 'hpi': 
            howard_policy_iteration(num_states, num_actions, mdp_type, is_mdp_episodic, \
            these_are_episodic, transition_matrix, reward_matrix, \
            gamma)

    
    else: 
        policy = read_policy(policy_path)
        policy_evaluation( num_states, num_actions, mdp_type, is_mdp_episodic, \
    these_are_episodic, transition_matrix, reward_matrix, \
    gamma, policy)
