import pygame
import os.path

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards


class player(object):
    min_radius = 1000
    full_health = 100
    init_instance = False
    fired_sound = 0
    jump_sound = 0
    won_sound = 0
    explosion_sound = 0
    doh_sound = 0
    status = ""
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, width, height, imageLoc):
        self.x = (SCREEN_WIDTH - width) / 2
        self.y = 0.85 * SCREEN_HEIGHT
        self.velocity = 1
        self.isJump = False
        self.walkLeft = False
        self.walkRight = False
        self.jumpCount = 32
        self.walkCount = 0
        self.surf = pygame.Surface((width, height))
        self.surf.set_colorkey(WHITE)
        self.WalkImages = []
        self.JumpImages = []
        self.readWalkImages(imageLoc)
        self.readJumpImages(imageLoc)
        self.hit_box = (0, 0, 0, 0)
        self.collision_state = False
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.width = self.WalkImages[0].get_width()
        self.height = self.WalkImages[0].get_height()
        self.radius = round(min(self.width/2, self.height/2))
        player.min_radius = min (player.min_radius, self.radius)
        self.x_cen = round(self.x + self.width/2)
        self.y_cen = round(self.y +self.height/2)
        self.face_right = True
        self.health = player.full_health
        self.health_loss = 10
        if not player.init_instance:
            player.fired_sound = pygame.mixer.Sound("sounds/bullet_fired.wav")
            player.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
            player.won_sound = pygame.mixer.Sound("sounds/won.wav")
            player.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
            player.doh_sound = pygame.mixer.Sound("sounds/doh.wav")

    def setCollisionState(self, value):
        if value and self.collision_state != value:
            if self.health > 10:
                self.health -= self.health_loss
                if player.won_sound:
                    player.won_sound.play(0)
                    player.status = "Good Guy Hit"
            else:
                print("Out of health- set state to done")
        self.collision_state = value

    def update_position(self, keys, bullets):
        pass

    def draw(self, screen):
        self.surf.fill(WHITE)
        curImage = pygame.Surface((0, 0))
        if self.walkRight:
            self.walkCount += 1
            if self.walkCount > len(self.WalkImages) * 3 - 1:
                self.walkCount = 0
            curImage = self.WalkImages[self.walkCount // 3]
        elif self.walkLeft:
            self.walkCount += 1
            if self.walkCount > len(self.WalkImages) * 3 - 1:
                self.walkCount = 0
            curImage = pygame.transform.flip(self.WalkImages[self.walkCount // 3], True, False)
        elif self.isJump:
            jumpIndex = abs(self.jumpCount - len(self.JumpImages) * 2)
            if jumpIndex < len(self.JumpImages) * 4:
                curImage = self.JumpImages[jumpIndex // 4]
            else:
                curImage = self.JumpImages[0]
            if not self.face_right:
                curImage = pygame.transform.flip(curImage, True, False)
        else:
            if self.face_right:
                curImage = self.WalkImages[0]
            else:
                curImage = pygame.transform.flip(self.WalkImages[0], True, False)

        self.surf.blit(curImage, (0, 0))
        screen.blit(self.surf, (self.x, self.y))
        self.hit_box = (self.x, self.y, curImage.get_width(), curImage.get_height())

        pygame.draw.rect(screen, (0, 255, 0), (self.x_cen - player.min_radius, self.y - 10, player.min_radius * 2, 5), 0)
        pygame.draw.rect(screen, (255, 0, 0), (self.x_cen - player.min_radius, self.y - 10, \
                                               round(2 * player.min_radius - (self.health/player.full_health)* 2 * player.min_radius), 5), 0)

    def readWalkImages(self, imageLoc):
        imagePrefix = "png/" + imageLoc + "/Walk ("
        file_count = 1
        file_path = imagePrefix + str(file_count) + ").png"
        while os.path.exists(file_path):
            imageLoaded = pygame.image.load(file_path)
            imageXformed = pygame.transform.rotozoom(imageLoaded, 0.0, 0.05)
            self.WalkImages.append(imageXformed)
            file_count += 1
            file_path = imagePrefix + str(file_count) + ").png"

    def readJumpImages(self, imageLoc):
        imagePrefix = "png/" + imageLoc + "/Jump ("
        file_count = 1
        file_path = imagePrefix + str(file_count) + ").png"
        while os.path.exists(file_path):
            imageLoaded = pygame.image.load(file_path)
            imageXformed = pygame.transform.rotozoom(imageLoaded, 0.0, 0.05)
            self.JumpImages.append(imageXformed)
            file_count += 1
            file_path = imagePrefix + str(file_count) + ").png"


