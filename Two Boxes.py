import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Boxes")
#creates a window
BORDER = pygame.Rect(WIDTH//2 - 5 ,0, 10, HEIGHT)
#the middle line
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('PygameForBeginners-main','Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('PygameForBeginners-main','Assets','Gun+Silencer.mp3'))
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('PygameForBeginners-main','Assets','cosmic-drift.mp3'))
#sounds
HEALTH_FONT =  pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60 #frames per second
VEL =5
BULLET_VEL = 20
MAX_BULLETS = 1 #max bullet thrown 

YELLOW_HIT =  pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
# mutilple userevent

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('PygameForBeginners-main','Assets','spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('PygameForBeginners-main','Assets','spaceship_red.png'))

YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(55, 40)),90)
#55 --> width,  40--> height,  90 degrees rotate
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(55, 40)),270)
#55 --> width,  40--> height,  270 degrees rotate
SPACE =pygame.image.load(os.path.join('PygameForBeginners-main','Assets','space.png'))



def draw_window(yellow,red, red_bullet, yellow_bullet,red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, (0,0,0),BORDER) #draws middle line
    #pygame.draw.rect(): This function is used to draw a rectangle. It takes the surface, color, and pygame Rect object as an input parameter and draws a rectangle on the surface.

    red_health_text = HEALTH_FONT.render("Health: "+ str(red_health),1,(255,255,255))
    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_health),1,(255,255,255))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10,10))
    #to get the red score inside the screen
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE,(red.x, red.y))
#player images
    for bullet in red_bullet:
        pygame.draw.rect(WIN,(255,0,0), bullet)
    for bullet in yellow_bullet:
        pygame.draw.rect(WIN,(255,255,0),bullet)
        #bullets images
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #yellow should not leave the screen
        yellow.x -= VEL #left
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #yellow should not cross the border
        yellow.x += VEL #right
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #yellow should not leave the screen
        yellow.y -= VEL #up
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #yellow should not leave the screen
        yellow.y += VEL #down

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #red should not cross the border
        red.x -= VEL #left
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #red should not leave the screen
        red.x += VEL #right
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #red should not leave the screen
        red.y -= VEL #up
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #red should not leave the screen
        red.y += VEL #down

def handle_bullets(yellow_bullet, red_bullet, yellow, red):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
            #removes bullets from yellow when red is hit
        elif bullet.x > WIDTH:
           yellow_bullet.remove(bullet)
           #removes bullets hits end of screen

    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
            #removes bullets from red when yellow is hit
        elif bullet.x < 0:
            red_bullet.remove(bullet)
            #removes bullets hits end of screen


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1, (255,255,255))
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) #freezes pygame and restarts
        
def main():

    red = pygame.Rect(700, 300, 55, 40)
    yellow = pygame.Rect(100,300,55,40)

    red_bullet = []
    yellow_bullet = []
#scores
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()

    BACKGROUND_SOUND.play()

    run = True
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN: #key pressed down
                if event.key == pygame.K_LCTRL and len(yellow_bullet) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    #bullet should come out of the image
                    yellow_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLETS:
                   bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                   red_bullet.append(bullet) 
                   BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text =""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if  winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() #moves even if the keys are cotinuous pressed
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullet,red_bullet,yellow,red)

        draw_window(yellow,red, red_bullet, yellow_bullet, red_health, yellow_health)
    main()

if __name__ == "__main__":
    main()