from action import Action
import numpy as np
import random

class Policy:
    def __init__(self, agent, states, actions, seed=None):
        """
        Constructor for SARSA/Q-Learning policy.
        This is a base class which will be specialized for the different epsilon-greedy policies

        Arguments:
        agent - 'M' for the male agent, 'F' for the female agent
        states - The RL state space being used
        actions - A list of actions that are available

        Properties:
        pi - The function executed to choose an action, given the current state and a Q table, intended to be overridden
        rng - A random number generator used for stochastic policies, which can be initialized with a prescribed seed
        """
        self.agent = agent
        self.states = states
        self.actions = actions
        # placeholder
        self.pi = None
        self.seed = seed
        self.rng = np.random.default_rng(seed=seed)

    def execute(self, state, rlstate, table):
        """
        Execute the policy for one step, given current real world and RL states, and the Q table
        """
        return self.pi(state, rlstate, table)
    
    def is_applicable(self, state, action):
        """
        Returns True if the given action is applicable given the current state
        """
        a = Action()
        if action == 'Pickup':
            return a.is_pickup_applicable(self.agent, state)
        elif action == 'Dropoff':
            return a.is_dropoff_applicable(self.agent, state)
        elif action == 'N':
            return a.is_north_applicable(self.agent, state)
        elif action == 'S':
            return a.is_south_applicable(self.agent, state)
        elif action == 'E':
            return a.is_east_applicable(self.agent, state)
        elif action == 'W':
            return a.is_west_applicable(self.agent, state)
        elif action == 'U':
            return a.is_up_applicable(self.agent, state)
        elif action == 'D':
            return a.is_down_applicable(self.agent, state)

    def get_applicable_actions(self, state):
        """
        Returns an list of actions applicable in the given state
        """
        return list(filter(lambda action: self.is_applicable(state, action), self.actions))

class PRandom(Policy):
    """
    The PRANDOM policy: at any point, choose uniform random action from available actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pi = lambda s, rs, qs: self.random(s)

    def random(self, state):
        valid_actions = self.get_applicable_actions(state)
        if 'Pickup' in valid_actions:
            return 'Pickup'
        elif 'Dropoff' in valid_actions:
            return 'Dropoff'
        else:
            return self.rng.choice(valid_actions)
        
class PGreedy(Policy):
    """
    The PGREEDY policy: always choose the available action leading to the highest possible Q value from the given state
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pi = lambda s, rs, qs: self.greedy(s, rs, qs)

    def greedy(self, state, rlstate, table):
        valid_actions = self.get_applicable_actions(state)
        if 'Pickup' in valid_actions:
            return 'Pickup'
        elif 'Dropoff' in valid_actions:
            return 'Dropoff'
        else:
            # avoid blockage problem
            self.rng.shuffle(valid_actions)
            
            best_q = -2**32
            best_a = None
            for action in valid_actions:
                this_q = table[action][rlstate]
                if this_q > best_q:
                    best_q = this_q
                    best_a = action
            return best_a

class PExploit(PRandom, PGreedy):
    """
    The PEXPLOIT policy: randomly perform PGREEDY 80% of the time, and PRANDOM 20% of the time.
    """
    def __init__(self, *args, **kwargs):
        super(PRandom, self).__init__(*args, **kwargs)
        self.pi = lambda s, rs, qs: self.exploit(s, rs, qs)

    def exploit(self, state, rlstate, table):
        if self.rng.random() >= 0.85:
            return self.random(state)
        else:
            return self.greedy(state, rlstate, table)