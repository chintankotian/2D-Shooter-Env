import pygame


class env(object):
    def __init__(self, display_dimension = (500,400),fps = 30):
        self.display_width = display_dimension[0]
        self.display_height = display_dimension[1]
        self.players = []
        self.walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
        self.walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
        self.bg = pygame.image.load('images/bg.jpg')
        self.bg = pygame.transform.scale(self.bg,display_dimension)
        self.char = pygame.image.load('images/standing.png')
        self.reset_state = False
        self.frame_count = 0
        self.fps = fps

    
    def getDisplayDim(self):
        return (self.display_width,self.display_height)

    def create(self):
        self.win = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('AI shooter')
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.man1 = self.getPlayer(0,self.display_height - 64,64,64, 'player-1', 10, 10)
        self.man2 = self.getPlayer(self.display_width - 64,self.display_height - 64,64,64, 'player-2', 390, 10)
        state = [[0,self.display_height - 64,self.display_width - 64,self.display_height - 64,-1,-1],[self.display_width - 64,self.display_height - 64,0,self.display_height - 64,-1,-1]]
        return state

    def reset(self):
        self.reset_state = False

        self.man1.x, self.man1.y = 0,self.display_height - 64
        self.man1.score = 0
        self.man1.bullets = []
        self.man1.isJump = False
        self.man1.left = False    
        self.man1.right = False
        self.man1.jumpCount = 10

        self.man2.x, self.man2.y = self.display_width - 64,self.display_height - 64
        self.man2.score = 0
        self.man2.bullets = []
        self.man2.isJump = False
        self.man2.left = False    
        self.man2.right = False
        self.man2.jumpCount = 10


        return [[0,self.display_height - 64,self.display_width - 64,self.display_height - 64,-1,-1],[self.display_width - 64,self.display_height - 64,0,self.display_height - 64,-1,-1]]
    
    # refresh state
    def redrawWindow(self,mans,win,collision_detect = True):
        self.win.blit(self.bg,(0,0))
        total_bullets = []
        winner_player = []

        for man in mans: 
            man.draw(win)
            total_bullets += man.bullets

        
        for shot_bullet in total_bullets:
            shot_bullet.draw(win)

        if(collision_detect):
            for shot_bullet in total_bullets:
                winner_player += self.collision(shot_bullet)
            # print(winner_player)
        
        pygame.display.update()
        return winner_player
        
    
    def collision(self,bullet):
    # iterates through all the bullets and checks whether it has collided with the opponents hit box
        winners = []
        for player in self.players:
            if(player != bullet.player):
                if(bullet.y - bullet.radius < player.hitBox[1] + player.hitBox[3]) and (bullet.y + bullet.radius > player.hitBox[1]):
                    if(bullet.x + bullet.radius > player.hitBox[0]) and (bullet.x - bullet.radius < player.hitBox[0] + player.hitBox[2]):
                        print(bullet.player.name + " hit "+ player.name)
                        print('bullet co-ord = ',bullet.x,bullet.y)
                        print('player co-ord = ',player.x,player.y)
                        # print('hello')
                        bullet.bullet_pop()
                        bullet.player.score += 1
                        winners.append(bullet.player)
        return winners
    
    class bullet(object):
        def __init__(self,outer,x,y,direction,player):
            self.x = x
            self.y = y
            self.direction = direction
            self.velocity = 10
            self.player = player
            self.radius = 5
            self.outer = outer
            
        def bullet_pop(self):
            self.player.bullets.pop(self.player.bullets.index(self))

        def draw(self,win):
            if(self.x > 0) and (self.x < self.outer.display_width):
                self.x -= self.velocity * self.direction
                pygame.draw.circle(win, (0,0,0), (int(self.x),int(self.y)), self.radius)
            else:
                self.bullet_pop()

    def getBullet(self,x,y,direction,player):
        return self.bullet(self, x, y, direction, player)

    def getPlayer(self,x, y, width, height, name,score_x,score_y):
        return self.Player(self, x, y, width, height, name, score_x, score_y)



    class Player(object):
        def __init__(self,outer, x, y, width, height, name,score_x,score_y, bullet_interval = 1):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.velocity = 1
            self.isJump = False
            self.left = False    
            self.right = False
            self.walkCount = 0
            self.jumpCount = 10
            self.bullets = []
            self.outer = outer
            outer.players.append(self)
            self.hitBox = (self.x + 20, self.y, 20, 40)
            self.name = name
            self.bullet_interval = bullet_interval
            self.bullet_shooting_speed = 1
            self.font = pygame.font.SysFont('comicsans', 20, True)
            self.score = 0
            self.score_x = score_x
            self.score_y = score_y
            self.name_font = pygame.font.SysFont('comicsans', 10, True)
            self.reward = 0

            # self.bullet_velocity = 10

        def draw(self,win):
            text = self.font.render(self.name +" = "+ str(self.score), 1, (0, 0, 0))
            win.blit(text, (self.score_x, self.score_y))
            text = self.font.render(self.name, 1, (0, 0, 0))
            win.blit(text, (self.x, self.y))

            if(self.bullet_shooting_speed > 0):
                self.bullet_shooting_speed += 1
            
            if(self.bullet_shooting_speed > self.bullet_interval):
                self.bullet_shooting_speed = 0
            
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if self.right:
                win.blit(self.outer.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1

            elif self.left:
                win.blit(self.outer.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount += 1

            else:
                win.blit(self.outer.char,(self.x,self.y))

            self.hitBox = (self.x + 20, self.y + 15, 20, 45)
            pygame.draw.rect(win, (255,255,0), self.hitBox, 2)

        def step_left(self):
            if(self.x >= self.velocity):
                self.x -= self.velocity
                self.left = True
                self.right = False

        def step_right(self):
            if(self.x < self.outer.display_width - self.width):
                self.x += self.velocity
                self.left = False
                self.right = True

        def halt(self,win):
            # self.left = False
            # self.right = False
            if(self.right):
                win.blit(self.outer.walkRight[0],(self.x,self.y))
            elif(self.left):
                win.blit(self.outer.walkLeft[0],(self.x,self.y))

            self.walkCount = 0
        
        def jump(self):
            self.isJump = True
        
        def cont_jump(self):
            neg = 1
            if(self.isJump):    
                neg = 1
                # print('inside is cont jump')

                if self.jumpCount < 0:
                    neg = -1

                if self.jumpCount >= -10:
                    self.y -= (self.jumpCount**2)*0.5*neg
                    self.jumpCount -= 1

                else:
                    self.isJump = False
                    self.jumpCount = 10

        def shoot(self):
            if(len(self.bullets) < 1):
                self.bullet_shooting_speed = 1
                if(self.right):
                    direction = -1
                else:
                    direction = 1

                self.bullets.append(self.outer.getBullet(self.x + self.width/2, self.y + self.height/2, direction, self))

    def Step(self,player1,player2):
        self.clock.tick(self.fps)
        self.frame_count += 1
        print(self.frame_count)
        left1, right1, jump1, shoot1 = player1
        left2, right2, jump2, shoot2 = player2
        self.man1.reward = -1
        self.man2.reward = -1

        #  man 1 control
        if(right1):
            self.man1.step_right()


        elif(left1):
            self.man1.step_left()


        else:
            self.man1.halt(self.win)
            # pass

        if not self.man1.isJump:
            if(jump1):
                self.man1.jump()
        print((self.man1.bullet_shooting_speed == 0))
        if(shoot1  and (self.man1.bullet_shooting_speed == 0)):
            self.man1.shoot()
            print('shooot')
        
        # man 2 controls
        if(left2):
            self.man2.step_left()

        elif(right2):
            self.man2.step_right()

        else:
            self.man2.halt(self.win)

        # if not isJump:
        if(jump2):
            self.man2.jump()

        if(shoot2 and  (self.man2.bullet_shooting_speed == 0)):
            self.man2.shoot()

        
        self.man1.cont_jump()
        self.man2.cont_jump()

        state1 = [[self.man1.x,self.man1.y,-1,-1],self.man1.reward]
        state2 = [[self.man2.x,self.man2.y,-1,-1],self.man2.reward]

        if(len(self.man1.bullets) > 0):
            state1[0][2], state1[0][3] = self.man2.bullets[0].x, self.man2.bullets[0].y

        if(len(self.man2.bullets) > 0):
            state2[0][2], state2[0][3] = self.man1.bullets[0].x, self.man1.bullets[0].y
                
        winners = self.redrawWindow(self.players,self.win)
        if(len(winners)):
            if(len(winners) > 1):
                self.man1.reward += 26
                self.man2.reward += 26
            else:
                winners[0].reward += 51

            self.reset_state = True
            
        
        state1[-1] = self.man1.reward
        state2[-1] = self.man2.reward


        return [state1,state2,self.reset_state]
        # redrawWindow(man2,win)





 
if __name__ == '__main__':
    run = True
    env = env(display_dimension=(600,100), fps=60)
    env.create()
    while run:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False

        data = env.Step([1,1,0,1],[1,1,1,1])
        
        if(data[-1]):
            env.reset()   
