import pygame
import os
from pygame.font import Font
from queue import Queue
import numpy as np
import argparse
import ast

# import action lists
agentFActions = []
agentMActions = []
with open('out/f_actions', 'r', encoding="utf-8") as f:
    for line in f:
        x = line[:-1]
        agentFActions.append(x)
with open('out/m_actions', 'r', encoding="utf-8") as f:
    for line in f:
        x = line[:-1]
        agentMActions.append(x)

# import experiment id
with open('out/experiment_id', 'r', encoding="utf-8") as f:
    for line in f:
        id = line

# import experiment seed
with open('out/experiment_seed', 'r', encoding="utf-8") as f:
    for line in f:
        seed = line

# controls overall size
SCALE = 1.0

# create window
WIDTH, HEIGHT = (SCALE*1200), (SCALE*400)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Reinforcement Learning Visualization | Experiment: {id} | Seed: {seed}")

# colors
LIGHT_YELLOW = (255, 255, 204)
PURPLE = (128, 0, 128)

# speed of execution
FPS = 60

# importing assets

# 3x3 grid
Z_LEVEL = pygame.image.load(os.path.join('assets', 'grid.png'))

# grid labels
# Create font object and set font size
pygame.font.init()
font = Font(None, int(SCALE*28))
# Create text surfaces for the labels
Z1_LABEL = font.render('z=1', True, PURPLE)
Z2_LABEL = font.render('z=2', True, PURPLE)
Z3_LABEL = font.render('z=3', True, PURPLE)

# Pickup, Dropoff, Risk cell labels
P = pygame.image.load(os.path.join('assets','p_pix.png'))
D = pygame.image.load(os.path.join('assets','d_pix.png'))
R = pygame.image.load(os.path.join('assets','r_pix.png'))

# agents
FEMALE_AGENT = pygame.image.load(os.path.join('assets', 'female_agent.png'))
FEMALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'female_agent_simple.png'))
MALE_AGENT = pygame.image.load(os.path.join('assets', 'male_agent.png'))
MALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'male_agent_simple.png'))

# block to pickup/dropoff
BLOCK = pygame.image.load(os.path.join('assets', 'block.png'))

# arrow for q-table viz
ARROW = {}
ARROW['F'] = {}
ARROW['M'] = {}
MALE_ARROW = pygame.image.load(os.path.join('assets', 'male-arrow.png'))
FEMALE_ARROW = pygame.image.load(os.path.join('assets', 'female-arrow.png'))
for g in ['F', 'M']:
    gender = 'female' if g == 'F' else 'male'
    CUR_ARROW = MALE_ARROW if g == 'M' else FEMALE_ARROW
    ARROW[g]['N'] = CUR_ARROW
    ARROW[g]['W'] = pygame.transform.rotate(CUR_ARROW, 90)
    ARROW[g]['S'] = pygame.transform.rotate(CUR_ARROW, 180)
    ARROW[g]['E'] = pygame.transform.rotate(CUR_ARROW, 270)
    ARROW[g]['U'] = pygame.image.load(os.path.join('assets', f'{gender}-up-arrow.png'))
    ARROW[g]['D'] = pygame.image.load(os.path.join('assets', f'{gender}-down-arrow.png'))
    ARROW[g]['Pickup'] = pygame.image.load(os.path.join('assets', f'{gender}-pickup-label.png'))
    ARROW[g]['Dropoff'] = pygame.image.load(os.path.join('assets', f'{gender}-dropoff-label.png'))

# define new asset sizes
RESIZED_Z_LEVEL = (SCALE*360,SCALE*360)
RESIZED_LETTERS = (SCALE*35,SCALE*45)
RESIZED_AGENTS = (SCALE*35,SCALE*45)
RESIZED_BLOCK = (SCALE*25,SCALE*25)

# resize assets
grid = pygame.transform.scale(Z_LEVEL,RESIZED_Z_LEVEL)
p = pygame.transform.scale(P,RESIZED_LETTERS)
d = pygame.transform.scale(D,RESIZED_LETTERS)
r = pygame.transform.scale(R,RESIZED_LETTERS)
f_not_carrying = pygame.transform.scale(FEMALE_AGENT_SIMPLE,RESIZED_AGENTS)
f_carrying = pygame.transform.scale(FEMALE_AGENT,RESIZED_AGENTS)
m_not_carrying = pygame.transform.scale(MALE_AGENT_SIMPLE,RESIZED_AGENTS)
m_carrying = pygame.transform.scale(MALE_AGENT,RESIZED_AGENTS)
block = pygame.transform.scale(BLOCK,RESIZED_BLOCK)

