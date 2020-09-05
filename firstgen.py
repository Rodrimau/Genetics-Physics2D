import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import math
import pygame
from pygame.locals import *
import time
import math
import random
from PIL import Image
import random

# Space
space = pymunk.Space()
space.gravity = 0, -900
# Constant
b0 = space.static_body
size = w, h = 1800, 600
# Colors
GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (50, 50, 200)
GREEN = (0, 255, 0)
class App:
    def __init__(self, size, elements):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        self.active_shape = None
        self.selected_shapes = []
        self.pulling = False
        self.gravity = False
        self.images = []
        self.image_nbr = 60
        self.startTime = time.time()
        self.seconds = 0
        self.springs = elements

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)
            self.draw()
            dt = self.clock.tick(60)
            space.step(dt/1000)
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
                        # self.active_shape.body.position += v
                        v.normalized()
                        self.active_shape.body.apply_impulse_at_world_point(v*50)            

            if event.key == K_h:
                self.gravity = not self.gravity
                if self.gravity:
                    space.gravity = 0, 0
                else:
                    space.gravity = 0, -900

            if event.key == K_c:
                p = from_pygame(pygame.mouse.get_pos(), self.screen)
                Circle(p, radius=20)


        elif event.type == MOUSEBUTTONDOWN:
            p = from_pygame(event.pos, self.screen)
            self.active_shape = None
            for s in space.shapes:
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

    def draw(self):
        self.screen.fill(GRAY)
        space.debug_draw(self.draw_options)
        # Texto:
        font = pygame.font.SysFont("comicsans", 50)
        img = font.render(f"Seconds: {int(self.seconds)}", True, RED)
        self.screen.blit(img, (800,20))
        prev_seconds = self.seconds
        self.seconds = ((time.time() - self.startTime))
        for x in self.springs:
        # if prev_seconds!= self.seconds:
            x.joint.rest_length += 10*math.sin(5*prev_seconds)
        # print(spring.joint.rest_length)
        pygame.display.update()


class PivotJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0), collide=True):
        joint = pymunk.constraint.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        space.add(joint)

class SimpleMotor:
    def __init__(self, b, b2, rate):
        joint = pymunk.constraint.SimpleMotor(b, b2, rate)
        space.add(joint)

class SpringJoint:
    def __init__(self, b1, b2, a1 = (0, 0), a2 =(0, 0), length = 100,stif =100,damp=10):
        self.joint = pymunk.constraint.DampedSpring(b1, b2, a1, a2, length, stif, damp)
        space.add(self.joint)

class GrooveJoint:
    def __init__(self, b1, b2, a1 =(0,0), a2 =(0,0), anchor_b= (0,0)):
        joint = pymunk.constraint.GrooveJoint(b1, b2, a1, a2, anchor_b)
        joint.collide_bodies = False
        space.add(joint)


class Circle:
    id = 0
    def __init__(self, pos, radius=30,color=GRAY,friction=0.5,mass=0):
        self.id = (Circle.id + 1)
        self.body = pymunk.Body(mass=mass)
        self.body.position = pos
        shape = pymunk.Circle(self.body, radius)
        shape.density = 0.01
        shape.color = color
        shape.friction = friction
        shape.elasticity = 1
        space.add(self.body, shape)

class Box:
    def __init__(self, p0=(0, 0), p1=(w, h), d=4):
        x0, y0 = p0
        x1, y1 = p1
        ps = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(b0, ps[i], ps[(i+1) % 4], d)
            segment.elasticity = 0.5
            segment.friction = 1
            space.add(segment)

class Floor:
    def __init__(self, p0=(-200, 0), p1=(w+200,), d=10):
        segment = pymunk.Segment(b0, p0 , p1, d)
        segment.elasticity = 0.5
        segment.friction = 1
        space.add(segment)

def sampleInit():
    # Defino cantidad de Nodes
    nodes = 2+random.randint(1,5)
    nodesList =[]
    for _ in range(nodes):
        nodesList.append(Circle((900+random.randint(0,50), 100+random.randint(0,50)),color =(255,0,255), friction = 10*random.random(),mass=random.randint(0,100),radius=random.randint(10, 30)))
    springs = random.randint((nodes)-1,sum(range(nodes)))
    springsList =[]
    springCombination =[]
    for x in range(nodes):
        for y in range(nodes):
            springCombination.append((x,y))
    springCombinationClean = []
    for i in [list(set(x)) for x in springCombination if  x != x[::-1]]:
        if i not in springCombinationClean:
            springCombinationClean.append(i)    
    for i in range(springs):
        c1 = random.randint(0,len(springCombinationClean)-1)
        w1 = springCombinationClean[c1][0]
        w2 = springCombinationClean[c1][1]
        springsList.append(SpringJoint( nodesList[w1].body, nodesList[w2].body,  length = 20+random.randint(0,200),stif=50+random.randint(0,50)))
        springCombinationClean.remove(springCombinationClean[c1])
    return springsList

if __name__ == '__main__':
    Floor()
    
    springsList = sampleInit()

    print(space._constraints)
    App(size,springsList).run()
