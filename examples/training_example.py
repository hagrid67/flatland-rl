from flatland.envs.generators import complex_rail_generator
from flatland.envs.rail_env import RailEnv
import numpy as np
from flatland.utils.rendertools import RenderTool

np.random.seed(1)

# Use the complex_rail_generator to generate feasible network configurations with corresponding tasks
# Training on simple small tasks is the best way to get familiar with the environment
#
env = RailEnv(width=15,
              height=15,
              rail_generator=complex_rail_generator(nr_start_goal=10, nr_extra=10, min_dist=10, max_dist=99999, seed=0),
              number_of_agents=5)


# Import your own Agent or use RLlib to train agents on Flatland
# As an example we use a random agent here


class RandomAgent:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

    def act(self, state):
        """
        :param state: input is the observation of the agent
        :return: returns an action
        """
        return np.random.choice(np.arange(self.action_size))

    def step(self, memories):
        """
        Step function to improve agent by adjusting policy given the observations

        :param memories: SARS Tuple to be
        :return:
        """
        return

    def save(self):
        # Store the current policy
        return


# Load the agent with the parameters corresponding to the environment and observation_builder
agent = RandomAgent(env.get_observation_size(), env.get_action_size())
n_trials = 1000

# Empty dictionary for all agent action
action_dict = dict()

for trials in range(1, n_trials + 1):

    # Reset environment and get initial observations for all agents
    obs = env.reset()
    # Here you can also further enhance the provided observation by means of normalization
    # See training navigation example in the baseline repository

    score = 0
    # Run episode
    for step in range(100):
        # Chose an action for each agent in the environment
        for a in range(env.get_num_agents()):
            action = agent.act(obs[a])
            action_dict.update({a: action})

        # Environment step which returns the observations for all agents, their corresponding
        # reward and whether their are done
        next_obs, all_rewards, done, _ = env.step(action_dict)

        # Update replay buffer and train agent
        agent.step(obs[a], action_dict[a], all_rewards[a], next_obs[a], done[a])
        score += all_rewards[a]

        obs = next_obs.copy()
        if done['__all__']:
            break
