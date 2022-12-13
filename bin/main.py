
from base_screen import App
from pymunk.vec2d import Vec2d
from shapes import Circle
from constraints import GrooveJoint

size = w, h = 1500, 800


if __name__ == '__main__':

    app = App(size)

    space = app.space
    a1 = Vec2d(200, 100)
    a2 = Vec2d(500, 100)
    b1 = Circle(pos=a1, space=space, radius=30, mass=10)
    b2 = Circle(pos=a2, space=space, radius=30, mass=10)

    GrooveJoint(b1.body, b2.body, space, a1=1.5 * (b2.body.position - b1.body.position), a2=0.5 * (b2.body.position - b1.body.position), anchor_b=(0, 0))
    GrooveJoint(b2.body, b1.body, space, a2=1.5 * (b1.body.position - b2.body.position), a1=0.5 * (b1.body.position - b2.body.position), anchor_b=(0, 0))
    app.run()
