# brings pygame into existence
import pygame
from sys import exit
pygame.init()

import math
import random

from menu import Menu
from player import Player
from ball import Ball
from button import Button
from text import Text

# 600x600 will be the resolution of the game
screen = pygame.display.set_mode((600,600))

# this will be the window's name
pygame.display.set_caption('aim 2')

# fetches a tick system (which is used later)
clock = pygame.time.Clock()

# test_font is the "Score: x" text and the upgrade_font is for the cost label in 
test_font = pygame.font.Font(None, 50)
upgrade_font = pygame.font.Font(None, 30)

# puts the player sprite into a single group and sets the default location of it through pos_x and pos_y. 
sprite_player = pygame.sprite.GroupSingle()
player_real = Player(sprite_player, pos_x=300, pos_y=300)

sprite_ball = pygame.sprite.GroupSingle()
ball_real = Ball(sprite_ball, pos_x=300, pos_y=300)

sprite_button = pygame.sprite.Group()
button = Button(sprite_button, pos_x=500, pos_y=70, pressed_state='graphics1/buttonunpressed.png')
# sets the default state of the button to a bool value (False) of a variable (toggle), in which the variable will later be toggled to activate certain behaviours.
toggle = False 

## this will define the Upgrade menu sprite group, which contains all fixed graphics of the menu (eg the background/ upgrade text). 
sprite_menuGUI = pygame.sprite.Group()
menuGUI = Menu(sprite_menuGUI, pos_x=725, pos_y=300, graphic='upgrademenu/popoutmenu1.png')
upgrade_icon = Menu(sprite_menuGUI, pos_x=725, pos_y=50, graphic='upgrademenu/upgrade.png')

## there will be three variables assigned to each upgrade button: the main title sprite, the buy button sprite, and its cost (-x score).
value_upgrade_title = Menu(sprite_menuGUI, pos_x=725, pos_y=100, graphic='upgrademenu/value_upgrade.png')
value_upgrade_buybutton = Menu(sprite_menuGUI, pos_x=775, pos_y=150, graphic='upgrademenu/buy_value.png')

# the player owns 0 value upgrades by default
owned_value = 0

# the first step in the value upgrade will cost 10 score; the default gain (which will be increased through this update) is 1.
gain = 1
cost = 10

## the count variable here is actually really important because it will be the integer display of the scoring system.
count = 0

sprite_text = pygame.sprite.Group()
score_text = Text(sprite_text, font_size=50, text='Score: ' + str(round(count, 1)), color='black', pos_x=300, pos_y=50)

# locks the cursor inside the main game window
pygame.event.set_grab(True)

## the events below will happen during the game's runtime.
while True:

    ## fetches the x and y pos of the ball sprite which will be used for the pos randomizer later.
    for sprite in sprite_ball:
        x = sprite.rect.centerx
        y = sprite.rect.centery

    ### for every value upgrade from the 2nd step onwards, calculate the upgrade's cost: 10 * (1.14 ^ number of owned upgrades).
    if int(owned_value) > 0:
        cost = round(float(10 * math.pow(1.14, int(owned_value))), 1)
    
    ## the game will draw out the main background first because it underlaps **EVERYTHING ELSE**.
    # turns the background white
    screen.fill('white')

    # draws a line from the position the cursor to the center of the circle/ball's current position - iterates every frame.
    # layered over the white background but under the upgrade button to avoid awkward overlap.
    pygame.draw.line(screen, 'pink', (x, y), pygame.mouse.get_pos(), 4)

### the lines below up until 'for event in pygame.event.get():' draws out the sprites and text that the game currently needs.
    # draws out the sprite in order of the line number
    sprite_ball.draw(screen)
    sprite_menuGUI.draw(screen)
    sprite_button.draw(screen)

    sprite_text.draw(screen)
    ##  defines text content to later be blit (cant be done outside of while True, otherwise the content of the text wont be iterately updated).
    # score = test_font.render('Score: ' + str(round(count, 1)), True, 'black')
    # score_rect = score.get_rect(center = (300, 50))

    gain_text = test_font.render('Gain: ~ ' + str(round(float(gain), 2)) + ' /circle', True, 'black')
    gain_text_rect = gain_text.get_rect(center = (300, 80))

    vupgrade_cost = upgrade_font.render('COST: ' + str(cost) , True, 'white')
    vupgrade_cost_rect = vupgrade_cost.get_rect(center = (690, 150))

    # bliting every text rect onto the screen
    # screen.blit(score, score_rect)
    screen.blit(gain_text, gain_text_rect)
    screen.blit(vupgrade_cost, vupgrade_cost_rect)

    # the player sprite has the highest sprite order priority because it will overlap **EVERYTHING ELSE** - thus being the last sprite drawn.
    sprite_player.draw(screen)

### events in the for condition below are those that will be trigged through a pygame event (input and such).
### the if condititions below will be reserved for GENERAL SETUP
    for event in pygame.event.get():
        ## when the player presses ESCAPE, the game will exit.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

        ## when the mouse moves, the player sprite (the square) will follow the mouse's position (updated 144 times a second).
        if event.type == pygame.MOUSEMOTION:
            player_real = Player(sprite_player, pos_x=(pygame.mouse.get_pos()[0]), pos_y=(pygame.mouse.get_pos()[1]))

### the if condititions below will be reserved for GENERAL COLLISION CHECKS

        # if the player cursor collides with the button:
        if pygame.sprite.collide_rect(player_real, button):
            # if the player collides with the button and left click:
            if event.type == pygame.MOUSEBUTTONDOWN:
                ## there are two states of the button which are determined by an alternating bool value (dependent on left clicks).
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
                    screen = pygame.display.set_mode((850,600))

        ## checks when the player's mouse pos (or the player sprite that follows the pos) collides with the ball/circle.
        if pygame.sprite.collide_rect(player_real, ball_real):
            ## if the player's mouse pos is colliding with the ball and the game receives an X or Z input, then the following happens:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_z:

                    ## moves the ball to a random pos in the screen
                    # due to the ball sprite being exactly 100x100, the random position is limited to an area of 56x56 (7x8, 7x8) to 550x550 (55x10, 55xc10)
                    # this is to prevent some parts of the ball going off screen. (which is 600x600)
                    x = float(random.randint(7,55) * random.randint(8,10))
                    y = float(random.randint(7,55) * random.randint(8,10))

                    # the line below prints the new location of the ball, just to ensure that the janky code works xd. (just uncomment to use)
                    # print("(" + str(x) + ", " + str(y) + ")")

                    # fetches the ball sprite and puts it in the new random position.                  
                    for sprite in sprite_ball:
                        sprite.rect.center = (x, y)

                    # adds score after each iteration
                    count += float(gain)

        # IF the player isnt colliding with the ball and still presses the key: deduct count.
        elif pygame.sprite.collide_rect(player_real, ball_real) == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_z:
                    # line 110 111 prevents negative count
                    if count <= 3:
                        count = 0
                    else:
                        count -= int(3)

### the if condititions below will be reserved for SPECIFIC UPGRADE COLLISION CHECKS

        ## checks when the player is hovering over the value upgrade button
        if pygame.sprite.collide_rect(player_real, value_upgrade_buybutton):
            if event.type == pygame.MOUSEBUTTONDOWN and count >= cost:
                count = float(count) - float(cost)
                gain = float(gain) * 1.12
                owned_value = int(owned_value) + 1

    # updates the game 144 times a second. 
    pygame.display.update()
    clock.tick(144)
