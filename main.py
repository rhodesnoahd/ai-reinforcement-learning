from queue import Queue
from stateSpace import StateSpace
from action import Action
from agent import Agent
from rlw import VSSpace, SSSpace, MSpace
from policy import PGreedy, PExploit, PRandom
import argparse
import copy
import csv

# Manhattan
def distance(locF, locM):
    return (abs(locF[0] - locM[0])
            + abs(locF[1] - locM[1])
            + abs(locF[2] - locM[2]))

def write_actions(agentFActions, agentMActions, id, seed, rewardList, distList, vizFile, movingAgent):
    """
    Write agent history and other performance metrics to files
    These are used for analysis and for offline visualization
    This is run at the end of simulation when the --history
    flag is supplied
    """
    with open('out/f_actions', 'w', encoding="utf-8") as f:
        for action in agentFActions:
            f.write('%s\n' % action)
    with open('out/m_actions', 'w', encoding="utf-8") as f:
        for action in agentMActions:
            f.write('%s\n' % action)
    with open('out/experiment_id', 'w', encoding="utf-8") as f:
        f.write(id)
    with open('out/experiment_seed', 'w', encoding="utf-8") as f:
        f.write(seed)
    with open(vizFile, 'w', newline='',encoding="utf-8") as f:
        write = csv.writer(f)
        for i, (rewards, distance, agent) in enumerate(zip(rewardList, distList, movingAgent)):
            write.writerow([i+1, rewards, distance, agent])

def write_terminal_states(terminal_states):
    """
    Write a CSV file containing the terminal state times
    These are used for analysis of performance
    This is run at the end of simulation when the --history
    flag is supplied
    """
    with open('out/terminal_states', 'w', encoding="utf-8") as f:
        write = csv.writer(f, delimiter=',')
        write.writerow(['Steps'])
        for s in terminal_states:
            write.writerow([s])

def write_table(agentFtable, agentMtable):
    """
    Write the entire Q-table for each agent to file
    This is used for the offline visualization of the entire run
    This is called appropriately at the end of the simulation
    when the --dump-tables option is supplied
    """
    with open('out/f_table.txt', 'w', encoding="utf-8") as f:
        for table in agentFtable:
            f.write('%s\n' % str(table))
    with open('out/m_table.txt', 'w', encoding="utf-8") as f:
        for table in agentMtable:
            f.write('%s\n' % str(table))

def write_report_timing(timings):
    """
    Write the timesteps for report Q-table dumps
    This is used for providing visualizations for the report
    This is called appropriately in the simulation
    when the --report option is supplied
    """
    with open(f'out/report_timings.txt', 'w', encoding='utf-8') as f:
        for t in timings:
            f.write(str(t) + '\n')

def reload_queue(q):
    # empty queue and load F first then M
    q.get()
    q.put('F')
    q.put('M')

