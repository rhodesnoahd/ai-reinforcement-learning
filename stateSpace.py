from cell import Cell
from action import Action
import numpy as np

class StateSpace:
    def __init__(self, experiment):
        """
        Constructor for RW state space.

        Argument:
        experiment - 'original' or 'modified'
        original corresponds to experiments 1, 2, 3, & part of 4
        modified corresponds to part of experiment 4 after 3rd terminal state is reached

        Properties:
        state_space - a 3D NumPy array of Cells
        locF - (x,y,z) coordinates of female agent
        locM - (x,y,z) coordinates of male agent
        carF - True if female agent is carrying a block and False otherwise
        carM - True if male agent is carrying a block and False otherwise
        locDrop - list of (x,y,z) coordinates of each Dropoff cell
        locPick - list of (x,y,z) coordinates of each Pickup cell
        """
        self.state_space = np.empty(shape=(
            3, 3, 3), dtype=object, order='C')   # 'C' means row-major order in memory
        self.locF = None
        self.locM = None
        self.carF = False
        self.carM = False
        self.locDrop = []
        self.locPick = []

        # initializing state_space as all normal cells
        for x in range(self.state_space.shape[0]):
            for y in range(self.state_space.shape[1]):
                for z in range(self.state_space.shape[2]):
                    self.state_space[x, y, z] = Cell()

        # female agent
        self.state_space[0, 0, 0].add_agent('F')
        self.locF = [0, 0, 0]

        # male agent
        self.state_space[2, 1, 2].add_agent('M')
        self.locM = [2, 1, 2]

        # pickup cells
        if experiment == 'original':
            self.state_space[1, 1, 0].set_type('Pickup')
            self.locPick.append([1, 1, 0])
            self.state_space[2, 2, 1].set_type('Pickup')
            self.locPick.append([2, 2, 1])
        elif experiment == 'modified':
            self.state_space[0, 2, 0].set_type('Pickup')
            self.locPick.append([0, 2, 0])
            self.state_space[1, 2, 2].set_type('Pickup')
            self.locPick.append([1, 2, 2])
            
        # dropoff cells
        self.state_space[0, 0, 1].set_type('Dropoff')
        self.locDrop.append([0, 0, 1])
        self.state_space[0, 0, 2].set_type('Dropoff')
        self.locDrop.append([0, 0, 2])
        self.state_space[2, 0, 0].set_type('Dropoff')
        self.locDrop.append([2, 0, 0])
        self.state_space[2, 1, 2].set_type('Dropoff')
        self.locDrop.append([2, 1, 2])

        # risk cells
        self.state_space[1, 1, 1].set_type('Risk')
        self.state_space[2, 1, 0].set_type('Risk')

    def get_location(self, agent):
        """
        returns (x,y,z) coordinates of agent
        argument:
        agent - 'F' for female agent; 'M' for male agent
        """
        if agent == 'F':
            return self.locF
        if agent == 'M':
            return self.locM
        
    def update_agent_loc(self, agent, loc):
        """
        updates the location of agent
        returns nothing
        arguments:
        agent - 'F' for female agent; 'M' for male agent
        loc - (x,y,z) coordinates to assign to agent locaction
        """
        if agent == 'F':
            self.locF = loc
        if agent == 'M':
            self.locM = loc

    def update_agent_carrying(self, agent, bool):
        """
        updates whether agent is carrying block
        returns nothing
        arguments:
        agent - 'F' for female agent; 'M' for male agent
        bool - boolean value to assign to agent carrying attribute
        """
        if agent == 'F':
            self.carF = bool
        if agent == 'M':
            self.carM = bool

    def is_agent_carrying(self, agent):
        """
        returns True if agent is carrying a block and False otherwise
        argument:
        agent - 'F' for female agent; 'M' for male agent
        """
        if agent == 'F':
            return self.carF
        if agent == 'M':
            return self.carM

    def is_pickup(self, loc):
        """
        returns True if cell is Pickup and False otherwise
        argument:
        loc - (x,y,z) coordinates of a cell
        """
        return self.state_space[loc[0], loc[1], loc[2]].get_type() == 'Pickup'

    def is_dropoff(self, loc):
        """
        returns True if cell is Dropoff and False otherwise
        argument:
        loc - (x,y,z) coordinates of a cell
        """
        return self.state_space[loc[0], loc[1], loc[2]].get_type() == 'Dropoff'
    
    def get_state_representation(self):
        """
        returns a list with form:
        [x,y,z,x',y',z',i,i',a,b,c,d,e,f], where
        x,y,z is the location of F
        x',y',z' is the location of M
        i = 1 if F is carrying a block and 0 otherwise
        i' = 1 if M is carrying a block and 0 otherwise
        a,b,c,d are the number of blocks in the dropoff locations
        e,f are the number of blocks in the pickup locations
        """
        if self.carF:
            i = 1
        else:
            i = 0
        if self.carM:
            iPrime = 1
        else:
            iPrime = 0

        state = [self.locF[0], self.locF[1], self.locF[2], 
                 self.locM[0], self.locM[1], self.locM[2],
                 i, iPrime,                         
                 self.state_space[self.locDrop[0][0], self.locDrop[0][1], self.locDrop[0][2]].get_num_blocks(),     
                 self.state_space[self.locDrop[1][0], self.locDrop[1][1], self.locDrop[1][2]].get_num_blocks(),     
                 self.state_space[self.locDrop[2][0], self.locDrop[2][1], self.locDrop[2][2]].get_num_blocks(),     
                 self.state_space[self.locDrop[3][0], self.locDrop[3][1], self.locDrop[3][2]].get_num_blocks(),     
                 self.state_space[self.locPick[0][0], self.locPick[0][1], self.locPick[0][2]].get_num_blocks(), 
                 self.state_space[self.locPick[1][0], self.locPick[1][1], self.locPick[1][2]].get_num_blocks()]
        
        return state
    

    def is_first_dropoff_filled(self):
        """
        returns True if exactly 1 dropoff cell contains 5 blocks and False otherwise
        """
        counter = 0
        for i in range(4):
            counter += max(0, self.state_space[self.locDrop[i][0], self.locDrop[i][1], self.locDrop[i][2]].get_num_blocks() - 4)
        
        return True if counter == 1 else False
        

    def perform_action(self, agent, action):
        """
        performs action by calling appropriate Action method
        returns a reward 
        reward is 14 if action is 'Pickup' or 'Dropoff' or
        reward is -1 if moving from normal cell and -2 if moving from risk cell
        arguments:
        agent - 'F' for female agent; 'M' for male agent
        action - 'Pickup', 'Dropoff', 'E', 'W', 'N', 'S', 'U', or 'D'
        """
        loc = self.get_location(agent)
        reward = self.state_space[loc[0], loc[1], loc[2]].get_cost()

        a = Action()
        if action == 'Pickup':
            a.pickup_block(agent, self)
            reward = 14
        if action == 'Dropoff':
            a.dropoff_block(agent, self)
            reward = 14
        if action == 'E':
            a.move_east(agent, self)
        if action == 'W':
            a.move_west(agent, self)
        if action == 'N':
            a.move_north(agent, self)
        if action == 'S':
            a.move_south(agent, self)
        if action == 'U':
            a.move_up(agent, self)
        if action == 'D':
            a.move_down(agent, self)

        return reward

    def is_complete(self):
        """
        returns True if all Pickup cells contain 5 blocks and False otherwise
        """
        if (self.state_space[self.locDrop[0][0], self.locDrop[0][1], self.locDrop[0][2]].get_num_blocks() == 5 and   
            self.state_space[self.locDrop[1][0], self.locDrop[1][1], self.locDrop[1][2]].get_num_blocks() == 5 and   
            self.state_space[self.locDrop[2][0], self.locDrop[2][1], self.locDrop[2][2]].get_num_blocks() == 5 and   
            self.state_space[self.locDrop[3][0], self.locDrop[3][1], self.locDrop[3][2]].get_num_blocks() == 5):
            return True
        else:
            return False