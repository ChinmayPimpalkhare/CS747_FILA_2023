"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the FaultyBanditsAlgo class. Here are the method details:
    - __init__(self, num_arms, horizon, fault): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)
"""

import numpy as np

# START EDITING HERE
# You can use this space to define any helper functions that you need
def kl_divergence(p,q): 
    e = 10e-10
    kl = p*np.log((p + e)/(q + e)) + (1 - p)*np.log((1 + e - p)/(1 + e - q))
    return kl

def binary_search(rhs, p, t):
    #Ideal conditions: 
    #   Upper Cutoff = 0.5*np.log(t) 
    #   Lower Cutoff = 0.1
    #   Epsilon = 0.1 if rhs > 1 else 0.05
    delta = 1/16
    upper_cutoff = 0.6*np.log(t) #Upper value of KL (Toggle)
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
        counting = 0
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

class FaultyBanditsAlgo:
    def __init__(self, num_arms, horizon, fault):
        # You can add any other variables you need here
        self.num_arms = num_arms
        self.horizon = horizon
        self.fault = fault # probability that the bandit returns a faulty pull
        # START EDITING HERE


        #KL-UCB Implementation 
        self.totalcount = 0 #t in the algorithm
        self.counts = np.zeros(num_arms)
        self.p_hats = np.zeros(num_arms)
        self.kl_ucbs = np.ones(num_arms)
        self.c = 0
        self.adjusted_p = np.zeros(num_arms)


        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        #Implementation of KL-UCB 
        return np.argmax(self.kl_ucbs)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE


        # #KL-UCB Implementation (Approach 1)
        # #print("Total_count", self.total_count)
        # self.totalcount += 1 
        # self.counts[arm_index] += 1
        # self.p_hats[arm_index] = ((self.counts[arm_index] - 1)/(self.counts[arm_index]))*self.p_hats[arm_index] + (1/(self.counts[arm_index]))*reward
        # #self.adjusted_p[arm_index] = (1 - self.fault)*self.p_hats[arm_index] + 0.5*self.fault
        # for arms in range(self.num_arms): 
        #     self.kl_ucbs[arms] = compute_kl_ucb(self.p_hats[arms], self.totalcount, self.counts[arms], self.c, arms)


        # #KL-UCB Implementation (Approach 2)
        # #print("Total_count", self.total_count)
        self.totalcount += 1 
        self.counts[arm_index] += 1
        self.p_hats[arm_index] = ((self.counts[arm_index] - 1)/(self.counts[arm_index]))*self.p_hats[arm_index] + (1/(self.counts[arm_index]))*reward
        self.adjusted_p[arm_index] = np.maximum((self.p_hats[arm_index] - 0.5*self.fault)/(1 - self.fault), 0)
        for arms in range(self.num_arms): 
            self.kl_ucbs[arms] = compute_kl_ucb(self.adjusted_p[arms], self.totalcount, self.counts[arms], self.c, arms)


        #END EDITING HERE