# asset locations

# z levels
Z1_LOCATION = (SCALE*10,SCALE*10)
Z2_LOCATION = (SCALE*420,SCALE*10)
Z3_LOCATION = (SCALE*830,SCALE*10)

# grid labels
Z1_LABEL_LOCATION = (SCALE*178,SCALE*373)
Z2_LABEL_LOCATION = (SCALE*579,SCALE*373)
Z3_LABEL_LOCATION = (SCALE*988,SCALE*373)

# pickup labels
P_LOCATION_221 = (SCALE*135,SCALE*200)
P_LOCATION_332 = (SCALE*660,SCALE*85)

# modified pickup labels
P_LOCATION_131 = (SCALE*19,SCALE*82)
P_LOCATION_233 = (SCALE*957,SCALE*85)

# dropoff labels
D_LOCATION_311 = (SCALE*250,SCALE*320)
D_LOCATION_112 = (SCALE*425,SCALE*320)
D_LOCATION_113 = (SCALE*835,SCALE*320)
D_LOCATION_323 = (SCALE*1070,SCALE*200)

# risk labels
R_LOCATION_321 = (SCALE*250,SCALE*200)
R_LOCATION_222 = (SCALE*545,SCALE*200)

# agents
F_START = (SCALE*55, SCALE*285)
M_START = (SCALE*(990+120), SCALE*(120+55))

# Z=1 agent blit locations
LOC_111 = (SCALE*55, SCALE*285) 
LOC_211 = (SCALE*175, SCALE*285)
LOC_311 = (SCALE*295, SCALE*285)
LOC_121 = (SCALE*55, SCALE*165)
LOC_221 = (SCALE*175, SCALE*165)
LOC_321 = (SCALE*295, SCALE*165)
LOC_131 = (SCALE*55, SCALE*45) 
LOC_231 = (SCALE*175, SCALE*45)
LOC_331 = (SCALE*295, SCALE*45)

# Z=2 agent blit locations
LOC_112 = (SCALE*465, SCALE*285)
LOC_212 = (SCALE*585, SCALE*285)
LOC_312 = (SCALE*705, SCALE*285)
LOC_122 = (SCALE*465, SCALE*165)
LOC_222 = (SCALE*585, SCALE*165)
LOC_322 = (SCALE*705, SCALE*165)
LOC_132 = (SCALE*465, SCALE*45)
LOC_232 = (SCALE*585, SCALE*45)
LOC_332 = (SCALE*705, SCALE*45)

# Z=3 agent blit locations
LOC_113 = (SCALE*875, SCALE*285)
LOC_213 = (SCALE*995, SCALE*285)
LOC_313 = (SCALE*1115, SCALE*285)
LOC_123 = (SCALE*875, SCALE*165)
LOC_223 = (SCALE*995, SCALE*165)
LOC_323 = (SCALE*1115, SCALE*165) 
LOC_133 = (SCALE*875, SCALE*45)
LOC_233 = (SCALE*995, SCALE*45)
LOC_333 = (SCALE*1115, SCALE*45)

# put agent blit locations into 3d array
LOC_MATRIX = np.empty(shape=(3, 3, 3), dtype=object, order='C')

LOC_MATRIX[0,0,0] = LOC_111
LOC_MATRIX[1,0,0] = LOC_211
LOC_MATRIX[2,0,0] = LOC_311 
LOC_MATRIX[0,1,0] = LOC_121
LOC_MATRIX[1,1,0] = LOC_221
LOC_MATRIX[2,1,0] = LOC_321
LOC_MATRIX[0,2,0] = LOC_131
LOC_MATRIX[1,2,0] = LOC_231
LOC_MATRIX[2,2,0] = LOC_331

LOC_MATRIX[0,0,1] = LOC_112 
LOC_MATRIX[1,0,1] = LOC_212
LOC_MATRIX[2,0,1] = LOC_312 
LOC_MATRIX[0,1,1] = LOC_122
LOC_MATRIX[1,1,1] = LOC_222
LOC_MATRIX[2,1,1] = LOC_322
LOC_MATRIX[0,2,1] = LOC_132
LOC_MATRIX[1,2,1] = LOC_232
LOC_MATRIX[2,2,1] = LOC_332

