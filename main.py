import pygame
import numpy as np
from env import env
# import tensorflow as tf
# from tensorflow.keras import layers
# from tensorflow.keras import models
import sys, getopt

def makeModel(env):
    model = models.Sequential()
    model.add(layers.Input(shape = (6,)))
    model.add(layers.Dense(64,activation = 'relu'))
    model.add(layers.Dense(64,activation = 'relu'))
    model.add(layers.Dense(4, activation = 'sigmoid'))

    return model

def probsToDiscrete(actions):
    retActions = np.zeros_like(actions)
    for i,action in enumerate(actions):
        if(action > 0.5):
            retActions[i] = 1
    return retActions

if __name__ == "__main__":
    humanPlayer1 = False
    humanPlayer2 = False

    try:
        opts, remainder = getopt.getopt(sys.argv[1:],"ha:b:",['player1=','player2='])
    except getopt.GetoptError as ex:
        print(ex)
        print('usage : main.py -p1 human or bot -p2 human or bot')
        sys.exit(2)
    
    for opt, args in opts:
        if(opt in ('-a','--player1')):
            if(args.lower() == 'human'):
                humanPlayer1 = True
            elif(args.lower() == 'bot'):
                humanPlayer1 = False
            else:
                print('--player1 can only be human or bot')
                sys.exit(2)

        elif(opt in ('-b','--player2')):
            if(args.lower() == 'human'):
                humanPlayer2 = True
            elif(args.lower() == 'bot'):
                humanPlayer2 = False
            else:
                print('--player2 can only be human or bot')
                sys.exit(0)
    
    


    run = True
    env = env(display_dimension=(600,600), fps=60, winningScore = 5)
    state = env.create()
    # model = makeModel(env)
    while run:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
        
        actions = np.zeros_like(env.randomAction())
        if(not humanPlayer1 and not humanPlayer2):
            actions = env.randomAction()

        keys = pygame.key.get_pressed()

        if(humanPlayer1):

            if(keys[pygame.K_LEFT]):
                actions[0][0] = 1
            
            if(keys[pygame.K_RIGHT]):
                actions[0][1] = 1
            
            if(keys[pygame.K_UP]):
                actions[0][2] = 1
            
            if(keys[pygame.K_RCTRL]):
                actions[0][3] = 1
        else:
            actions[0] = env.randomAction()[0]

        if(humanPlayer2):

            if(keys[pygame.K_a]):
                actions[1][0] = 1
            
            if(keys[pygame.K_d]):
                actions[1][1] = 1
            
            if(keys[pygame.K_w]):
                actions[1][2] = 1
            
            if(keys[pygame.K_LCTRL]):
                actions[1][3] = 1
        else:
            actions[1] = env.randomAction()[1]

        state = env.Step(actions)

        if(state[-1]):
            env.reset()