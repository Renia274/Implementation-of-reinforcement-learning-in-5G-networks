import os
import random
import pdb
import gym
import pylab
import numpy as np
from collections import deque
from keras.models import Model, load_model
from keras.layers import Input, Dense, Lambda, Add
from keras.optimizers import Adam, RMSprop
from keras import backend as K
from custom_enviroment.envs.customenviromentt import TestCustomEnvv
from tensorflow.keras.optimizers import RMSprop, Adam



def OurModel(input_shape, action_space, dueling):
    X_input = Input(input_shape)
    X = X_input

    # Input Layer of state size(4) and Hidden Layer with 128 nodes
    X = Dense(128, input_shape=input_shape, activation="relu", kernel_initializer='he_uniform')(X)

    # Hidden layer with 64 nodes
    X = Dense(64, activation="relu", kernel_initializer='he_uniform')(X)

    # Hidden layer with 32 nodes
    X = Dense(32, activation="relu", kernel_initializer='he_uniform')(X)

    if dueling:
        state_value = Dense(1, kernel_initializer='he_uniform')(X)
        state_value = Lambda(lambda s: K.expand_dims(s[:, 0], -1), output_shape=(action_space,))(state_value)

        action_advantage = Dense(action_space, kernel_initializer='he_uniform')(X)
        action_advantage = Lambda(lambda a: a[:, :] - K.mean(a[:, :], keepdims=True), output_shape=(action_space,))(action_advantage)

        X = Add()([state_value, action_advantage])
    else:
        # Output Layer with # of actions: 8 nodes
        X = Dense(action_space, activation="linear", kernel_initializer='he_uniform')(X)

    model = Model(inputs = X_input, outputs = X, name='Dueling DQN model')
    model.compile(loss="mean_squared_error", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=["accuracy"])

    model.summary()
    return model

class DQNAgent:
    def __init__(self, env_name):
        self.env_name = env_name
        self.env = gym.make(env_name)
        self.env.seed(0)
        self.env._max_episode_steps = 20
        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n

        self.EPISODES = 2
        self.memory = deque(maxlen=5000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01 # minimum exploration probability
        self.epsilon_decay = 0.999 # exponential decay rate for exploration prob
        self.batch_size = 32
        self.train_start = 1000

        # defining model parameters
        self.dqn = True # use doudle deep q network
        self.Soft_Update = True # use soft parameter update
        self.dueling = True # use dealing netowrk

        self.TAU = 34.8 # target network soft update hyperparameter

        self.Save_Path = 'Models'
        if not os.path.exists(self.Save_Path): os.makedirs(self.Save_Path)
        self.scores, self.episodes, self.average = [], [], []

        if self.dqn:
            print("-------------DQN------------")
            self.Model_name = os.path.join(self.Save_Path,"Dueling DQN_"+self.env_name+".h5")

        # create main model and target model
        self.model = OurModel(input_shape=(self.state_size,), action_space = self.action_size, dueling = self.dueling)
        self.target_model = OurModel(input_shape=(self.state_size,), action_space = self.action_size, dueling = self.dueling)


    def update_target_model(self):
        if not self.Soft_Update:
            self.target_model.set_weights(self.model.get_weights())
            return
        if self.Soft_Update:
            q_model = self.model.get_weights()
            target_model= self.target_model.get_weights()
            counter = 0
            for q_weight, target_weight in zip(q_model, target_model):
                target_weight = target_weight * (1-self.TAU) + q_weight * self.TAU
                target_model[counter] = target_weight
                counter += 1
            self.target_model.set_weights(target_model)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > self.train_start:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

#choose an action via ε-greedy strategy
    def act(self, state):
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self):
        if len(self.memory) < self.train_start:
            return
        # Randomly sample minibatch from the memory
        minibatch = random.sample(self.memory, self.batch_size)

        state = np.zeros((self.batch_size, self.state_size))
        next_state = np.zeros((self.batch_size, self.state_size))
        action, reward, done = [], [], []

        #  before prediction

        for i in range(self.batch_size):
            state[i] = minibatch[i][0]
            action.append(minibatch[i][1])
            reward.append(minibatch[i][2])
            next_state[i] = minibatch[i][3]
            done.append(minibatch[i][4])


        # predict Q-values for starting state using the main network
        target = self.model.predict(state)
        # predict best action in ending state using the main network
        target_next = self.model.predict(next_state)
        # predict Q-values for ending state using the target network
        target_val = self.target_model.predict(next_state)

        for i in range(len(minibatch)):
            # correction on the Q value for the action used
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                # choose the max Q value among next actions

                target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))



        # Train the Neural Network with batches
        self.model.fit(state, target, batch_size=self.batch_size, verbose=0)

    def load(self, name):
        self.model = load_model(name)

    def save(self, name):
        self.model.save(name)

    #plot actions per episode
    pylab.figure(figsize=(18, 9))
    def PlotModel(self, score, episode):
        self.scores.append(score)
        self.episodes.append(episode)
        self.average.append(sum(self.scores[-50:]) / len(self.scores[-50:]))
        pylab.plot(self.episodes, self.average, 'r')
        pylab.plot(self.episodes, self.scores, 'b')
        pylab.ylabel('Score', fontsize=18)
        pylab.xlabel('Steps', fontsize=18)
        dqn = 'DQN_'
        softupdate = ''
        dueling = ''
        if self.dqn: dqn = 'DQN_'
        if self.Soft_Update: softupdate = '_soft'
        if self.dueling: dueling = '_Dueling'
        try:
            pylab.savefig(dqn+self.env_name+softupdate+dueling+".png")
        except OSError:
            pass

        return str(self.average[-1])[:5]

    def run(self):
        for e in range(self.EPISODES):

            reset_arrays = self.env.reset_array()
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            print("State with reshape",state)
            done = False
            i = 0
            while not done:

                action = self.act(state)
                print("My action",action)
                next_state, reward, done, _ = self.env.step(action)
                total_reward = reward
                next_state = np.reshape(next_state, [1, self.state_size])
                print("My next state",next_state)
                if not done or i == self.env._max_episode_steps-1:
                    reward = reward
                    print("My reward",reward)
                else:
                    done = True
                self.remember(state, action, reward, next_state, done)
                state = next_state
                print("My_state",state)
                i += 1
                if done:
                    # every step update target model
                    self.update_target_model()

                    # every episode, plot the result
                    average = self.PlotModel(i, e)

                    print("episode: {}/{}, score: {}, e: {:.2}, average: {}".format(e, self.EPISODES, i, self.epsilon, average))
                    if i == self.env._max_episode_steps:
                        print("Saving trained model as", self.Model_name)

                        break
                self.replay()



if __name__ == "__main__":

    env_name = 'TestCustomEnv-v1'
    agent = DQNAgent(env_name)
    agent.run()
