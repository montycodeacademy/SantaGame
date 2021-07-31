import math
import random
from projectile import *

from player import *


class bad_guy(player):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, width, height, imageLoc):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, width, height, imageLoc)

    def update_position(self, keys, bullets):
        dist = 500
        for bullet in bullets:
            if (bullet.creator != self):
                dist = min(math.sqrt((self.x - bullet.x) * (self.x - bullet.x) + \
                                 (self.y - bullet.y) * (self.y - bullet.y)), dist)

        if not (self.isJump):
            if dist < 75:
                self.isJump = True
                self.jumpCount = 32
        else:
            if self.jumpCount >= -32:
                if self.jumpCount <= 0:
                    self.y += (self.jumpCount * self.jumpCount) * 0.02
                else:
                    self.y -= (self.jumpCount * self.jumpCount) * 0.02
                self.jumpCount -= 1;
            else:
                self.isJump = False

        if self.walkRight:
            if self.x < self.screen_width - self.width / 2 - self.velocity:
                self.x += self.velocity
            else:
                self.walkRight = False
                self.walkLeft = True

        if self.walkLeft:
            if self.x + self.width / 2 + self.velocity > 0:
                self.x -= self.velocity
            else:
                self.walkLeft = False
                self.walkRight = True

        self.x_cen = round(self.x + self.width / 2)
        self.y_cen = round(self.y + self.height / 2)

        if random.randrange(1,250) == 13:
            if self.walkRight:
                bullet = projectile(self.screen_width, self.screen_height, \
                                    round(self.x + self.width / 2), \
                                    round(self.y + self.height / 2), \
                                    10, 1, (0, 0, 0), 5, self)
            else:
                bullet = projectile(self.screen_width, self.screen_height, \
                                    round(self.x + self.width / 2), \
                                    round(self.y + self.height / 2), \
                                    10, -1, (0, 0, 0), 5, self)
            bullets.append(bullet)
            player.fired_sound.play(0)
            player.status = "Bad Guy Fires"


    def setCollisionState(self, value):
        if self.health > 10:
            self.health -= self.health_loss
            if player.explosion_sound:
                player.explosion_sound.play(0)
                player.status = "Bad Guy Hit"
        else:
            print("Out of health- set state to done")
