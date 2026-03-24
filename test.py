import pygame
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, LINE_WIDTH, ASTEROID_RADIUS_INTERVAL, ASTEROID_MAX_RADIUS

def asteroid_shape():
    angles = [0, 45, 90, 135, 180, 225, 270, 315, 360]
    pointlist = []
    for angle in angles:
        diff = ASTEROID_MAX_RADIUS + random.uniform(ASTEROID_MAX_RADIUS - ASTEROID_RADIUS_INTERVAL, ASTEROID_MAX_RADIUS + ASTEROID_RADIUS_INTERVAL)
        pointlist.append(pygame.Vector2(0,1).rotate(angle)*diff)
    return pointlist

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
   

    while True:
        screen.fill("black")

        
        pygame.draw.polygon(screen, "white", asteroid(), LINE_WIDTH)
        pygame.display.flip()
        dt = clock.tick(60)/1000

if __name__ == "__main__":
    main()

