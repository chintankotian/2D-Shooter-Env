import pygame
display_width = 500
display_height = 400

win = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('First game')
pygame.init()

clock = pygame.time.Clock()

class Player(object):
    def __init__(self, x, y, width, height):
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
        self.hitBox = (self.x + 20, self.y, 20, 40)
        # self.bullet_velocity = 10

    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.right:
            win.blit(walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        elif self.left:
            win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(char,(self.x,self.y))
        self.hitBox = (self.x + 20, self.y + 15, 20, 45)
        pygame.draw.rect(win, (255,0,0), self.hitBox, 2)

    def step_left(self):
        if(self.x >= self.velocity):
            self.x -= self.velocity
            self.left = True
            self.right = False

    def step_right(self,display_width):
        if(self.x < display_width - self.width):
            self.x += self.velocity
            self.left = False
            self.right = True

    def halt(self):
        # self.left = False
        # self.right = False
        if(self.left):
            win.blit(walkLeft[0],(self.x,self.y))
        else:
            win.blit(walkRight[0],(self.x,self.y))

        self.walkCount = 0
    
    def jump(self):
        self.isJump = True
        self.halt()
    
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
        if(len(self.bullets) < 5):
            if(self.left):
                direction = 1
            else:
                direction = -1

            self.bullets.append(bullet(self.x + self.width/2, self.y + self.height/2, direction, self))

class bullet():
    def __init__(self,x,y,direction,player):
        self.x = x
        self.y = y
        self.direction = direction
        self.velocity = 10
        self.player = player
        
    def draw(self,win):
        global display_width
        if(self.x > 0) and (self.x < display_width):
            self.x -= self.velocity * self.direction
            pygame.draw.circle(win, (0,0,0), (int(self.x),int(self.y)), 5)
        else:
            self.player.bullets.pop(self.player.bullets.index(self))
        # else:
            # self.bullets
#Parametrs of the object
# This goes outside the while loop, near the top of the program
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

run = True

man1 = Player(0,display_height - 64,64,64)
man2 = Player(display_width - 64,display_height - 64,64,64)
# refresh state
def redrawWindow(mans,win):
    global walkCount
    win.blit(bg,(0,0))
    total_bullets = []
    for man in mans: 
        man.draw(win)
        total_bullets += man.bullets

    for shot_bullet in total_bullets:
        shot_bullet.draw(win)

    pygame.display.update()

# main loop
while run:
    clock.tick(60)
    for event in pygame.event.get():
        # print(event)
        if(event.type == pygame.QUIT):
            run = False

    keys = pygame.key.get_pressed()
    # man 1 control
    if(keys[pygame.K_LEFT]):
        man1.step_left()

    elif(keys[pygame.K_RIGHT]):
        man1.step_right(display_width)

    else:
        man1.halt()
        # pass

    # if not man1.isJump:
    if(keys[pygame.K_SPACE]):
        man1.shoot()

    if(keys[pygame.K_UP]):
        man1.jump()
    
    

    # man1.cont_jump()
    # man2.cont_jump()
    
    # man 2 control
    if(keys[pygame.K_a]):
        man2.step_left()

    elif(keys[pygame.K_d]):
        man2.step_right(display_width)

    else:
        man2.halt()

    # if not isJump:
    if(keys[pygame.K_w]):
        man2.jump()

    if(keys[pygame.K_TAB]):
        man2.shoot()

    man1.cont_jump()
    man2.cont_jump()

    redrawWindow([man1,man2],win)
    # redrawWindow(man2,win)
    

