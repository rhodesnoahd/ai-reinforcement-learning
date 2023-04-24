import numpy as np

class RLSpace:
    """
    An abstract class representing the Reinforcement Learning (RL) state space
    It provides mappings from the real-world state space, and information about the shape of the space.
    """
    def map_state(self, state, agent):
        """
        Given a real-world state, provide a state in the RL state space of the given agent
        """
        pass

    def shape(self):
        """
        Returns shape of RL space, used to generate Q table
        This is used as the .shape parameter of the Numpy array created to store the states
        """
        pass

class VSSpace(RLSpace):
    """
    "Very Simple" RL space: each agent's RL space contains only their coordinates, and whether they hold a block.
    """
    def map_state(self, state, agent):
        loc = state.get_location(agent)
        is_carrying = state.is_agent_carrying(agent)
        return (loc[0], loc[1], loc[2], 1 if is_carrying else 0)
    
    def shape(self):
        return (3, 3, 3, 2)

class SSSpace(RLSpace):
    """
    "Somewhat Simple" RL space: each agent's RL space contains only their coordinates, whether they hold a block,
    and the relative position of the other agent
    """
    def map_state(self, state, agent):
        loc = state.get_location(agent)
        other_loc = state.get_location('F' if agent == 'M' else 'M')
        is_carrying = state.is_agent_carrying(agent)
        return (loc[0], loc[1], loc[2], 1 if is_carrying else 0,
                (loc[0] - other_loc[0]) + 2, 
                (loc[1] - other_loc[1]) + 2,
                (loc[2] - other_loc[2]) + 2)
    
    def shape(self):
        return (3, 3, 3, 2, 5, 5, 5)
    
class MSpace(RLSpace):
    """
    "Medium" complexity RL space: stores the agent position/block status, and the status of the pickup-dropoff only (not other agent)
    """
    def map_state(self, state, agent):
        loc = state.get_location(agent)
        #other_loc = state.get_location('F' if agent == 'M' else 'M')
        is_carrying = state.is_agent_carrying(agent)
        dropoff_1, dropoff_2, dropoff_3, dropoff_4, pickup_1, pickup_2 = state.get_state_representation()[8:]
        return (loc[0], loc[1], loc[2], 1 if is_carrying else 0,  
            1 if dropoff_1 < 5 else 0,
            1 if dropoff_2 < 5 else 0,
            1 if dropoff_3 < 5 else 0,
            1 if dropoff_4 < 5 else 0,
            1 if pickup_1 > 0 else 0,
            1 if pickup_2 > 0 else 0)

    def shape(self):
        return (3, 3, 3, 2, 2, 2, 2, 2, 2, 2)