LOC_MATRIX[0,0,2] = LOC_113 
LOC_MATRIX[1,0,2] = LOC_213
LOC_MATRIX[2,0,2] = LOC_313
LOC_MATRIX[0,1,2] = LOC_123
LOC_MATRIX[1,1,2] = LOC_223
LOC_MATRIX[2,1,2] = LOC_323 
LOC_MATRIX[0,2,2] = LOC_133
LOC_MATRIX[1,2,2] = LOC_233
LOC_MATRIX[2,2,2] = LOC_333

MOVE_OFFSET_NESW = SCALE*120
MOVE_OFFSET_UD = SCALE*410

class Agent:
    """
    Class which allows us to pass many attributes related to an agent by reference 
    and call methods to modify those attributes.

    Properties:
    id - 'F' or 'M'
    loc - (x,y) coordinates on display window
    asset - image used to represent agent visually
    actionList - list of actions agent will perform generated from prior simulation
    qtable - Q-table of agent generated from prior simulation
    index - used to access agent's actionList
    """
    def __init__(self, _id, _loc, _asset, _actionList, _qtable = None):
        self.id = _id # F or M
        self.loc = _loc
        self.asset = _asset
        self.actionList = _actionList
        self.qtable = _qtable
        self.index = 0
        self.has_block = False
    
    def set_asset(self, _asset):
        """
        sets the asset of the agent
        """
        self.asset = _asset

    def move_east(self):
        """
        moves the agent east by updating its location
        returns nothing
        """
        self.loc = (self.loc[0]+1, self.loc[1], self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def move_west(self):
        """
        moves the agent west by updating its location
        returns nothing
        """
        self.loc = (self.loc[0]-1, self.loc[1], self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])
  
    def move_north(self):
        """
        moves the agent north by updating its location
        returns nothing
        """
        self.loc = (self.loc[0], self.loc[1]+1, self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def move_south(self):
        """
        moves the agent south by updating its location
        returns nothing
        """
        self.loc = (self.loc[0], self.loc[1]-1, self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def move_up(self):
        """
        moves the agent up by updating its location
        returns nothing
        """
        self.loc = (self.loc[0], self.loc[1], self.loc[2]+1)
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])
    
    def move_down(self):
        """
        moves the agent down by updating its location
        returns nothing
        """
        self.loc = (self.loc[0], self.loc[1], self.loc[2]-1)
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def pickup(self):
        """
        performs pickup action by changing agent's asset to colored version
        """
        self.has_block = True
        if self.id == 'F':
            self.asset = f_carrying
        elif self.id == 'M':
            self.asset = m_carrying
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def dropoff(self):
        """
        performs dropoff action by changing agent's asset to simple version
        """
        self.has_block = False
        if self.id == 'F':
            self.asset = f_not_carrying
        elif self.id == 'M':
            self.asset = m_not_carrying
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def set_table(self, qtable):
        """
        sets the Q-table of the agent
        """
        self.qtable = qtable

    def get_table_state(self):
        """
        returns the state of agent's Q-table
        """
        if self.qtable:
            return self.qtable[self.index]

class Conditions:
    """
    Class which allows us to pass conditions by reference and 
    update attributes as events occur during visualizaiton
    """
    def __init__(self):
        self.numDropoff = 0
        self.numActions = 0
        self.numTerminal = 0
        self.id = None
        self.is_modified = False
        self.has_switched = False
