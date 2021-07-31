from player import *
from projectile import *
from pygame.locals import *


class good_guy(player):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, width, height, imageLoc):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, width, height, imageLoc)

        self.last_bullet_fired = pygame.time.get_ticks()

    def update_position(self, keys, bullets):
        if not (self.isJump):
            if keys[K_UP]:
                self.isJump = True
                self.jumpCount = 32
                if (player.jump_sound):
                    player.jump_sound.play(0)
                    player.status = "Good Guy Jumps"
        else:
            if self.jumpCount >= -32:
                if self.jumpCount <= 0:
                    self.y += (self.jumpCount * self.jumpCount) * 0.02
                else:
                    self.y -= (self.jumpCount * self.jumpCount) * 0.02
                self.jumpCount -= 1;
            else:
                self.isJump = False

        if keys[K_LEFT] and self.x + self.width / 2 + self.velocity > 0:
            self.x -= self.velocity
            self.walkLeft = True
            self.face_right = False
        else:
            self.walkLeft = False

        if keys[K_RIGHT] and self.x < self.screen_width - self.width / 2 - self.velocity:
            self.x += self.velocity
            self.walkRight = True
            self.face_right = True
        else:
            self.walkRight = False

        if keys[K_SPACE] and len(bullets) < 6:
            t = pygame.time.get_ticks()
            if (t - self.last_bullet_fired) / 1000.0 > .25:
                if player.fired_sound:
                    player.fired_sound.play(0)
                    player.status = "Good Guy Fires"
                if self.face_right:
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
            self.last_bullet_fired = t
        self.x_cen = round(self.x + self.width / 2)
        self.y_cen = round(self.y + self.height / 2)


