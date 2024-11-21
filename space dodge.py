import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 500
# width and height of the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#WIN means window
#display is a module, and set_mode is a function inside that module. It actually creates an instance of the pygame.Surface class, and returns that
pygame.display.set_caption("Space Dodge")
#set_caption gives the WIN a name
BG = pygame.transform.scale(pygame.image.load("ZZXg1.jpg"),(WIDTH, HEIGHT))
#scale transforms the image to fit the screen
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
#players block
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3
#falling objects
FONT = pygame.font.SysFont("comicsans", 30)
#explains the desired font


def draw(player,elapsed_time,stars):
#to draw
    WIN.blit(BG,(0,0))
#The Pygame blit() method is one of the methods to place an image onto the screens of pygame applications. 

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
#1 is a anti-aliasing parameter
    #This creates a new surface with text already drawn onto it. At the end you can just blit the text surface onto your main screen.
    #for the tickeing time on the screen
    WIN.blit(time_text,(10,10))
#positions the time_text
    pygame.draw.rect(WIN,"red", player)
#Player's bloack
    for star in stars:
        pygame.draw.rect(WIN, "white", star)
#for falling blocks
    pygame.display.update()
#pygame.display.update. — Update portions of the screen for software displays.
def main():
    run = True
    
    player =pygame.Rect(200,HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
#positions the player's block
    clock = pygame.time.Clock()
#time. Clock function makes a clock object that can be used to keep track of time.
    start_time = time.time()
    #The Python time time() method returns the current UTC time.
    elapsed_time = 0;

    star_add_increment = 2000
    star_count = 0
#number of falling stars
    stars = []
    hit = False
#if hits the target
    while run:

        star_count += clock.tick(60)
        #increase the star count
        elapsed_time = time.time() - start_time
#number of blocks that needs to fall
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0,  WIDTH)
                #The randint() method returns an integer number selected element from the specified range.
                star = pygame.Rect(star_x, STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT )
                #-STAR_HEIGHT is so that bloack appear from above the screen
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50) 
            #increases the time speed for falling stars gradually
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #should close the win when 'X' button is hit

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        #gives keys information and direction the player bloack should move
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            #if star hits bottom, they should dissapear
            elif star.y + STAR_HEIGHT >= player.y and star.colliderect(player):
                #colliderect for adding collision in a shape using Pygame in Python.
                stars.remove(star)
                hit = True
                break
            #if stars collid with player block, end the game
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            #font details that appears when game is lost
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            #position where lost_text must be placed
            pygame.display.update()
            pygame.time.delay(4000)
            #frezzes the game
            break

        draw(player,elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
