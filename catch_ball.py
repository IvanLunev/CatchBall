"""
Game: Catch the ball
"""
import pygame
from pygame.draw import *
from random import randint

pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

FPS = 1
screen = pygame.display.set_mode((1000, 700))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    Draws a ball.
    :return: None
    :rtype: None
    """
    global center_x, center_y, radius
    center_x = randint(100, 900)
    center_y = randint(100, 600)
    radius = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (center_x, center_y), radius)


def click(event):
    """
    Returns circle coordinates.
    :param event: Event on the screen
    :type event: MOUSEBUTTONDOWN
    :return: None
    :rtype: None
    """
    print(cross_check(event.pos, (center_x, center_y), radius))


def cross_check(dot1, dot2, rad):
    """
    Checks dot1 in circle with center dot2 and radius rad.
    :param dot1: coordinates of the point
    :type dot1: tuple
    :param dot2: center coordinates
    :type dot2: tuple
    :param rad: radius
    :type rad: float
    :return: In circle?
    :rtype: bool
    """
    dist = ((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2) ** (1 / 2)
    return dist < rad


def draw_score(score):
    """
    Draws score.
    :param score: Score
    :type score: float
    :return: None
    :rtype: None
    """
    textsurface = myfont.render('Your Score: ' + str(score), False, BLACK)
    screen.blit(textsurface, (20, 20))
    textsurface = myfont.render('Your Score: ' + str(score), False, WHITE)
    screen.blit(textsurface, (20, 20))


pygame.display.update()
clock = pygame.time.Clock()
finished = False
Score = 0
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if cross_check(event.pos, (center_x, center_y), radius):
                Score += 1
                draw_score(Score)
            click(event)

    new_ball()
    draw_score(Score)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
