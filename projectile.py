import pygame

class projectile(object):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, x, y, velocity, \
                 direction, color, radius, creator):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.velocity = velocity
        self.direction = direction
        self.color = color
        self.x_distance = 0
        self.creator = creator

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update_position(self, keys, bullets):
        if self.x + self.velocity * self.direction > 0 and \
                self.x + self.velocity * self.direction < self.screen_width:
            self.x = self.x + self.velocity * self.direction
        else:
            index = bullets.index(self)
            del bullets[index]