class Block:
    """
    Class which defines Pickup & Dropoff block blit locations and
    allows us to pass many block attributes by reference
    """
    def __init__(self):
        self.pickup_one = 10
        self.pickup_two = 10
        self.block_arr_one = [] #floor 1 
        self.block_arr_two = [] #floor 2

        self.block_one_y = (SCALE*223 )
        self.block_two_y = (SCALE*107)
        self.block_one_x = (SCALE*220)
        self.block_two_x = (SCALE*750)

        self.offset = 11 * SCALE

        for i in range(10):
            block1 = (self.block_one_x,self.block_one_y)
            block2 = (self.block_two_x,self.block_two_y)
            self.block_arr_one.append(block1)
            self.block_arr_two.append(block2)
            self.block_one_y = self.block_one_y - self.offset
            self.block_two_y = self.block_two_y - self.offset

        self.drop_off_one = [] 
        self.drop_off_two = []
        self.drop_off_three = []
        self.drop_off_four = []
        self.itr1 = 0
        self.itr2 = 0
        self.itr3 = 0
        self.itr4 = 0
        self.y1 = SCALE * 341
        self.y2 = SCALE * 341
        self.y3 = SCALE * 341
        self.y4 = SCALE * 223

        self.modifiedBlock_one_x = (SCALE * 103)
        self.modifiedBlock_one_y =(SCALE * 106)
        self.modifiedBlock_two_x = (SCALE * 1040)
        self.modifiedBlock_two_y = (SCALE * 106)

    def modifiy_pickup_block_locations(self):
        self.block_arr_one = []
        self.block_arr_two = []
        for i in range(10):
            block1 = (self.modifiedBlock_one_x,self.modifiedBlock_one_y)
            block2 = (self.modifiedBlock_two_x,self.modifiedBlock_two_y)
            self.block_arr_one.append(block1)
            self.block_arr_two.append(block2)
            self.modifiedBlock_one_y = self.modifiedBlock_one_y - self.offset
            self.modifiedBlock_two_y = self.modifiedBlock_two_y - self.offset

def draw_window(c, agent, b):
    """
    draws the window for each frame by blitting static assets and
    conditionally blitting dynamic assets
    """
    WIN.fill(LIGHT_YELLOW)

    WIN.blit(grid, Z1_LOCATION)
    WIN.blit(grid, Z2_LOCATION)
    WIN.blit(grid, Z3_LOCATION)

    WIN.blit(Z1_LABEL, Z1_LABEL_LOCATION)
    WIN.blit(Z2_LABEL, Z2_LABEL_LOCATION)
    WIN.blit(Z3_LABEL, Z3_LABEL_LOCATION)

    if c.is_modified:
        WIN.blit(p, P_LOCATION_131)
        WIN.blit(p, P_LOCATION_233)
    else:
        WIN.blit(p, P_LOCATION_221)
        WIN.blit(p, P_LOCATION_332)

    WIN.blit(d, D_LOCATION_311)
    WIN.blit(d, D_LOCATION_112)
    WIN.blit(d, D_LOCATION_113)
    WIN.blit(d, D_LOCATION_323)

    WIN.blit(r, R_LOCATION_321)
    WIN.blit(r, R_LOCATION_222)
    
    if c.numActions == 0:
        WIN.blit(f_not_carrying, LOC_MATRIX[0][0][0])
        WIN.blit(m_not_carrying, LOC_MATRIX[2][1][2])
    else:
        draw_action(c, agent, b)

    pygame.display.update()

