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

FPS = 60
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

    def __init__(self, coords):
        """
        Sets:
            Random color;
            Ball coordinates (x, y);
            Ball radius r;
            Ball speed;
            Ball angle.
        """
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.x = coords[0]
        self.y = coords[1]
        self.r = randint(25, 50)
        self.speed = randint(1, 5) * 150 / FPS
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

        self.draw()

    def draw(self):
        for k_ in range(5):
            circle(screen, self.color, (self.x, self.y), self.r * (10 - 2 * k_) / 10)
            circle(screen, BLACK, (self.x, self.y), self.r * (9 - 2 * k_) / 10)


def smash(ball_1, ball_2):
    """
    Gets two balls and makes smashing and updates angels.
    :param ball_1: Ball 1
    :type ball_1: Ball
    :param ball_2: Ball 2
    :type ball_2: Ball
    :return: None
    :rtype: None
    """
    if cross_check(
            (ball_1.x + ball_1.speed * math.cos(ball_1.angle), ball_1.y + ball_1.speed * math.sin(ball_1.angle)),
            (ball_2.x + ball_2.speed * math.cos(ball_2.angle), ball_2.y + ball_2.speed * math.sin(ball_2.angle)),
            ball_1.r + ball_2.r
    ):
        beta = math.atan((ball_1.y - ball_2.y) / (ball_1.x - ball_2.x))
        ball_1.angle = 2 * beta + math.pi - ball_1.angle
        ball_2.angle = 2 * beta + math.pi - ball_2.angle


def crossing_check(coords_, balls_):
    """
    Checks balls coordinates crossing.
    :param coords_: Coordinates list
    :type coords_: tuple
    :param balls_: Balls list
    :type balls_: list
    :return: Crossing?
    :rtype: bool
    """
    for ball_ in balls_:
        if cross_check(coords_, (ball_.x, ball_.y), ball_.r + 50):
            return True
    return False


pygame.display.update()
clock = pygame.time.Clock()
finished = False

Score = 0
n_balls = 10

balls = []
for k in range(n_balls):
    coords = (randint(100, WINDOW_x - 100), randint(100, WINDOW_y - 100))
    while crossing_check(coords, balls):
        coords = (randint(100, WINDOW_x - 100), randint(100, WINDOW_y - 100))
    balls.append(Ball(coords))

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if cross_check(event.pos, (ball.x, ball.y), ball.r):
                    Score += 1
                    draw_score(Score)

                    coords = (randint(100, WINDOW_x - 100), randint(100, WINDOW_y - 100))
                    while crossing_check(coords, balls):
                        coords = (randint(100, WINDOW_x - 100), randint(100, WINDOW_y - 100))
                    ball.__init__(coords)

    for i in range(n_balls):
        for j in range(i + 1, n_balls):
            smash(balls[i], balls[j])
    for ball in balls:
        ball.update()
    draw_score(Score)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
