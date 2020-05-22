import pygame


class env(object):
    def __init__(self, display_dimension = (500,400)):
        self.display_width = display_dimension[0]
        self.display_height = display_dimension[1]
        self.players = []
        self.walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
        self.walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
        self.bg = pygame.image.load('images/bg.jpg')
        self.char = pygame.image.load('images/standing.png')
    
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
        self.man1.x, self.man1.y = 0,self.display_height - 64
        self.man1.score = 0
        self.man1.bullets = []

        self.man2.x, self.man2.y = self.display_width - 64,self.display_height - 64
        self.man2.score = 0
        self.man2.bullets = []

        return [[0,self.display_height - 64,self.display_width - 64,self.display_height - 64,-1,-1],[self.display_width - 64,self.display_height - 64,0,self.display_height - 64,-1,-1]]
    
    # refresh state
    def redrawWindow(self,mans,win):
        self.win.blit(self.bg,(0,0))
        total_bullets = []
        for man in mans: 
            man.draw(win)
            total_bullets += man.bullets

        for shot_bullet in total_bullets:
            self.collision(shot_bullet)
        
        for shot_bullet in total_bullets:
            shot_bullet.draw(win)

        pygame.display.update()
    
    def collision(self,bullet):
    # iterates through all the bullets and checks whether it has collided with the opponents hit box
        for player in self.players:
            if(player != bullet.player):
                if(bullet.y - bullet.radius < player.hitBox[1] + player.hitBox[3]) and (bullet.y + bullet.radius > player.hitBox[1]):
                    if(bullet.x + bullet.radius > player.hitBox[0]) and (bullet.x - bullet.radius < player.hitBox[0] + player.hitBox[2]):
                        print(bullet.player.name + " hit "+ player.name)
                        bullet.bullet_pop()
                        bullet.player.score += 1
    
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
        def __init__(self,outer, x, y, width, height, name,score_x,score_y, bullet_interval = 5):
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
            # self.halt()
        
        def cont_jump(self):
            neg = 1
            if(self.isJump):    
                neg = 1

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
        left1, right1, jump1, shoot1 = player1
        left2, right2, jump2, shoot2 = player2

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

        if(shoot1  and (self.man1.bullet_shooting_speed == 0)):
            self.man1.shoot()
        

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

        state1 = [self.man1.x,self.man1.y,-1,-1]
        state2 = [self.man2.x,self.man2.y,-1,-1]

        if(len(self.man1.bullets) > 0):
            state1[2], state1[3] = self.man1.bullets[0].x, self.man1.bullets[0].y

        if(len(self.man2.bullets) > 0):
            state2[2], state2[3] = self.man2.bullets[0].x, self.man2.bullets[0].y
                
        self.redrawWindow(self.players,self.win)
        return [state1,state2]
        # redrawWindow(man2,win)





 
if __name__ == '__main__':
    run = True
    env = env()
    env.create()
    test_reset = 0
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        test_reset += 1
        for event in pygame.event.get():
            # print(event)
            if(event.type == pygame.QUIT):
                run = False
        print(env.Step([1,1,1,1],[1,1,1,1]))

        if(test_reset > 100):
            env.reset()   
            test_reset = 0    

    
    # main loop
    # while run:
    #     clock.tick(60)
    #     for event in pygame.event.get():
    #         # print(event)
    #         if(event.type == pygame.QUIT):
    #             run = False

    #     keys = pygame.key.get_pressed()
    #     # man 1 control
    #     if(keys[pygame.K_RIGHT]):
    #         man1.step_right(display_width)


    #     elif(keys[pygame.K_LEFT]):
    #         man1.step_left()


    #     else:
    #         man1.halt()
    #         # pass

    #     if not man1.isJump:
    #         if(keys[pygame.K_UP]):
    #             man1.jump()

    #     if(keys[pygame.K_RCTRL])  and (man1.bullet_shooting_speed == 0):
    #         man1.shoot()

    #     if(keys[pygame.K_a]):
    #         man2.step_left()

    #     elif(keys[pygame.K_d]):
    #         man2.step_right(display_width)

    #     else:
    #         man2.halt()

    #     # if not isJump:
    #     if(keys[pygame.K_w]):
    #         man2.jump()

    #     if(keys[pygame.K_LCTRL]) and  (man2.bullet_shooting_speed == 0):
    #         man2.shoot()

    #     man1.cont_jump()
    #     man2.cont_jump()


    #     redrawWindow(players,win)
    #     # redrawWindow(man2,win)
        

