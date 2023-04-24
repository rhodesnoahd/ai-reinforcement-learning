class Action:
    """
    Class to facilitate actions taken by agents in StateSpace.

    arguments: (all functions)
    agent - 'F' for female agent; 'M' for male agent
    ssObj - StateSpace Class object
    """
    def is_pickup_applicable(self, agent, ssObj):
        """
        returns True if agent can validly pick up a block and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check cell type
        if not ssObj.is_pickup(loc):
            return False
        
        # check carrying
        if ssObj.is_agent_carrying(agent):
            return False
        
        # check number of blocks
        if ssObj.state_space[loc[0], loc[1], loc[2]].get_num_blocks() <= 0:
            return False

        return True

    def is_dropoff_applicable(self, agent, ssObj):
        """
        returns True if agent can validly drop off a block and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check cell type
        if not ssObj.is_dropoff(loc):
            return False

        # check carrying
        if not ssObj.is_agent_carrying(agent):
            return False

        # check number of blocks
        if ssObj.state_space[loc[0], loc[1], loc[2]].get_num_blocks() >= 5:
            return False

        return True

    def is_east_applicable(self, agent, ssObj):
        """
        returns True if agent can validly move east and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check bounds
        if loc[0] >= 2:
            return False
        
        # check occupied
        loc = [loc[0] + 1, loc[1], loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def is_west_applicable(self, agent, ssObj):
        """
        returns True if agent can validly move west and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check bounds
        if loc[0] <= 0:
            return False
        
        # check occupied
        loc = [loc[0] - 1, loc[1], loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def is_north_applicable(self, agent, ssObj):
        """
        returns True if agent can validly move north and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check bounds
        if loc[1] >= 2:
            return False
        
        # check occupied
        loc = [loc[0], loc[1] + 1, loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def is_south_applicable(self, agent, ssObj):
        """
        returns True if agent can validly move south and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check bounds
        if loc[1] <= 0:
            return False
        
        # check occupied
        loc = [loc[0], loc[1] - 1, loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def is_up_applicable(self, agent, ssObj):
        """
        returns True if agent can validly move up and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check bounds
        if loc[2] >= 2:
            return False
        
        # check occupied
        loc = [loc[0], loc[1], loc[2] + 1]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def is_down_applicable(self, agent, ssObj):
        """
        returns True if agent can validly move down and False otherwise
        """
        loc = ssObj.get_location(agent)

        # check bounds
        if loc[2] <= 0:
            return False
        
        # check occupied
        loc = [loc[0], loc[1], loc[2] - 1]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def move_east(self, agent, ssObj):
        """
        moves an agent east by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_east_applicable(agent, ssObj):
            newLoc = [loc[0]+1, loc[1], loc[2]]

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].remove_agent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].add_agent(agent)
            ssObj.update_agent_loc(agent, newLoc)

    def move_west(self, agent, ssObj):
        """
        moves an agent west by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_west_applicable(agent, ssObj):
            newLoc = [loc[0]-1, loc[1], loc[2]]

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].remove_agent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].add_agent(agent)
            ssObj.update_agent_loc(agent, newLoc)

    def move_north(self, agent, ssObj):
        """
        moves an agent north by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_north_applicable(agent, ssObj):
            newLoc = [loc[0], loc[1]+1, loc[2]]

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].remove_agent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].add_agent(agent)
            ssObj.update_agent_loc(agent, newLoc)

    def move_south(self, agent, ssObj):
        """
        moves an agent south by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_south_applicable(agent, ssObj):
            newLoc = [loc[0], loc[1]-1, loc[2]]

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].remove_agent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].add_agent(agent)
            ssObj.update_agent_loc(agent, newLoc)

    def move_up(self, agent, ssObj):
        """
        moves an agent up by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_up_applicable(agent, ssObj):
            newLoc = [loc[0], loc[1], loc[2]+1]

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].remove_agent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].add_agent(agent)
            ssObj.update_agent_loc(agent, newLoc)

    def move_down(self, agent, ssObj):
        """
        moves an agent down by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_down_applicable(agent, ssObj):
            newLoc = [loc[0], loc[1], loc[2]-1]

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].remove_agent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].add_agent(agent)
            ssObj.update_agent_loc(agent, newLoc)

    def pickup_block(self, agent, ssObj):
        """
        picks up a block by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_pickup_applicable(agent, ssObj):
            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].remove_block()
            ssObj.update_agent_carrying(agent, True)

    def dropoff_block(self, agent, ssObj):
        """
        drops off a block by updating state space object
        returns nothing
        """
        loc = ssObj.get_location(agent)

        # perform check
        if self.is_dropoff_applicable(agent, ssObj):
            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].add_block()
            ssObj.update_agent_carrying(agent, False)