import pymunk
import random

# Constants
POPULATION_SIZE = 100
GENERATIONS = 50

# Classes
class Body:
    def __init__(self, mass, propulsion_force):
        self.mass = mass
        self.propulsion_force = propulsion_force
        self.distance_traveled = 0
        self.body = pymunk.Body(self.mass)  # Create body
        self.shape = pymunk.Circle(self.body, 10)  # Use body as argument
        
    def evaluate(self):
        return self.distance_traveled
    
    def mutate(self):
        self.mass += random.uniform(-0.1, 0.1)
        self.propulsion_force += random.uniform(-0.1, 0.1)
        
    def clone(self):
        return Body(self.mass, self.propulsion_force)

# Functionsa
def create_initial_population():
    return [Body(random.uniform(0.5, 2.0), random.uniform(5.0, 15.0)) for i in range(POPULATION_SIZE)]

def simulate(space, body):

    if body.body in space.bodies:
        space.remove(body.body)
    # Add body to space
    space.add(body.body, body.shape)
    # Apply propulsion force
    body.body.apply_force_at_local_point((0, body.propulsion_force), (0, 0))

    # Run simulation for 10 seconds
    for i in range(100):
        space.step(0.1)
    body.distance_traveled = body.shape.body.position.x
            
def reproduce(body1, body2):
    # Combine properties of both bodies
    mass = (body1.mass + body2.mass) / 2
    propulsion_force = (body1.propulsion_force + body2.propulsion_force) / 2
    
    return Body(mass, propulsion_force)

# Main program
space = pymunk.Space()
space.gravity = (0, -900)

# Create initial population
population = create_initial_population()

# Evaluate initial population
for body in population:
    simulate(space, body)

# Iterate over generations
for generation in range(GENERATIONS):
    # Select most fit individuals for reproduction
    population.sort(key=lambda body: body.evaluate(), reverse=True)
    fit_individuals = population[:int(0.8 * POPULATION_SIZE)]
    
    # Reproduce and create next generation
    for i in range(int(0.8 * POPULATION_SIZE) - 1):
        population.append(reproduce(fit_individuals[i], fit_individuals[i+1]))    
    # Mutate some individuals
    for body in population:
        if random.uniform(0, 1) < 0.1:
            body.mutate()
            
    # Evaluate new generation
    for body in population:
        simulate(space, body)
        
# Print final results
population.sort(key=lambda body: body.evaluate(), reverse=True)
for body in population:
    print(f"Distance traveled: {body.distance_traveled:.2f}")
