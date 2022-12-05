import pymunk
import random
from itertools import combinations
from constraints import TSpringJoint
import statistics

GRAY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (200, 50, 200)
GREEN = (0, 255, 0)
size = w, h = 2700, 800


class Circle:
    id = 0

    def __init__(self, pos, space, radius=30, color=GREEN, friction=0.5, mass=0.01):
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


class Subject:
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


