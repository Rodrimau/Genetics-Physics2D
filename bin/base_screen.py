import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import from_pygame
import pygame
from pygame import locals
import time
import math
from shapes import Circle, Box, SubjectTriangle, Triangle


GRAY = (220, 220, 220, 100)
RED = (255, 0, 0, 200)
BLUE = (200, 50, 200, 100)
GREEN = (0, 255, 0, 100)
size = w, h = 1500, 800

fps = 60


class App:
    def __init__(self, size, elements=None):
        pygame.init()

        self.space = pymunk.Space()
        self.size = size
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)

        self.space.gravity = 0, 9
        self.gravity = True
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        self.active_shape = None
        self.selected_shapes = []
        self.pulling = False
        self.startTime = time.time()
        self.seconds = 0
        self.springs = None

    def run(self):
        Box(self.space)
        subject1 = SubjectTriangle(self.space)
        subject1.create()
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)
                for shap in self.space.shapes:
                    if isinstance(shap, pymunk.shapes.Circle):
                        shap.body._set_angle = 0

            dt = self.clock.tick(self.fps)
            self.space.step(dt / 60)
            subject1.draw(self.screen, self.seconds)
            self.draw()
        print("QUIT")
        pygame.quit()

    def do_event(self, event):
        if event.type == locals.QUIT:
            self.running = False

        elif event.type == locals.KEYDOWN:
            if event.key in (locals.K_q, locals.K_ESCAPE):
                self.running = False

            keys = {
                locals.K_LEFT: (-1, 0),
                locals.K_RIGHT: (1, 0),
                locals.K_UP: (0, -1),
                locals.K_DOWN: (0, 1),
            }
            if event.key in keys:
                v = Vec2d(*keys[event.key])
                if self.active_shape is not None:
                    v.normalized()
                    self.active_shape.body.apply_impulse_at_world_point(
                        v * 5000, point=self.active_shape.body.position
                    )

            if event.key == locals.K_g:
                if self.gravity:
                    self.space.gravity = 0, 0
                    self.gravity = False
                    print("Gravity Off")
                else:
                    self.space.gravity = 0, 9
                    self.gravity = True
                    print("Gravity On")

            if event.key == locals.K_r:
                elements = self.space.constraints + self.space.shapes
                for e in elements:
                    self.space.remove(e)
                self.startTime = time.time()
                Box(self.space)
                subject1 = SubjectTriangle(self.space)
                subject1.create()

            if event.key == locals.K_c:
                p = from_pygame(pygame.mouse.get_pos(), self.screen)
                new_shape = Circle(p, space=self.space, radius=20, color=RED).shape
                shape, point, dist, gradient = new_shape.point_query(p)
                if dist < 0:
                    self.active_shape = new_shape

            if event.key == locals.K_t:
                p = from_pygame(pygame.mouse.get_pos(), self.screen)
                new_shape = Triangle(p, space=self.space, color=RED).shape
                shape, point, dist, gradient = new_shape.point_query(p)
                if dist < 0:
                    self.active_shape = new_shape

        elif event.type == locals.MOUSEBUTTONDOWN:
            p = from_pygame(event.pos, self.screen)
            self.active_shape = None
            for s in self.space.shapes:
                shape, point, dist, gradient = s.point_query(p)
                if dist < 0:
                    self.active_shape = s
                    self.pulling = True

                    s.body.angle = (p - s.body.position).angle

                    if locals.K_z:
                        self.selected_shapes.append(s)
                    else:
                        self.selected_shapes = []

        elif event.type == locals.MOUSEMOTION:
            self.p = event.pos

        elif event.type == locals.MOUSEBUTTONUP:
            if self.pulling:
                self.pulling = False
                b = self.active_shape.body
                p0 = b.position
                p1 = from_pygame(event.pos, self.screen)
                impulse = 100 * (p0 - p1).rotated(-b.angle)
                b.apply_impulse_at_local_point(impulse)
            pass

    def draw(self, subject=None):
        self.screen.fill(GRAY)
        self.space.debug_draw(self.draw_options)
        # Texto:
        font = pygame.font.SysFont("comicsans", 50)
        img = font.render(f"Seconds: {int(self.seconds)}", True, RED)
        self.screen.blit(img, (800, 20))
        prev_seconds = self.seconds
        self.seconds = time.time() - self.startTime
        # Start Position
        if subject:
            pygame.draw.lines(
                self.screen,
                RED,
                False,
                (Vec2d(subject.positionStart, 0), Vec2d(subject.positionStart, 900)),
                5,
            )
            springs = subject.springList
            if self.seconds > 5:
                for x in springs:
                    x.spring.joint.rest_length += 5 * math.sin(prev_seconds)
            # print(x.spring.joint.rest_length)
            subject.fit()
            # Actual Position
            pygame.draw.lines(
                self.screen,
                GREEN,
                False,
                (Vec2d(subject.positionEnd, 0), Vec2d(subject.positionEnd, 900)),
                5,
            )

        pygame.display.update()
