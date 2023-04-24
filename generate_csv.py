import os
from main import experiment

SEED1 = 1
SEED2 = 42

class Args():
    """
    To mimic the argparse library, this stub code is used
    """
    def __init__(self, experiment, seed, rl_type, csv_filename):
        self.experiment = experiment
        self.seed = seed
        self.rl_type = rl_type
        self.produce_history = True
        self.dump_tables = False
        self.vizFile = csv_filename

def main():
    """
    Script to produce performance variable data for the report
    Runs the full suite of experiments for our chosen RL state space models and seeds
    CSV files of reward histories, L1 agent distances, and the terminal states are produced
    These are processed in the included Jupyter Notebook file
    """
    i = 0
    for rl_type in ['ss', 'vs', 'ms']:
        for exp in ['1a', '1b', '1c', '2', '3a', '3b', '4']:        
            for seed in [SEED1, SEED2]:            
                viz_file = f'out/viz_{exp}_{seed}_{rl_type}.csv'
                args = Args(exp, seed, rl_type, viz_file)
                print('-'*80)
                print(f'{i}: {exp} - {seed} - {rl_type}')
                print('-'*80)
                experiment(args)
                if i == 0:
                    os.rename(viz_file, f'out/visualization.csv')
                    os.rename('out/terminal_states', f'out/terminal_states.csv')
                else:
                    os.rename(viz_file, f'out/visualization{i}.csv')
                    os.rename('out/terminal_states', f'out/terminal_states{i}.csv')
                i += 1

if __name__=='__main__':
    main()