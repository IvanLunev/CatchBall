"""
Game: Catch the ball
"""
import pygame
from pygame.draw import *
from random import randint
import random
import math

pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

FPS = 30
WINDOW_x = 1000
WINDOW_y = 700
screen = pygame.display.set_mode((WINDOW_x, WINDOW_y))

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
    center_x = randint(100, WINDOW_x - 100)
    center_y = randint(100, WINDOW_y - 100)
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


class Ball:
    """
    Makes a ball
    """

    def __init__(self):
        """
        Sets:
            Ball coordinates (x, y);
            Ball radius r;
            Ball speed;
            Ball angle.
        """
        self.x = randint(100, WINDOW_x - 100)
        self.y = randint(100, WINDOW_y - 100)
        self.r = randint(10, 100)
        self.speed = randint(1, 5) * 50 / FPS
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        """
        Updates parameters
        :return: None
        :rtype: None
        """
        if self.x - self.r + self.speed * math.cos(self.angle) < 0:
            self.angle = math.pi - self.angle
        elif self.x + self.r + self.speed * math.cos(self.angle) > WINDOW_x:
            self.angle = math.pi - self.angle
        elif self.y - self.r + self.speed * math.sin(self.angle) < 0:
            self.angle = 2 * math.pi - self.angle
        elif self.y + self.r + self.speed * math.sin(self.angle) > WINDOW_y:
            self.angle = 2 * math.pi - self.angle

        self.x = self.x + self.speed * math.cos(self.angle)
        self.y = self.y + self.speed * math.sin(self.angle)

        circle(screen, BLUE, (self.x, self.y), self.r)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

Score = 0
ball = Ball()

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

    ball.update()
    # new_ball()
    draw_score(Score)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
