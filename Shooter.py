# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'Resources/')
print(img_dir)

WIDTH = 900
HEIGHT = 700
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(vik_img, (90, 110))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.lastKeyPressed = 'U'
    
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]: self.speedx = 6; self.lastKeyPressed = 'R'
        if keystate[pygame.K_DOWN]: self.speedy = 6; self.lastKeyPressed = 'D'
        if keystate[pygame.K_LEFT]:  self.speedx = -6; self.lastKeyPressed = 'L'
        if keystate[pygame.K_UP]: self.speedy = -6; self.lastKeyPressed = 'U'

        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT - 90: self.rect.bottom = HEIGHT - 90
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.top < 0: self.rect.top = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        if self.lastKeyPressed == 'R': bullet = Bullet(self.rect.right, self.rect.centery, self.lastKeyPressed)
        elif self.lastKeyPressed == 'D': bullet = Bullet(self.rect.centerx, self.rect.bottom, self.lastKeyPressed)
        elif self.lastKeyPressed == 'L': bullet = Bullet(self.rect.left, self.rect.centery, self.lastKeyPressed)
        elif self.lastKeyPressed == 'U': bullet = Bullet(self.rect.centerx, self.rect.top, self.lastKeyPressed)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(corona_img, (40, 40))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.choice(2, HEIGHT)
        self.speedy = 3
        self.speedx = 3
        self.player = player

    def update(self):
        if self.player.rect.x > self.rect.x: self.rect.x += self.speedx
        else: self.rect.x -= random.randrange(self.speedx)
        
        if self.player.rect.y > self.rect.y: self.rect.y += self.speedy
        else: self.rect.y -= random.randrange(self.speedy)


        if self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, lastKeyPressed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(wipe_img, (10, 20))
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
        self.speedx = 10
        self.lastKeyPressed = lastKeyPressed

    def update(self):
        if self.lastKeyPressed == 'R': self.rect.x += self.speedx
        elif self.lastKeyPressed == 'D': self.rect.y += self.speedy
        elif self.lastKeyPressed == 'L': self.rect.x -= self.speedx
        elif self.lastKeyPressed == 'U': self.rect.y -= self.speedy
        
        if self.rect.bottom < 0 or self.rect.top > HEIGHT - 110: self.kill()
        if self.rect.right > WIDTH or self.rect.left < 0: self.kill() 

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corona Gang")
clock = pygame.time.Clock()

#Load images
background = pygame.image.load(path.join(img_dir, "nyc.jpg")).convert()
corona_img = pygame.image.load(path.join(img_dir, "corona.png")).convert_alpha()
vik_img    = pygame.image.load(path.join(img_dir, "vik.png")).convert_alpha()
wipe_img   = pygame.image.load(path.join(img_dir, "wipe.jpg")).convert_alpha()
background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(5):
    m = Mob(player)
    all_sprites.add(m)
    mobs.add(m)

def initializeGame():
    # Game loop
    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # bullet hit mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            m = Mob(player)
            all_sprites.add(m)
            mobs.add(m)

        # mob hit player
        hits = pygame.sprite.spritecollide(player, mobs, False)

        # mob hits mob and deflects
        check = 0
        for mob in mobs:
            for mob1 in mobs:
                if mob != mob1 and pygame.sprite.collide_rect(mob, mob1):
                    mob.rect.x += 10
                    mob.rect.y += 10
                    check = 1
                    break
            if check == 1:
                check = 0
                break


        # Draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    initializeGame()