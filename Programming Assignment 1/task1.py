"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value

# START EDITING HERE
# You can use this space to define any helper functions that you need
def kl_divergence(p,q): 
    e = 10e-10
    kl = p*math.log((p + e)/(q + e)) + (1 - p)*math.log((1 + e - p)/(1 + e - q))
    return kl

def binary_search(rhs, p, t):
    #Ideal conditions: 
    #   Upper Cutoff = 0.5*np.log(t) 
    #   Lower Cutoff = 0.1
    #   Epsilon = 0.1 if rhs > 1 else 0.05
    delta = 1/16
    upper_cutoff = 0.6*math.log(t) #Upper value of KL (Toggle)
    lower_cutoff = 0.1 #Lower value of KL (Toggle)
    epsilon = 1 #if rhs > 1 else 0.5 #Bisection Method Tolerance (Toggle)
    if rhs > upper_cutoff: 
        #print("RHS: ", round(rhs,3), "greater than UC: ", round(upper_cutoff, 3),"max poss kld: ", round(kl_divergence(p,1), 3) )
        return 1
    elif rhs < lower_cutoff: 
        #print("RHS lower than LC:", round(rhs,3),".Returning p: ", round(p,3))
        return p 
    elif p == 1: 
        return 1
    else: 
        l = p
        r = 1
        m = 0.5*(l + r)
        while np.abs(kl_divergence(p,m) - rhs) >= epsilon and np.maximum(np.abs(m - l), np.abs(m -r)) > delta:  
            m = 0.5*(l + r)
            #print("p:", round(p,3), "Left: ", round(kl_divergence(p,l),3), "Middle: ", round(kl_divergence(p, m),3), "Right: ", round(kl_divergence(p,r), 3), "RHS: ", round(rhs,3), "BS_iter: ", counting)
            if (kl_divergence(p,l) - rhs)*(kl_divergence(p,m) - rhs) < 0:
                r = m
            else: 
                l = m
        #print("RHS: ", round(rhs,3), "p:", round(p,3), "Returning m: ", round(m,3), "KLD: ", round(kl_divergence(p,m),3))
        return m 

def kl_plotter(): 
    for p in np.arange(0, 1, 0.01): 
        for q in np.arange(0, 1, 0.01): 
            print("KLD of p = ", round(p,3), "and q = ", round(q,3), "equals: ", round(kl_divergence(p,q),3))



def compute_kl_ucb(p, t, u, c, arm): 
    if u == 0:
        print
        return 1
    elif u > 0 and t == 1: 
        return 1 
    else:
        rhs = (np.log(t) + c*np.log(np.log(t)))/(u)
        return binary_search(rhs, p, t)


# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # START EDITING HERE
        self.counts = np.zeros(num_arms) #u_a^t in the algorithm 
        self.emp_means = np.zeros(num_arms) #\hat{p}_a^t in the algotithm
        self.infinity = 10e10
        self.ucbs = self.infinity * np.ones(num_arms) #ucb_a^t in the algorithm 
        self.total_count = 0
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        return np.argmax(self.ucbs)
        # END EDITING HERE  
        
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        #print("Total_count", self.total_count)
        self.total_count += 1 
        self.counts[arm_index] += 1
        #print(self.counts)
        for arms in range(self.num_arms):
            if arms == arm_index:
                u = self.counts[arm_index]
                new_p = ((u - 1)/u)*self.emp_means[arm_index] + (1/u)*reward
                self.emp_means[arm_index] = new_p
                self.ucbs[arm_index] = self.emp_means[arm_index] + np.sqrt((2*np.log(self.total_count))/(u))
            else: 
                if self.counts[arms] != 0:
                    self.ucbs[arms] = self.emp_means[arms] + np.sqrt((2*np.log(self.total_count))/(self.counts[arms]))
                    

        #raise NotImplementedError
        # END EDITING HERE


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.totalcount = 0 #t in the algorithm
        self.counts = np.zeros(num_arms)
        self.p_hats = np.zeros(num_arms)
        self.kl_ucbs = np.ones(num_arms)
        self.c = 0
        #kl_plotter()#Remove this
        # END EDITING HERE*
    
    def give_pull(self):
        # START EDITING HERE
        return np.argmax(self.kl_ucbs)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        #print("Totalcount", self.totalcount)
        self.totalcount += 1 
        self.counts[arm_index] += 1
        self.p_hats[arm_index] = ((self.counts[arm_index] - 1)/(self.counts[arm_index]))*self.p_hats[arm_index] + (1/(self.counts[arm_index]))*reward
        for arms in range(self.num_arms): 
            self.kl_ucbs[arms] = compute_kl_ucb(self.p_hats[arms], self.totalcount, self.counts[arms], self.c, arms)
        # END EDITING HERE

class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.totalcount = 0 
        self.successes = np.zeros(num_arms)
        self.failures = np.zeros(num_arms)
        self.sample_x = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        for arms in range(self.num_arms): 
            self.sample_x[arms] = np.random.beta(self.successes[arms] + 1, self.failures[arms] + 1)
        return np.argmax(self.sample_x)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward == 1: 
            self.successes[arm_index] += 1
        if reward == 0: 
            self.failures[arm_index] += 1 
        # END EDITING HERE
