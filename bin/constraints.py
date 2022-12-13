import pymunk
from pymunk.vec2d import Vec2d
import random


class PivotJoint:
    def __init__(self, b, b2, space, a=(0, 0), a2=(0, 0), collide=True):
        self.joint = pymunk.PinJoint(b, b2, a, a2)
        self.joint.collide_bodies = collide
        space.add(self.joint)


class SimpleMotor:
    def __init__(self, b, b2, rate, space):
        self.joint = pymunk.SimpleMotor(b, b2, rate)
        space.add(self.joint)


class SpringJoint:
    def __init__(self, b1, b2, space, a1=(0, 0), a2=(0, 0), length=100, stif=100, damp=0):
        self.joint = pymunk.DampedSpring(b1, b2, a1, a2, length, stif, damp)
        self.joint.collide_bodies = False
        space.add(self.joint)


class GrooveJoint:
    def __init__(self, b1, b2, space, a1=(0, 0), a2=(0, 0), anchor_b=(0, 0)):
        self.joint = pymunk.GrooveJoint(b1, b2, a1, a2, anchor_b)
        self.joint.collide_bodies = False
        space.add(self.joint)


class TSpringJoint:
    def __init__(self, b1, b2, space, a1=Vec2d(0, 0), a2=Vec2d(0, 0), length=100, stif=100, damp=1000, max_length=2, min_length=0.5, grooved=True):

        if grooved:
            groovedWich = random.randint(1, 1)
            groovedWich = 2

            if groovedWich == 1:
                self.groove1 = GrooveJoint(b1, b2, space, a1=length * max_length * (b2.position - b1.position).normalized(), a2=length * min_length * (b2.position - b1.position).normalized(), anchor_b=(0, 0))
            if groovedWich == 2:
                self.groove2 = GrooveJoint(b2, b1, space, a2=length * max_length * (b1.position - b2.position).normalized(), a1=length * min_length * (b1.position - b2.position).normalized(), anchor_b=(0, 0))
            if groovedWich == 3:
                self.groove2 = GrooveJoint(b2, b1, space, a2=length * max_length * (b1.position - b2.position).normalized(), a1=length * min_length * (b1.position - b2.position).normalized(), anchor_b=(0, 0))
                self.groove1 = GrooveJoint(b1, b2, space, a1=length * max_length * (b2.position - b1.position).normalized(), a2=length * min_length * (b2.position - b1.position).normalized(), anchor_b=(0, 0))
        self.spring = SpringJoint(b1, b2, space, length=length, stif=stif, damp=damp)

