# Alex Kwong ask8kb
"""
dino jumping game. you die if u touch a cactus. game speeds up every time day or night changes. press space to jump.
"""

import pygame
import gamebox
import random

game_on = False  # is the game running

camera = gamebox.Camera(800, 600)  # the game window

p_width = 15  # dino dimensions
p_height = 60
c_width1 = random.randint(10, 20)  # cacti dimensions
c_height1 = random.randint(30, 60)
c_width2 = random.randint(10, 20)
c_height2 = random.randint(30, 60)
c_width3 = random.randint(10, 20)
c_height3 = random.randint(30, 60)
c_width4 = random.randint(10, 20)
c_height4 = random.randint(30, 60)
c_xpos = 450  # starting x pos of the first cactus
cactus_velocity = -8  # starting cactus velocity
dino_velocity = 14  # the dino velocity
score = 1  # starting score
gravity = 1.5  # gravity
colornum = 1  # day time when equal to 1, and night time when equal to -1
color = 'white'  # day or night time

ground = gamebox.from_color(400, 500, "black", 1000, 200)  # the ground
dino = gamebox.from_color(50, 405, "red", p_width, p_height)  # the dino
leftbar = gamebox.from_color(-50, 405, "red", 10, 800)  # cacti move when touches invisible wall

cacti = [gamebox.from_color(c_xpos, 400 - (c_height1 / 2), "green", c_width1, c_height1),
         gamebox.from_color(c_xpos + random.randint(200, 400), 400 - (c_height2 / 2), "green", c_width2, c_height2),
         gamebox.from_color(c_xpos + random.randint(400, 600), 400 - (c_height3 / 2), "green", c_width3, c_height3)]  # cacti
for cactus in cacti:  # setting the speed of each cacti
    cactus.xspeed = cactus_velocity
dino.yspeed = dino_velocity  # setting dino speed


def tick(keys):
    global game_on
    global score
    global colornum
    global color

    if game_on == True:  # if game starts, have the dino and cacti move
        dino.move_speed()
        for cactus in cacti:
            cactus.move_speed()
        score += 1  # scores increases by one every tick
    if (game_on == False) and (score != 1):  # for restarting the game after dino dies
        if pygame.K_SPACE in keys:
            dino.yspeed = 0
            score = 1  # reset score back to 1
            colornum = 1  # reset back to day time
            for cactus in cacti:  # reset cacti pos and speed
                cactus.x += random.randint(800, 1500)
                cactus.xspeed = -8
    # ------- INPUT ---------
    if pygame.K_SPACE in keys:  # starts game when space is pressed
        game_on = True

    if (pygame.K_SPACE in keys) and dino.touches(ground):  # dino jumps when spaced is pressed
        dino.yspeed -= 20
        dino.move_speed()

    # ------- Collisions ---------
    if dino.bottom_touches(ground):  # stops the dino from falling through the ground
        dino.move_to_stop_overlapping(ground)
        dino.yspeed = 0
    for cactus in cacti:  # game ends when dino touches a cactus
        if dino.touches(cactus):
            game_on = False
        if cactus.touches(leftbar):  # moves cacti to right side of screen when passed left side
            cactus.x += random.randint(800, 1500)
            cactus.width = random.randint(10, 20)
            cactus.height = random.randint(30, 60)
            cactus.y = 400 - (cactus.height / 2)
    dino.yspeed += gravity  # gravity for the dino

    if score % 200 == 0:  # changes day and night and increases cactus speed
        colornum = colornum * -1
        for cactus in cacti:
            cactus.xspeed -= 1
    if (colornum == 1) and (game_on is True):  # changing day and night
        color = 'white'
    elif (colornum == -1) and (game_on is True):
        color = 'grey'
    camera.clear(color)  # sets day or night
    camera.draw(gamebox.from_text(400, 50, str(score), 50, "red", bold=False))  # drawing the score
    camera.draw(ground)  # drawing the ground
    camera.draw(dino)  # drawing the dino
    for cactus in cacti:  # drawing the cacti
        camera.draw(cactus)
    camera.display()  # displaying stuff


ticks_per_second = 60  # 60 ticks per second

gamebox.timer_loop(ticks_per_second, tick)  # runs game
