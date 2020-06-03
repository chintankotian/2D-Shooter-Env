# A 2 player 2D shooter game in pygame

Reference - [Tech with Tim](https://www.youtube.com/watch?v=i6xMBig-pP4&list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5)
## Installing Dependencies
```bash

pip install -r requirements.txt

```
## Basic Enviroment usage

 The followig code creates an env and takes random actions

```python
from env import env
run = True
    env = env(display_dimension=(600,600), fps=60)
    env.create()
    state = env.reset()
    print('Initial state = ',state)
    while run:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
        actions = env.randomAction()
        state = env.Step(actions)
        if(state[-1]):
            print("-"*10 + 'ENV RESET' + "-"*10)
            state = env.reset()  

```

## Play the game 

You can try out the game by yourself

```bash

python main.py --player1 human --player2 human

```
player1 and player2 can be human or bot

### Controls


#### Player 1 Control
* LEFT  - Left Arrow
* Right - Right Arrow
* Jump  - Up Arrow
* Shoot - Right Control

#### Player 2 Control
* LEFT  - A
* Right - D
* Jump  - W
* Shoot - Left Control

