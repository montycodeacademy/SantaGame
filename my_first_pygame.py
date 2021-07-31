from bad_guy import *
from good_guy import *
from control_panel import *


# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# all related to player
surf_width = 94
surf_height = 63

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

def redrawScreen():
    # Fill the screen with the background image
    global walkCount
    global jumpCount
    screen.blit(my_control_panel.backGround, (0, 0))
    my_control_panel.draw(screen, myEnemy.status)
    myPlayer.draw(screen)
    myEnemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    for button in buttons:
        button.draw(screen)
    pygame.display.flip()

def pause_game():
    player.status = "Game Paused - Hit Resume"
    pause_btn.set_active(False)
    resume_btn.set_active(True)
    redrawScreen()
    my_control_panel.pause_game()
    player.status = "Game Running"
    pause_btn.set_active(True)
    resume_btn.set_active(False)

def resume_game():
    my_control_panel.paused = False

def reset_game():
    print("Reset Game")

def help():
    my_control_panel.set_help_flag(not my_control_panel.get_help_flag())

def mousebuttonsclicked():
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.call_back()

pause_btn = simple_button("Pause", (60, 30), pause_game)
resume_btn = simple_button("Resume", (60, 70), resume_game)
resume_btn.set_active(False)
reset_btn = simple_button("Reset", (60,110), reset_game)
help_btn = simple_button("Help", (60,150), help)
buttons = [pause_btn, resume_btn, reset_btn, help_btn]

# Main loop
clock = pygame.time.Clock()
clock.tick(33)
myPlayer = good_guy(SCREEN_WIDTH, SCREEN_HEIGHT, surf_width, surf_height, "Player")
myPlayer.x = 0
myEnemy = bad_guy(SCREEN_WIDTH, SCREEN_HEIGHT, surf_width, surf_height, "Enemy")
myEnemy.walkRight = True
bullets = []

my_control_panel = control_panel(SCREEN_WIDTH, SCREEN_HEIGHT, pause_btn, resume_btn, help_btn, redrawScreen)

def handle_collision():
    isColliding = False
    distance = math.sqrt((myEnemy.x_cen - myPlayer.x_cen) * (myEnemy.x_cen - myPlayer.x_cen) + \
                           (myEnemy.y_cen - myPlayer.y_cen) * (myEnemy.y_cen - myPlayer.y_cen))

    if (myEnemy.radius + myPlayer.radius > distance):
        isColliding = True
    myPlayer.setCollisionState(isColliding)

    for bullet in bullets:
        if bullet.creator != myEnemy:
            distance = math.sqrt((bullet.x - myEnemy.x_cen) * (bullet.x - myEnemy.x_cen) + \
                                 (bullet.y - myEnemy.y_cen) * (bullet.y - myEnemy.y_cen))

            if myEnemy.radius + bullet.radius > distance:
                index = bullets.index(bullet)
                del bullets[index]
                my_control_panel.score += 1
                myEnemy.setCollisionState(True)
            else:
                x_distance =  myEnemy.x - bullet.x
                if not x_distance or x_distance * bullet.x_distance < 0 :
                    myEnemy.doh_sound.play(0)
                    player.status = "Bad Guy Evades"
                bullet.x_distance = x_distance
        else:
            distance = math.sqrt((bullet.x - myPlayer.x_cen) * (bullet.x - myPlayer.x_cen) + \
                                 (bullet.y - myPlayer.y_cen) * (bullet.y - myPlayer.y_cen))
            if myPlayer.radius + bullet.radius > distance:
                index = bullets.index(bullet)
                del bullets[index]
                my_control_panel.score -= 1
                myPlayer.setCollisionState(True)
            else:
                x_distance =  myPlayer.x - bullet.x
                if not x_distance or x_distance * bullet.x_distance < 0 :
                    #myPlayer.doh_sound.play(0)
                    player.status = "Good Guy Evades"
                bullet.x_distance = x_distance

my_control_panel.start_game()

while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_p:
                pause_game()
            elif event.key == K_h:
                my_control_panel.set_help_flag(not my_control_panel.get_help_flag())
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mousebuttonsclicked()

    keys = pygame.key.get_pressed()
    myPlayer.update_position(keys, bullets)
    myEnemy.update_position(keys, bullets)
    for bullet in bullets:
        bullet.update_position(keys, bullets)
    handle_collision()
    redrawScreen()
    pygame.time.delay(10)

my_control_panel.quit_game()