def experiment(args):
    """
    Implements the event loop for experiments
    argparse object args has the following parameters:
    id - '1a', '1b', '1c', '2', '3a', '3b', '4'
    seed - seed value for reproducibility
    produce_history - whether to write agent history/analytics to file
    dump_table - whether to dump complete agent Q-table history to file
    rl_type - type of RL state space to use (options: 'vs', 'c2', 'ss')
    vizFile - filename for providing analytics
    """
    # Parse argument options
    id = args.experiment
    seed = args.seed
    produce_history = args.produce_history
    dump_table = args.dump_tables
    rl_type = args.rl_type
    vizFile = args.vizFile
    
    print(f"\n### Experiment {id} running with seed {seed} ###\n")
    
    # Setting hyperparameters appropriately
    alpha = 0.3
    if id == '1a' or id == '1b' or id == '1c' or id == '2' or id == '4':
        alpha = 0.3
    elif id == '3a':
        alpha = 0.1
    elif id == '3b':
        alpha = 0.5
    gamma = 0.5

    # Setting real world state space object RW
    RW = StateSpace('original')

    # Setting RL state space object RLW
    RLW = SSSpace()
    if rl_type == 'ss':
        RLW = SSSpace()
    elif rl_type == 'vs':
        RLW = VSSpace()
    elif rl_type == 'ms':
        RLW = MSpace()
    
    actions = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']

    # Initialize agents with PRANDOM and appropriate arguments

    policyF = PRandom('F', RLW, actions, seed=seed)
    policyM = PRandom('M', RLW, actions, seed=seed)

    agentF = Agent('F', RLW, policyF, RW, alpha, gamma)
    agentM = Agent('M', RLW, policyM, RW, alpha, gamma)

    # We utilize a Queue to store the order of the agents

    q = Queue(maxsize=2)
    q.put('F')
    q.put('M')

    # Here we create some Lists to store the results
    # from the simulation for offline visualization and analytics

    # stores the rewards obtained for analytics
    rewardList = []

    # stores the distance between agents for analytics
    distList = []

    # stores the actions taken by agent 'F'
    agentFActions = []

    # stores the actions taken by agent 'M'
    agentMActions = []

    # stores the qtable dumps of agent 'F'
    agentFtable = []

    # stores the qtable dumps of agent 'M'
    agentMtable = []

    # number of terminal states reached
    terminal = 0

    # agent that is moving for each iteration (for CSV)
    movingAgent = []

    # actions required for each terminal state (for performance)
    terminal_state_actions = []

    # timings for Q-table dumps in the visualization
    timings = []
    dropoff_timing_not_written = True

    # iteration number
    n = 0

    # number of actions between terminal states
    numActions = 0

    # just terminated flag
    justTerminated = False

    # MAIN EVENT LOOP
    # Briefly, the agent whose turn it is, chooses an action
    # History/analytics objects are updated as appropriate
    # RW is updated by the results of the action, and a reward is calculated
    # The agent that moved is updated and using this reward performs SARSA/QL
    # Various states are tested, and policies/dropoffs change depending on experiment
    # If the RW indicates that a terminal state is reached, RW is reset
    # The end result of the experiment is tested and analytic objects
    # are written to a file as necessary before exiting

    while True:
        # 'F' or 'M'
        curAgent = q.get()

        movingAgent.append(curAgent)

        # choose action
        if curAgent == 'F':
            action = agentF.choose_action(RW)
            if produce_history:
                agentFActions.append(action)
        elif curAgent == 'M':
            action = agentM.choose_action(RW)
            if produce_history:
                agentMActions.append(action)

        # perform action
        reward = RW.perform_action(curAgent, action)
        numActions += 1

        # update qtable
        if curAgent == 'F':
            agentF.update(RW, reward)
        elif curAgent == 'M':
            agentM.update(RW, reward)

        rewardList.append(reward)

        # dump qtable
        if dump_table:
            if curAgent == 'F':
                agentFtable.append(agentF.extract_table(copy.deepcopy(RW)))
            elif curAgent == 'M':
                agentMtable.append(agentM.extract_table(copy.deepcopy(RW)))

        # When the first dropoff is filled, dump qtable
        if dump_table and RW.is_first_dropoff_filled() and dropoff_timing_not_written:
            print(f"Recording {n+1} in report timings")
            timings.append(n+1)
            dropoff_timing_not_written = False      

        # Store distance between agents after 'M' moves
        distList.append(distance(RW.locF, RW.locM))

        # check completion criterion
        if RW.is_complete():
            justTerminated = True
            terminal += 1
            if dump_table:
                print(f"Recording {n+1} in report timings")
                timings.append(n+1)
            print(f"Terminal state {terminal} reached after {numActions} actions\n")
            terminal_state_actions.append(numActions)
            numActions = 0
            if id == '4' and (terminal == 1 or terminal == 2):
                RW = StateSpace('original')
                reload_queue(q)
            elif id == '4' and (terminal == 3 or terminal == 4 or terminal == 5):
                if terminal == 3:
                    print("Pickup locations modified\n")
                RW = StateSpace('modified')
                reload_queue(q)
            elif id == '4' and terminal == 6:
                print(f"Total number of terminal states reached: {terminal}") # 6
                if produce_history:
                    write_actions(agentFActions, agentMActions, id, str(seed), rewardList, distList, vizFile, movingAgent)
                    write_terminal_states(terminal_state_actions)
                if dump_table:
                    #print(agentFtable)
                    write_table(agentFtable, agentMtable)
                break
            elif id != '4':
                RW = StateSpace('original')
                reload_queue(q)
        # Provide progress updates of RW periodically to stdout
        if n % (250-1) == 0:
            print(RW.get_state_representation())
        
        # This tests if the game was just completed

        if not justTerminated:
            q.put(curAgent)
        
        justTerminated = False
        
        n += 1

        # switch policy after first 500 moves for 1b, 1c, 2, 3, & 4
        if id != '1a':
            if n == 500:
                if id == '1b':
                    agentF.set_policy(PGreedy('F', RLW, actions, seed=seed))
                    agentM.set_policy(PGreedy('M', RLW, actions, seed=seed))
                elif id == '1c' or id == '2' or id == '3a' or id == '3b' or id == '4':
                    agentF.set_policy(PExploit('F', RLW, actions, seed=seed))
                    agentM.set_policy(PExploit('M', RLW, actions, seed=seed))
                if id == '2':
                    # run the SARSA q-learning variation for 9500 steps
                    agentF.set_learning('sarsa')
                    agentM.set_learning('sarsa')

        # stop after 10,000 moves
        if n == 10000:
            # TODO dump qtable
            print(f"Recording {n-1} in report timings")
            timings.append(n-1)
            print(f"\nTotal number of terminal states reached: {terminal}")
            if produce_history:
                write_actions(agentFActions, agentMActions, id, str(seed), rewardList, distList, vizFile, movingAgent)
                write_terminal_states(terminal_state_actions)
            if dump_table:
                #print(agentFtable)
                print(timings)
                write_report_timing(timings)
                write_table(agentFtable, agentMtable)
            break


def main():
    """
    Entry point of the simulation
    Arguments are parsed and passed to experiment()
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("experiment", help="Experiment to run", type=str)
    arg_parser.add_argument("seed", help="Random seed to use", type=int)
    arg_parser.add_argument("-i", "--history",
        dest="produce_history",
        help="Produce history for visualization",
        required=False,
        action="store_true")
    arg_parser.add_argument("-d", "--dump-tables",
        dest="dump_tables",
        help="Dump Q-tables to files m_table.txt and f_table.txt",
        required=False,
        action="store_true")
    arg_parser.add_argument("-r", "--rl", 
        dest="rl_type",
        help="Choose RL state space type",
        required=False,
        type=str,
        default='ss')
    arg_parser.add_argument("-v", "--viz",
        dest="vizFile",
        help="Choose destination of visualization CSV",
        required=False,
        type=str,
        default='out/visualization.csv')
    args = arg_parser.parse_args()
    experiment(args)

if __name__ == "__main__":
    main()
