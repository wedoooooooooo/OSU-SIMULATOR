    # brings pygame into existence
import pygame
from sys import exit
import random
pygame.init()

# 600x600 will be the resolution of the game
screen = pygame.display.set_mode((600,600))

# this will be the window's name
pygame.display.set_caption('aim 2')

# fetches a tick system (which is used later)
clock = pygame.time.Clock()

# this will set the font's type and font's size
test_font = pygame.font.Font(None, 50)

## creates a player sprite containing the image (1), fill (2) and default position (3)
class Player(pygame.sprite.Sprite):
    # we use *groups so the sprite is able to be put in zero or as many groups as we like
    def __init__(self, *groups, pos_x, pos_y):
        super().__init__(*groups)

        self.image = pygame.image.load('graphics1/blue.png').convert_alpha() # (1)
        self.image.fill('blue') # (2)
        self.rect = self.image.get_rect(center = (pos_x,pos_y)) # (3)

# puts the player sprite into a single group and sets the default location of it through pos_x and pos_y 
sprite_player = pygame.sprite.GroupSingle()
player_real = Player(sprite_player, pos_x=300, pos_y=300)

## basically the same progress as line 28-40
class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups, pos_x, pos_y):
        super().__init__(*groups)

        self.image = pygame.image.load('graphics1/ball.png').convert_alpha()
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

sprite_ball = pygame.sprite.GroupSingle()
ball_real = Ball(sprite_ball, pos_x=100, pos_y=100)

class Button(pygame.sprite.Sprite):
    def __init__(self, *groups, pos_x, pos_y, pressed_state):
        super().__init__(*groups)
        self.image = pygame.image.load(pressed_state).convert_alpha()
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

sprite_button = pygame.sprite.Group()
button = Button(sprite_button, pos_x=500, pos_y=70, pressed_state='graphics1/buttonunpressed.png')
# sets the default state of the button to a bool value (False) of a variable (toggle), in which the variable will later be toggled to activate certain behaviours
toggle = False 

## the count variable here is actually really important because it will be the integer display of the scoring system
count = 0

pygame.event.set_grab(True)

## the events below will happen during the game's runtime
while True:

    # turns the background white
    screen.fill('White')

    sprite_button.draw(screen)

    # you cant blit a font render outside of 'while True', sad
    score = test_font.render('Score: ' + str(count), True, 'black')
    # creates a rectange for that font render
    score_rect = score.get_rect(center = (300, 50))

    # displays the sprites and text that we currently need
    sprite_ball.draw(screen)
    sprite_player.draw(screen)
    screen.blit(score, score_rect)

    ## fetches the x and y pos of the ball sprite which will be used for the pos randomizer later
    for sprite in sprite_ball:
        x = sprite.rect.x
        y = sprite.rect.y

    ## events that will be trigged through a pygame event (input and such) will go under here
    for event in pygame.event.get():

        ## when the player presses ESCAPE, the game will exit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

        ## when the mouse moves, the player sprite (the square) will follow the mouse's position (updated 144 times a second)
        if event.type == pygame.MOUSEMOTION:
            player_real = Player(sprite_player, pos_x=(pygame.mouse.get_pos()[0]), pos_y=(pygame.mouse.get_pos()[1]))

        # if the player cursor collides with the button:
        if pygame.sprite.collide_rect(player_real, button):
            # if the player collides with the button and left click:
            if event.type == pygame.MOUSEBUTTONDOWN:
                ## there are two states of the button which are determined by an alternating bool value (dependent on left clicks) 
                # this is for the default state of the button (FALSE)
                if toggle:
                    toggle = False
                    button = Button(sprite_button, pos_x=500, pos_y=70, pressed_state='graphics1/buttonunpressed.png')
                    screen = pygame.display.set_mode((600,600))
                # this is for the changed state of the button (TRUE)
                else:
                    toggle = True
                    button = Button(sprite_button, pos_x=500, pos_y=70, pressed_state='graphics1/buttonpressed.png')
                    # changes window size
                    screen = pygame.display.set_mode((750,600))

        ## checks when the player's mouse pos (or the player sprite that follows the pos) collides with the ball/circle
        if pygame.sprite.collide_rect(player_real, ball_real):

            ## if the player's mouse pos is colliding with the ball and the game receives an X or Z input, then the following happens:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_z:

                    ## moves the ball to a random pos in the screen
                    # due to the ball sprite being exactly 100x100, the random position is limited to an area of 56x56 (7x8, 7x8) to 550x550 (55x10, 55xc10)
                    # this is to prevent some parts of the ball going off screen. (which is 600x600)
                    x = float(random.randint(7,55) * random.randint(8,10))
                    y = float(random.randint(7,55) * random.randint(8,10))

                    # the line below prints the new location of the ball, just to ensure that the janky code works xd (just uncomment to use)
                    # print("(" + str(x) + ", " + str(y) + ")")

                    # fetches the ball sprite and puts it in the new random position                    
                    for sprite in sprite_ball:
                        sprite.rect.center = (x, y)

                    # adds score after each iteration
                    count += int(1)

        # IF the player isnt colliding with the ball and still presses the key: deduct count 
        elif pygame.sprite.collide_rect(player_real, ball_real) == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_z:
                    # line 110 111 prevents negative count
                    if count <= 3:
                        count = 0
                    else:
                        count -= int(3)

    # updates the game 144 times a second 
    pygame.display.update()
    clock.tick(144)
