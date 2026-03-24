import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH,ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_RADIUS_INTERVAL, ANGLES
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.point_diff_list = [self.radius + random.uniform( -ASTEROID_RADIUS_INTERVAL, ASTEROID_RADIUS_INTERVAL) for angle in ANGLES]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.asteroid_shape(), LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity*dt

    def split(self, player):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            player.add_score()
            return
        
        log_event("asteroid_split")
        angle = random.uniform(20,50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = self.velocity.rotate(angle) *1.2
        asteroid2.velocity = self.velocity.rotate(-angle)*1.2
    
    def asteroid_shape(self):
        pointlist = []
        for angle_i in range(len(ANGLES)):
            diff = self.point_diff_list[angle_i]
            point = self.position + pygame.Vector2(0,1).rotate(ANGLES[angle_i])*diff
            pointlist.append(point)
        return pointlist

    # proposed by ChatGPT
    def bounce(self, other_asteroid):
        offset = other_asteroid.position - self.position
        distance = offset.length()

        if distance == 0:
            return

        normal = offset / distance

        # Push overlapping asteroids apart
        overlap = self.radius + other_asteroid.radius - distance
        if overlap > 0:
            correction = normal * (overlap / 2)
            self.position -= correction
            other_asteroid.position += correction

        # Relative velocity along collision normal
        relative_velocity = self.velocity - other_asteroid.velocity
        speed_along_normal = relative_velocity.dot(normal)

        # If they are already moving apart, do nothing
        if speed_along_normal > 0:
            return

        # Equal-mass elastic collision:
        # swap the normal components of velocity
        impulse = normal * speed_along_normal
        self.velocity -= impulse
        other_asteroid.velocity += impulse