def draw_qtable(c, agent, b, has_block = None):
    """
    draws the Q-table assets at each state
    The Q-table values are scaled logarithmically to the range [0.5, 1.0]
    These scaled values are used to resize a sprite corresponding to the action
    This sprite is blitted on the square
    """
    q_values, q_directions = agent.get_table_state()
    max_q = np.max(q_values)
    min_q = np.min(q_values)
    alpha = 0.5
    beta = 1.0
    def scale(x):
        if (min_q == max_q):
            return 1.0
        a = (np.exp(beta)-np.exp(alpha))/(max_q - min_q)
        b = (np.exp(alpha)*max_q - np.exp(beta)*min_q)/(max_q - min_q)
        return np.log(a*x+b)

    for i in range(3):
        for j in range(3):
            for k in range(3):
                if has_block is None:
                    has_block = agent.has_block
                index = i*18+j*6+k*2+has_block
                q_direction = q_directions[index]
                # If there is no favored direction in the Q-table, don't draw any visualization
                if q_direction == '':
                    continue
                # q_values are used to produce scaled image sizes
                q_value = scale(q_values[index]) // (1/ 64.)
                scaled = (q_value, q_value)
                # The location we draw to has to be offset so that it remains centered after resizing
                offset = 64 - q_value
                draw_x = LOC_MATRIX[i,j,k][0]+(offset // 2)
                draw_y = LOC_MATRIX[i,j,k][1]+(offset // 2)
                # The appropriate image is scaled and blitted to the screen in the proper location
                rect = pygame.Rect((draw_x, draw_y), scaled)
                scaled_img = pygame.transform.scale(ARROW[agent.id][q_direction], scaled)
                WIN.blit(scaled_img, rect)

def draw_action(c, agent, b):
    """
    draws agent & block assets conditionally based on action performed
    """
    i = agent.index
    action = agent.actionList[i]
    if action == 'E':
        agent.move_east()
    elif action == 'W':
        agent.move_west()
    elif action == 'N':
        agent.move_north()
    elif action == 'S':
        agent.move_south()
    elif action == 'U':
        agent.move_up()
    elif action == 'D':
        agent.move_down()
   
    elif action == 'Pickup':
        agent.pickup()

        if c.is_modified and c.numTerminal == 3 and not c.has_switched:
            c.has_switched = True
            b.modifiy_pickup_block_locations()

        # original pickup locations
        if c.id != '4' and agent.loc == (1,1,0):
            b.pickup_one -= 1
        if c.id != '4' and agent.loc == (2,2,1):
            b.pickup_two -= 1
        
        # modified pickup locaitons
        if c.id == '4' and c.numTerminal < 3 and agent.loc == (1,1,0):
            b.pickup_one -= 1
        if c.id == '4' and c.numTerminal < 3 and agent.loc == (2,2,1):
            b.pickup_two -= 1
        if c.id == '4' and c.numTerminal >= 3 and agent.loc == (0,2,0):
            b.pickup_one -= 1
        if c.id == '4' and c.numTerminal >= 3 and agent.loc == (1,2,2):
            b.pickup_two -= 1
    
    elif action == 'Dropoff':
        agent.dropoff()
        c.numDropoff += 1
        if agent.loc == (2,0,0):
            if b.itr1 != 0: #itr is 0 here so we dont want to minus the offset yet
                b.y1 = b.y1 - b.offset
            dropoff_block = (SCALE * 340, b.y1)
            b.itr1 += 1
            b.drop_off_one.append(dropoff_block)
        elif agent.loc == (0,0,1):
            if b.itr2 != 0:
                b.y2 = b.y2 - b.offset
            dropoff_block_two = (SCALE * 515, b.y2)
            b.itr2 += 1
            b.drop_off_two.append(dropoff_block_two)
        elif agent.loc == (0,0,2):
            if b.itr3 != 0:
                b.y3 = b.y3 - b.offset
            dropoff_block_three = (SCALE * 925, b.y3)
            b.itr3 += 1
            b.drop_off_three.append(dropoff_block_three)
        elif agent.loc == (2,1,2):
            if b.itr4 != 0:
                b.y4 = b.y4 - b.offset
            dropoff_block_four = (SCALE * 1160, b.y4)
            b.itr4 += 1
            b.drop_off_four.append(dropoff_block_four)

    # blit pickup blocks
    for itr in range(b.pickup_one):
        game_block1 = b.block_arr_one[itr]
        WIN.blit(block,(game_block1[0], game_block1[1]))

    for itr_ in range(b.pickup_two):
        game_block2 = b.block_arr_two[itr_]
        WIN.blit(block,(game_block2[0],game_block2[1]))

    # blit dropoff blocks
    if b.itr1 != 0:
        for l in range(b.itr1):
            drp1 = b.drop_off_one[l]
            WIN.blit(block,(drp1[0],drp1[1]))

    if b.itr2 != 0:
        for k in range(b.itr2):
            drp2 = b.drop_off_two[k]
            WIN.blit(block,(drp2[0],drp2[1]))

    if b.itr3 != 0:
        for j in range(b.itr3):
            drp3 = b.drop_off_three[j]
            WIN.blit(block,(drp3[0],drp3[1]))

    if b.itr4 != 0:
        for h in range(b.itr4):
            drp4 = b.drop_off_four[h]
            WIN.blit(block,(drp4[0],drp4[1]))

def save_image(filename):
    pygame.image.save(WIN, filename)

def main():
    """
    Driver code to run PyGame visualization by iterating through the agents'
    action lists and Q-tables
    """
    # Argument parsing code for setting options
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--fps",
        dest="fps",
        help="Framerate of display updates (default 60)",
        required=False,
        type=int,
        default=60)
    arg_parser.add_argument("--qtable",
        dest="qtable",
        help="Visualize Q-table each turn",
        required=False,
        type=str,
        default='')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument("--no-block",
        dest="no_block",
        help="Whether to display the Q-table only for no-block condition",
        required=False,
        action="store_true")
    group.add_argument("--has-block", 
        dest="has_block",
        help="Whether to display the Q-table only for the has-block condition",
        required=False,
        action="store_true")
    arg_parser.add_argument("--report",
        dest="report",
        help="Produce images as specified for the report",
        required=False,
        action="store_true")
    arg_parser.add_argument("--paused",
        dest="paused",
        help="Start in single-step mode",
        required=False,
        action="store_true")
    args = arg_parser.parse_args()
    block_string = 'B' if args.has_block - args.no_block == 1 else 'N'
    paused = args.paused
    FPS = args.fps

    report_timings = []
    if args.report:
        with open('out/report_timings.txt', 'r') as f:
            for line in f:
                x = line[:-1]
                report_timings.append(int(x))
        print(f"timings: {report_timings}")

    c = Conditions()
    c.id = id
    
    b = Block()

    F = Agent('F', [0,0,0], f_not_carrying, agentFActions)
    M = Agent('M', [2,1,2], m_not_carrying, agentMActions)

    q = Queue(maxsize=2)
    q.put(M)
    q.put(F)

    run = True
    clock = pygame.time.Clock()

    # number of total iterations
    n = 0

    # load Q-table data
    if args.qtable:
        f_table = []
        m_table = []
        with open('out/f_table.txt', 'r') as f:
            for line in f:
                x = line[:-1]
                parsed = ast.literal_eval(x)
                f_table.append(parsed)
        with open('out/m_table.txt', 'r') as f:
            for line in f:
                x = line[:-1]
                parsed = ast.literal_eval(x)
                m_table.append(parsed)
        F.set_table(f_table)
        M.set_table(m_table)

    screengrab = False
    single_step = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = True if not paused else False
            if paused and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                single_step = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                FPS = min(FPS*2, 120)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                FPS = max(FPS//2, 1)
            elif paused and event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                screengrab = True
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                run = False

        if paused and screengrab:
            save_image(f'screengrab_{seed}_exp{id}_{n}.png')
            print('Screengrab captured')
            screengrab = False

        if args.report and n in report_timings:
            save_image(f'qtables/report_{seed}_exp{id}_{args.qtable}_{n}_{block_string}.png')

        if paused and not single_step:
            continue

        pygame.display.set_caption(f"Reinforcement Learning Visualization | Experiment: {id} | Seed: {seed} | n: {n}")

        curAgent = q.get()

        draw_window(c, curAgent, b)
        c.numActions += 1
        q.put(curAgent)

        if args.qtable:
            change_block = None
            if args.has_block or args.no_block:
                change_block = args.has_block
            if args.qtable == 'M':
                draw_qtable(c, M, b, change_block)
            elif args.qtable == 'F':
                draw_qtable(c, F, b, change_block)

        # redraw inactive agent
        if c.numActions != 0:
            if curAgent.id == 'F':
                WIN.blit(M.asset, LOC_MATRIX[M.loc[0]][M.loc[1]][M.loc[2]])
            else:
                WIN.blit(F.asset, LOC_MATRIX[F.loc[0]][F.loc[1]][F.loc[2]])
            pygame.display.update()




        # check terminal state
        if c.numDropoff == 20:
            c.numTerminal += 1
            if id == '4' and c.numTerminal == 3:
                c.is_modified = True
            c.numActions = 0
            c.numDropoff = 0
            F.loc = [0,0,0]
            M.loc = [2,1,2]
            curAgent = q.get()
            curAgent = q.get()
            q.put(M)
            q.put(F)
            b.pickup_one = 10
            b.pickup_two = 10
            b.drop_off_one = []
            b.drop_off_two = []
            b.drop_off_three = []
            b.drop_off_four = []
            b.y1 = 341 * SCALE
            b.y2 = 341 * SCALE
            b.y3 = 341 * SCALE
            b.y4 = 223 * SCALE
            b.itr1 = 0
            b.itr2 = 0
            b.itr3 = 0
            b.itr4 = 0

        if c.numActions != 0:
            n += 1
        if n >= 10000 or (id == '4' and c.numTerminal == 6):
            break # indicates end of experiment

        single_step = False
        
    pygame.quit()

if __name__ == "__main__":
    main()
