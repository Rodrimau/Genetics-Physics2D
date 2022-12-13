import pymunk
import pygame
from pymunk.vec2d import Vec2d
from itertools import combinations
import statistics
import math
import random
from constraints import TSpringJoint


GRAY = (220, 220, 220, 100)
RED = (255, 0, 0, 100)
BLUE = (200, 50, 200, 100)
GREEN = (0, 255, 0, 100)
size = w, h = 1500, 800


class Circle:
    id = 0

    def __init__(self, pos, space, radius=30, color=GREEN, friction=0.5, mass=1):
        self.id = (Circle.id + 1)
        self.body = pymunk.Body(mass=mass)
        self.body.position = pos
        self.body.angle = 0
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 0.1
        self.shape.color = color
        self.shape.friction = friction
        self.shape.elasticity = 1
        space.add(self.body, self.shape)


class Triangle:
    id = 0

    def __init__(self, pos, space, color=GREEN, friction=0.5, mass=1):
        self.id = (Triangle.id + 1)
        self.body = pymunk.Body(mass=mass)
        self.body.position = pos
        self.body.angle = 0
        self.shape = pymunk.Poly(self.body, vertices=[(25, 10), (-25, 10), (0, -25)])
        self.shape.density = 1
        self.shape.color = color
        self.shape.friction = friction
        self.shape.elasticity = 1
        space.add(self.body, self.shape)


class Box:
    def __init__(self, space, p0=(0, 0), p1=(w, h), d=40):
        x0, y0 = p0
        x1, y1 = p1
        ps = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(space.static_body, ps[i], ps[(i + 1) % 4], d)
            segment.elasticity = 0
            segment.friction = 0.5
            space.add(segment)


class SubjectRound:
    def __init__(self, space):
        self.nodes = 2 + random.randint(1, 2)
        self.springs = random.randint((self.nodes) - 1, sum(range(self.nodes)))
        self.positionStart = 0
        self.positionEnd = 0
        self.fitness = 0
        self.space = space

    def create(self):
        # Defino cantidad de Nodes
        nodesList = []
        for _ in range(self.nodes):
            nodesList.append(Circle((500 + random.randint(0, 400), 100 + random.randint(0, 400)),
                                    color=BLUE,
                                    friction=random.random(),
                                    radius=random.randint(15, 50),
                                    space=self.space))
        springsList = []
        springsCombination = [i for i in combinations(list(range(self.nodes)), 2)]
        for _ in range(self.springs):
            # Elijo Spring al azar c1 entre los nodos w1 y w2
            s1 = random.randint(0, len(springsCombination) - 1)
            n1 = springsCombination[s1][0]
            n2 = springsCombination[s1][1]
            springsList.append(TSpringJoint(nodesList[n1].body, nodesList[n2].body,
                                            length=200 + random.randint(0, 0),
                                            stif=100000000 + random.randint(0, 100),
                                            damp=10000000,
                                            space=self.space,
                                            grooved=1))
            springsCombination.remove(springsCombination[s1])
        self.nodesList = nodesList
        self.springList = springsList
        self.positionStart = statistics.mean([x.body.position[0] for x in self.nodesList])
        # print(self.nodes , self.springs)

    def fit(self):
        self.positionEnd = statistics.mean([x.body.position[0] for x in self.nodesList])
        self.fitness = self.positionEnd - self.positionStart
        return self.fitness

    def draw(self, screen, screen_time):
        pygame.draw.lines(screen, RED, False, (Vec2d(self.positionStart, 0), Vec2d(self.positionStart, 900)), 5)
        springs = self.springList
        if screen_time > 5:
            for x in springs:
                x.spring.joint.rest_length += 5 * math.sin(screen_time)
        # print(x.spring.joint.rest_length)
        self.fit()
        # Actual Position
        pygame.draw.lines(screen, GREEN, False, (Vec2d(self.positionEnd, 0), Vec2d(self.positionEnd, 900)), 5)


class SubjectTriangle:
    def __init__(self, space):
        self.nodes = 2 + random.randint(1, 2)
        self.springs = random.randint((self.nodes) - 1, sum(range(self.nodes)))
        self.positionStart = 0
        self.positionEnd = 0
        self.fitness = 0
        self.space = space

    def create(self):
        # Defino cantidad de Nodes
        nodesList = []
        for _ in range(self.nodes):
            nodesList.append(Triangle((500 + random.randint(0, 400), 100 + random.randint(0, 400)),
                                      color=BLUE,
                                      friction=random.random(),
                                      space=self.space))
        springsList = []
        springsCombination = [i for i in combinations(list(range(self.nodes)), 2)]
        for _ in range(self.springs):
            # Elijo Spring al azar c1 entre los nodos w1 y w2
            s1 = random.randint(0, len(springsCombination) - 1)
            n1 = springsCombination[s1][0]
            n2 = springsCombination[s1][1]
            springsList.append(TSpringJoint(nodesList[n1].body, nodesList[n2].body,
                                            length=200 + random.randint(0, 0),
                                            stif=1000 + random.randint(0, 100),
                                            damp=100000,
                                            space=self.space,
                                            grooved=1))
            springsCombination.remove(springsCombination[s1])
        self.nodesList = nodesList
        self.springList = springsList
        self.positionStart = statistics.mean([x.body.position[0] for x in self.nodesList])
        # print(self.nodes , self.springs)

    def fit(self):
        self.positionEnd = statistics.mean([x.body.position[0] for x in self.nodesList])
        self.fitness = self.positionEnd - self.positionStart
        return self.fitness

    def draw(self, screen, screen_time):
        pygame.draw.lines(screen, RED, False, (Vec2d(self.positionStart, 0), Vec2d(self.positionStart, 900)), 5)
        springs = self.springList
        if screen_time > 5:
            for x in springs:
                x.spring.joint.rest_length += 3 * math.sin(screen_time)
        # print(x.spring.joint.rest_length)
        self.fit()
        # Actual Position
        pygame.draw.lines(screen, GREEN, False, (Vec2d(self.positionEnd, 0), Vec2d(self.positionEnd, 900)), 5)
