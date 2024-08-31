"""
You need to write code to plot the graphs as required in task2 of the problem statement:
    - You can edit any code in this file but be careful when modifying the simulation specific code. 
    - The simulation framework as well as the BernoulliBandit implementation for this task have been separated from the rest of the assignment code and is contained solely in this file. This will be useful in case you would like to collect more information from runs rather than just regret.
"""

import numpy as np
from multiprocessing import Pool
from task1 import Eps_Greedy, UCB, KL_UCB
import matplotlib.pyplot as plt
# START EDITING HERE


# You can use this space to define any helper functions that you need.
def easy_plot(list_x, list_y, algostring, ab):
  plt.figure(figsize= (12,12))
  plt.plot(list_x, list_y)
  if ab == 'a':  
    plt.xlabel("Varying p2 from 0 to 0.9 keeping p1 = 0.9")
  if ab == 'b':
    plt.xlabel("Varying p2 from 0 to 0.9 keeping delta = 0.1")
  plt.ylabel("Expected Regret for algorithm " + algostring)
  plt.show()

# END EDITING HERE

class BernoulliArmTask2:
  def __init__(self, p):
    self.p = p

  def pull(self, num_pulls=None):
    return np.random.binomial(1, self.p, num_pulls)

class BernoulliBanditTask2:
  def __init__(self, probs=[0.3, 0.5, 0.7],):
    self.__arms = [BernoulliArmTask2(p) for p in probs]
    self.__max_p = max(probs)
    self.__regret = 0

  def pull(self, index):
    reward = self.__arms[index].pull()
    self.__regret += self.__max_p - reward
    return reward

  def regret(self):
    return self.__regret
  
  def num_arms(self):
    return len(self.__arms)


def single_sim_task2(seed=0, ALGO=Eps_Greedy, PROBS=[0.3, 0.5, 0.7], HORIZON=1000):
  np.random.seed(seed)
  np.random.shuffle(PROBS)
  bandit = BernoulliBanditTask2(probs=PROBS)
  algo_inst = ALGO(num_arms=len(PROBS), horizon=HORIZON)
  for t in range(HORIZON):
    arm_to_be_pulled = algo_inst.give_pull()
    reward = bandit.pull(arm_to_be_pulled)
    algo_inst.get_reward(arm_index=arm_to_be_pulled, reward=reward)
  return bandit.regret()

def simulate_task2(algorithm, probs, horizon, num_sims=50):
  """simulates algorithm of class Algorithm
  for BernoulliBandit bandit, with horizon=horizon
  """
  
  def multiple_sims(num_sims=50):
    with Pool(10) as pool:
      sim_out = pool.starmap(single_sim_task2,
        [(i, algorithm, probs, horizon) for i in range(num_sims)])
    return sim_out 

  sim_out = multiple_sims(num_sims)
  regrets = np.mean(sim_out)

  return regrets

def task2(algorithm, horizon, p1s, p2s, num_sims=50):
    """generates the data for task2
    """
    probs = [[p1s[i], p2s[i]] for i in range(len(p1s))]

    regrets = []
    for prob in probs:
        regrets.append(simulate_task2(algorithm, prob, horizon, num_sims))

    return regrets

if __name__ == '__main__':
  # EXAMPLE CODE

  #Task 2A
  store_x_a = []
  store_regrets_a =[]
  p1a = []
  p2a = []
  for i in np.arange(0, 0.95, 0.05):
    p1a.append(0.9)
    p2a.append(i)
    store_x_a.append(i)
  regrets_a = task2(UCB, 30000, p1a, p2a, 50)
  print(regrets_a)
  
  #Task 2B
  store_x_b= []
  store_regrets_b =[]
  p1b = []
  p2b = []
  for i in np.arange(0, 0.95, 0.05):
    p1b.append(i + 0.1)
    p2b.append(i)
    store_x_b.append(i)
  regrets_b = task2(UCB, 30000, p1b, p2b, 50)
  print(regrets_b)


  store_x_bkl= []
  store_regrets_bkl =[]
  p1bkl = []
  p2bkl = []
  for i in np.arange(0, 0.95, 0.05):
    p1bkl.append(i + 0.1)
    p2bkl.append(i)
    store_x_bkl.append(i)
  regrets_bkl = task2(KL_UCB, 30000, p1bkl, p2bkl, 50)
  print(regrets_bkl)

  # INSERT YOUR CODE FOR PLOTTING HERE
  easy_plot(store_x_a, regrets_a, "UCB", 'a')
  easy_plot(store_x_b, regrets_b, "UCB", 'b')
  easy_plot(store_x_bkl, regrets_bkl, "KL_UCB", 'b')
  
  
  pass