"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the MultiBanditsAlgo class. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, set_pulled, reward): This method is called 
        just after the give_pull method. The method should update the 
        algorithm's internal state based on the arm that was pulled and the 
        reward that was received.
        (The value of arm_index is the same as the one returned by give_pull 
        but set_pulled is the set that is randomly chosen when the pull is 
        requested from the bandit instance.)
"""

import numpy as np

# START EDITING HERE
# You can use this space to define any helper functions that you need
def kl_divergence(p,q): 
    e = 10e-10
    kl = p*np.log((p + e)/(q + e)) + (1 - p)*np.log((1 + e - p)/(1 + e - q))
    return kl

def binary_search(rhs, p, t):
    upper_cutoff = 0.6*np.log(t) #Upper value of KL (Toggle)
    lower_cutoff = 0.1 #Lower value of KL (Toggle)
    epsilon = 1  #Bisection Method Tolerance (Toggle)
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
        #while np.abs(kl_divergence(p,m) - rhs) >= epsilon and np.maximum(np.abs(m - l), np.abs(m -r)) > 0.005:  
        while np.abs(kl_divergence(p,m) - rhs) >= epsilon or np.maximum(np.abs(kl_divergence(p,l) - kl_divergence(p,m)), np.abs(kl_divergence(p,r) - kl_divergence(p,m))) >= 0.5: 
            m = 0.5*(l + r)
            #print("p:", round(p,3), "Left KLD: ", round(kl_divergence(p,l),3), "Middle KLD: ", round(kl_divergence(p, m),3), "RHS: ", round(rhs,3))
            if (kl_divergence(p,l) - rhs)*(kl_divergence(p,m) - rhs) < 0:
                r = m
            else: 
                l = m 
        #print("RHS: ", round(rhs,3), "p:", round(p,3), "Returning m: ", round(m,3), "KLD: ", round(kl_divergence(p,m),3))
        return m 

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


class MultiBanditsAlgo:
    def __init__(self, num_arms, horizon):
        # You can add any other variables you need here
        self.num_arms = num_arms
        self.horizon = horizon
        # START EDITING HERE

        #KL-UCB Implementation
        self.total = 0
        self.total_1 = 0
        self.total_2 = 0 #t in the algorithm
        self.p_counts = np.zeros(num_arms)
        self.p_hats = np.zeros(num_arms)
        self.p_kl_ucbs = np.ones(num_arms)
        self.q_counts = np.zeros(num_arms)
        self.q_hats = np.zeros(num_arms)
        self.q_kl_ucbs = np.ones(num_arms)
        self.mean_kl_ucbs = np.ones(num_arms)
        self.counts = np.zeros(num_arms)
        self.hats = np.zeros(num_arms)
        self.kl_ucbs = np.ones(num_arms)
        self.c = 0
        
    
    def give_pull(self):
        # START EDITING HERE
        
        #KL-UCB Implementation
        return np.argmax(self.mean_kl_ucbs)
    

    
    def get_reward(self, arm_index, set_pulled, reward):
        # START EDITING HERE

        #Algorithm 1 (KL-UCB harmonic)
        if set_pulled == 0: 
            self.total_1 += 1 
            self.p_counts[arm_index] += 1
            self.p_hats[arm_index] = ((self.p_counts[arm_index] - 1)/(self.p_counts[arm_index]))*self.p_hats[arm_index] + (1/(self.p_counts[arm_index]))*reward
            for arms in range(self.num_arms): 
                self.p_kl_ucbs[arms] = compute_kl_ucb(self.p_hats[arms], self.total_1, self.p_counts[arms], self.c, arms)
        if set_pulled == 1: 
            self.total_2 += 1 
            self.q_counts[arm_index] += 1
            self.q_hats[arm_index] = ((self.q_counts[arm_index] - 1)/(self.q_counts[arm_index]))*self.q_hats[arm_index] + (1/(self.q_counts[arm_index]))*reward
            for arms in range(self.num_arms): 
                self.q_kl_ucbs[arms] = compute_kl_ucb(self.q_hats[arms], self.total_2, self.q_counts[arms], self.c, arms)
        for arms in range(self.num_arms): 
            self.mean_kl_ucbs[arms] = self.p_kl_ucbs[arms]*self.q_kl_ucbs[arms]/(self.p_kl_ucbs[arms] + self.q_kl_ucbs[arms])
        
        #Algorithm 2 (KL-UCB Naive)
        # self.total += 1
        # self.counts[arm_index] += 1
        # self.hats[arm_index] = ((self.counts[arm_index] - 1)/(self.counts[arm_index]))*self.hats[arm_index] + (1/(self.counts[arm_index]))*reward
        # for arms in range(self.num_arms): 
        #     self.kl_ucbs[arms] = compute_kl_ucb(self.hats[arms], self.total, self.counts[arms], self.c, arms)
        


        # END EDITING HERE



