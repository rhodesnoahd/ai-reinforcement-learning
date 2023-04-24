class Cell:
    """
    Class to compose the RW state space
    """
    def __init__(self):
        """
        Constructor for Normal cell to initialize RW state space

        Properties:
        type - cells are 'Normal', 'Pickup', 'Dropoff', or 'Risk' type
        occupancy - list to hold a single agent
        numBlocks - number of blocks
        cost - Risk cells cost -2, all other types cost -1
        """
        self.type = 'Normal'
        self.occupancy = []
        self.numBlocks = 0
        self.cost = -1

    def get_type(self):
        """
        returns the type of cell
        """
        return self.type

    def set_type(self, type):
        """
        sets type of cell
        Pickup cells start with 10 blocks
        Risk cells cost -2
        argument:
        type - 'Pickup', 'Dropoff', or 'Risk'
        """
        if type == 'Pickup':
            self.numBlocks = 10
        if type == 'Risk':
            self.cost = -2
        self.type = type

    def is_occupied(self):
        """
        returns True if agent in cell and False otherwise
        """
        return bool(self.occupancy)

    def which_agent(self):
        """
        if occupied, returns 'M' or 'F'
        if unoccupied, returns None
        """
        if self.is_occupied():
            return self.occupancy[0]

    def add_agent(self, agent):
        """
        adds agent to unoccupied cell
        argument:
        agent - 'F' for female agent; 'M' for male agent
        """
        if not (self.is_occupied()):
            self.occupancy.append(agent)

    def remove_agent(self, agent):
        """
        removes agent from occupied cell
        argument:
        agent - 'F' for female agent; 'M' for male agent
        """
        if self.is_occupied():
            self.occupancy.remove(agent)

    def get_num_blocks(self):
        """
        returns the number of blocks in cell
        """
        return self.numBlocks

    def add_block(self):
        """
        adds a block to Dropoff cell by incrementing numBlocks if there are less than 5 blocks present
        capacity of Dropoff cells is 5 blocks
        """
        if self.type == 'Dropoff' and self.numBlocks < 5:
            self.numBlocks += 1

    def remove_block(self):
        """
        removes a block from Pickup cell by decrementing numBlocks if there is at least one block present
        """
        if self.type == 'Pickup' and self.numBlocks > 0:
            self.numBlocks -= 1

    def get_cost(self):
        """
        returns the cost of cell
        """
        return self.cost
