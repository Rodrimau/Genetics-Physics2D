import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import math
import pygame
from pygame.locals import *
import time
import math
import random

from itertools import combinations
import statistics

# Constant
# b0 = space.static_body
size = w, h = 2700, 800
# Colors
GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (200, 50, 200)
GREEN = (0, 255, 0)




class PivotJoint:
    def __init__(self, b, b2, space, a=(0, 0), a2=(0, 0), collide=True):
        self.joint = pymunk.constraint.PinJoint(b, b2, a, a2)
        self.joint.collide_bodies = collide
        space.add(self.joint)

class SimpleMotor:
    def __init__(self, b, b2, rate, space):
        self.joint = pymunk.constraint.SimpleMotor(b, b2, rate)
        space.add(self.joint)

class SpringJoint:
    def __init__(self, b1, b2, space, a1 = (0, 0), a2 =(0, 0), length = 100,stif =100,damp=0,grooved=0 ):
        self.joint = pymunk.constraint.DampedSpring(b1, b2, a1, a2, length, stif, damp)
        self.joint.collide_bodies = False
        space.add(self.joint)

class GrooveJoint:
    def __init__(self, b1, b2, space , a1 =(0,0), a2 =(0,0), anchor_b= (0,0)):
        self.joint = pymunk.constraint.GrooveJoint(b1, b2, a1, a2, anchor_b)
        self.joint.collide_bodies = False
        space.add(self.joint)

class TSpringJoint:
    def __init__(self, b1, b2, space, a1 = Vec2d(0, 0), a2 =Vec2d(0, 0), length = 100,stif =100,damp=1000,max_length=2, min_length = 0.5,grooved =True ):
        
        if grooved:
            groovedWich = random.randint(1,2)
            # groovedWich = 1

            if groovedWich==1:
                self.groove1 = GrooveJoint(b1, b2, space, a1=length*max_length*(b2.position- b1.position).normalized(), a2=length*min_length*(b2.position - b1.position).normalized(),anchor_b=(0,0))
            if groovedWich==2:
                self.groove2 = GrooveJoint(b2, b1, space, a2=length*max_length*(b1.position- b2.position).normalized(), a1=length*min_length*(b1.position- b2.position).normalized(),anchor_b=(0,0))
            if groovedWich==3:
                self.groove2 = GrooveJoint(b2, b1, space, a2=length*max_length*(b1.position- b2.position).normalized(), a1=length*min_length*(b1.position- b2.position).normalized(),anchor_b=(0,0))
                self.groove1 = GrooveJoint(b1, b2, space, a1=length*max_length*(b2.position- b1.position).normalized(), a2=length*min_length*(b2.position - b1.position).normalized(),anchor_b=(0,0))
        self.spring = SpringJoint(b1,b2, space,length=length)




class Circle:
    id = 0
    def __init__(self, pos, space , radius=30,color=GREEN,friction=0.5,mass=0.01):
        self.id = (Circle.id + 1)
        self.body = pymunk.Body(mass=mass)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 0.1
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
            segment = pymunk.Segment(space.static_body, ps[i], ps[(i+1) % 4], d)
            segment.elasticity = 0
            segment.friction = 0.5
            space.add(segment)

class Floor:
    def __init__(self, space , p0=(-200, 0), p1=(w+200,), d=10):
        segment = pymunk.Segment(space.static_body, p0 , p1, d)
        segment.elasticity = 0.5
        segment.friction = 0.9
        space.add(segment)

class subject:
    def __init__(self, space ):
        self.nodes = 2+random.randint(1,3)
        self.springs = random.randint((self.nodes)-1,sum(range(self.nodes)))
        self.positionStart = 0
        self.positionEnd = 0
        self.fitness =  0
        self.space = space
        
    def create(self):
        # Defino cantidad de Nodes
        nodesList =[]
        for _ in range(self.nodes):
            nodesList.append(Circle((500+random.randint(0,400), 100+random.randint(0,400)),
            color =(200,100,255), 
            friction = random.random(),
            radius=random.randint(15, 50),
            space = self.space ))
        springsList =[]
        springsCombination=[i for i in combinations(list(range(self.nodes)),2)]
        for _ in range(self.springs):
            # Elijo Spring al azar c1 entre los nodos w1 y w2
            s1 = random.randint(0,len(springsCombination)-1)
            n1 = springsCombination[s1][0]
            n2 = springsCombination[s1][1]
            springsList.append(TSpringJoint( nodesList[n1].body, nodesList[n2].body,  
            length = 200+random.randint(0,0),
            stif = 10000+random.randint(0,100),
            damp= 10000,
            space = self.space ,

            grooved=1))
            springsCombination.remove(springsCombination[s1])
        self.nodesList = nodesList
        self.springList = springsList
        self.positionStart = statistics.mean([x.body.position[0] for x in self.nodesList])
        print(self.nodes , self.springs)

    def fit(self):
        self.positionEnd =  statistics.mean([x.body.position[0] for x in self.nodesList])
        self.fitness = self.positionEnd - self.positionStart
        return self.fitness


