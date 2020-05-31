import pygame
import numpy as np
from env import env
if __name__ == "__main__":
    run = True
    env = env(display_dimension=(600,600), fps=60)
    env.create()
    
    while run:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
        actions = env.randomAction()
        data = env.Step(actions)

        if(data[-1]):
            env.reset()
    