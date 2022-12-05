import pygame
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import *
from pygame import locals
from shapes import Circle, Box, Subject
import time
import math

GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (200, 50, 200)
GREEN = (0, 255, 0)
size = w, h = 1600, 800
fps = 60
class App:
    def __init__(self, size, elements=None):
        pygame.init()

        self.space = pymunk.Space()
        self.size = size
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        
        self.space.gravity = 0, -900
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        self.active_shape = None
        self.selected_shapes = []
        self.pulling = False
        self.gravity = False
        self.startTime = time.time()
        self.seconds = 0
        self.springs = None

    def run(self):
        #Box(self.space)

        while self.running:
            for event in pygame.event.get():
                self.do_event(event)

            dt = self.clock.tick(self.fps)
            self.space.step(dt/60)
            self.draw()
        
        pygame.quit()

    def do_event(self, event):
        if event.type == locals.QUIT:
            self.running = False

        elif event.type == locals.KEYDOWN:
            if event.key in (locals.K_q, locals.K_ESCAPE):
                self.running = False

            if event.key == locals.K_g:
                if self.gravity:
                    self.space.gravity = 0, 0
                else:
                    self.space.gravity = 0, -900

        elif event.type == locals.MOUSEMOTION:
            self.p = event.pos
            print(self.p )

    def draw(self):
        self.screen.fill(GRAY)
        self.space.debug_draw(self.draw_options)
        self.seconds = ((time.time() - self.startTime))

        # Texto:
        font = pygame.font.SysFont("comicsans", 50)
        img = font.render(f"Seconds: {int(self.seconds)}", True, RED)
        self.screen.blit(img, (500, 20))
        
        pygame.display.update()