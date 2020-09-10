import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import math
import pygame
from pygame.locals import *
import time
import math
import random
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
class App:
    def __init__(self, size, elements=None):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.space = pymunk.Space()
        self.space.gravity = 0, -900
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        self.active_shape = None
        self.selected_shapes = []
        self.pulling = False
        self.gravity = False
        self.startTime = time.time()
        self.seconds = 0
        self.springs = None
        self.fps = 60


    def run(self):
        Box(self.space)
        subject1 = None
        subject1 = subject(self.space)
        subject1.create()
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)
            
            self.draw(subject1)
            dt = self.clock.tick(self.fps)
            self.space.step(dt/1000)

        pygame.quit()

    def do_event(self, event):
        if event.type == QUIT:
            self.running = False

        elif event.type == KEYDOWN:
            if event.key in (K_q, K_ESCAPE):
                self.running = False
            
            keys = {K_LEFT: (-1, 0), K_RIGHT: (1, 0),
                    K_UP: (0, 1), K_DOWN: (0, -1)}
            if event.key in keys:
                v = Vec2d(keys[event.key]) 
                if self.active_shape != None:
                        v.normalized()
                        self.active_shape.body.apply_impulse_at_world_point(v*50000,point=self.active_shape.body.position)     

            if event.key == K_h:
                if self.gravity:
                    self.space.gravity = 0, 0
                else:
                    self.space.gravity = 0, -900

            if event.key == K_r:
                self.space.remove(self.space.constraints + self.space.shapes)
                self.startTime = time.time()             
                self.run()

            if event.key == K_c:
                p = from_pygame(pygame.mouse.get_pos(), self.screen)
                new_circle = Circle(p,space = self.space,color = RED, radius=20).shape
                dist, info = new_circle.point_query(p)
                if dist < 0:
                    self.active_shape = new_circle

        elif event.type == MOUSEBUTTONDOWN:
            p = from_pygame(event.pos, self.screen)
            self.active_shape = None
            for s in self.space.shapes:
                dist, info = s.point_query(p)
                if dist < 0:
                    self.active_shape = s
                    self.pulling = True

                    s.body.angle = (p - s.body.position).angle

                    if K_z:
                        self.selected_shapes.append(s)
                    else:
                        self.selected_shapes = [] 
                        
        elif event.type == MOUSEMOTION:
            self.p = event.pos

        elif event.type == MOUSEBUTTONUP:
            if self.pulling:
                self.pulling = False
                b = self.active_shape.body
                p0 = Vec2d(b.position)
                p1 = from_pygame(event.pos, self.screen)
                impulse = 100 * Vec2d(p0 - p1).rotated(-b.angle)
                b.apply_impulse_at_local_point(impulse)
            pass

    def draw(self, subject):
        self.screen.fill(GRAY)
        self.space.debug_draw(self.draw_options)
        # Texto:
        font = pygame.font.SysFont("comicsans", 50)
        img = font.render(f"Seconds: {int(self.seconds)}", True, RED)
        self.screen.blit(img, (800,20))
        prev_seconds = self.seconds
        self.seconds = ((time.time() - self.startTime))
        # Start Position
        pygame.draw.lines(self.screen ,RED ,  False,(Vec2d(subject.positionStart,0) ,Vec2d(subject.positionStart,900)) , 5)
        springs = subject.springList
        if self.seconds>5:
            for x in springs:
                x.spring.joint.rest_length += 5*math.sin(prev_seconds) 
        # print(x.spring.joint.rest_length)
        subject.fit()
        # Actual Position
        pygame.draw.lines(self.screen ,GREEN ,  False,(Vec2d(subject.positionEnd,0) ,Vec2d(subject.positionEnd,900)) , 5)

        pygame.display.update()


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


if __name__ == '__main__':

    app = App(size)

    space = app.space
    # a1 = Vec2d(200,100)
    # a2 =Vec2d(500,100)
    # b1 = Circle(pos = a1, space = space,radius=30)
    # b2 = Circle(pos = a2, space = space,radius=30)
    # print((b2.body.position - b1.body.position))
    # GrooveJoint(b1.body, b2.body, space,a1=1.5*(b2.body.position- b1.body.position),a2=0.5*(b2.body.position- b1.body.position),anchor_b=(0,0))
    # GrooveJoint(b2.body, b1.body, space,a2=1.5*(b1.body.position- b2.body.position),a1=0.5*(b1.body.position- b2.body.position),anchor_b=(0,0))


    
    app.run()
