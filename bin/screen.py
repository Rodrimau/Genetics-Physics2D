import pygame
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import *
from pygame.locals import *
from shapes import Circle, Box
import time
import math

GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (200, 50, 200)
GREEN = (0, 255, 0)
size = w, h = 2700, 800

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
     #   subject1 = None
    #    subject1 = Subject(self.space)
    #    subject1.create()
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)
    #        self.draw(subject1)
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
                dist = new_circle.point_query(p)
                if dist < 0:
                    self.active_shape = new_circle

        elif event.type == MOUSEBUTTONDOWN:
            p = from_pygame(event.pos, self.screen)
            self.active_shape = None
            for s in self.space.shapes:
                dist = s.point_query(p)
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
        self.screen.blit(img, (800, 20))
        prev_seconds = self.seconds
        self.seconds = ((time.time() - self.startTime))
        # Start Position
        pygame.draw.lines(self.screen, RED, False, (Vec2d(subject.positionStart,0) ,Vec2d(subject.positionStart,900)) , 5)
        springs = subject.springList
        if self.seconds>5:
            for x in springs:
                x.spring.joint.rest_length += 5*math.sin(prev_seconds) 
        # print(x.spring.joint.rest_length)
        subject.fit()
        # Actual Position
        pygame.draw.lines(self.screen ,GREEN ,  False,(Vec2d(subject.positionEnd,0) ,Vec2d(subject.positionEnd,900)) , 5)

        pygame.display.update()