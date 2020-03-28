# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

res_dir = path.join(path.dirname(__file__), 'Resources/')

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

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    pct = 100 - pct * 10
    if pct < 0: pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_kill_bar(surf, x, y, pct):
    BAR_LENGTH = 69
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(vik_img, (80, 110))
        self.rect = self.image.get_rect()
        self.radius = int(90 / 2 * 0.9)
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

    def shoot(self, all_sprites, bullets):
        if self.lastKeyPressed == 'R': bullet = Bullet(self.rect.right, self.rect.centery, self.lastKeyPressed)
        elif self.lastKeyPressed == 'D': bullet = Bullet(self.rect.centerx, self.rect.bottom, self.lastKeyPressed)
        elif self.lastKeyPressed == 'L': bullet = Bullet(self.rect.left, self.rect.centery, self.lastKeyPressed)
        elif self.lastKeyPressed == 'U': bullet = Bullet(self.rect.centerx, self.rect.top, self.lastKeyPressed)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(corona_img, (40, 40))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.choice([2, HEIGHT - 140])
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
        self.image = pygame.transform.scale(wipe_img, (20, 30))
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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 10

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def show_go_screen():
    import time
    time.sleep(0.5)
    screen.blit(main_bg, bg_rect)
    draw_text(screen, "GO CORONA, CORONA GO", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "69 to WIN, 10 to DIE", 18, WIDTH / 2, HEIGHT * 2 / 4 - 80)
    draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
    

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corona Gang")
clock = pygame.time.Clock()

#Load Sounds
shoot_sound = pygame.mixer.Sound(path.join(res_dir, "gunfire.wav"))
pygame.mixer.music.load(path.join(res_dir, 'wolf.mp3'))
pygame.mixer.music.set_volume(0.5)

#Load images
main_bg    = pygame.image.load(path.join(res_dir, "bg.png")).convert_alpha()
background = pygame.image.load(path.join(res_dir, "nyc.jpg")).convert()
corona_img = pygame.image.load(path.join(res_dir, "corona.png")).convert_alpha()
vik_img    = pygame.image.load(path.join(res_dir, "powell.png")).convert_alpha()
wipe_img   = pygame.image.load(path.join(res_dir, "cash.png")).convert_alpha()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(res_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['lg'].append(img_sm)

background_rect = background.get_rect()
bg_rect         = main_bg.get_rect()

all_sprites, mobs, bullets, player = None, None, None, None

def initializeGame():
    # Game loop
    running = True
    hitCounter = 0
    shootCounter = 0
    pygame.mixer.music.play(loops=-1)

    game_over = True
    while running:

        if game_over:
            hitCounter = 0
            shootCounter = 0
            show_go_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(5):
                m = Mob(player)
                all_sprites.add(m)
                mobs.add(m)

        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets)

        # Update
        all_sprites.update()

        # bullet hit mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            shootCounter += 1
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            m = Mob(player)
            all_sprites.add(m)
            mobs.add(m)

        # mob hit player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) 
        if hits:
            hitCounter += 1
            m = Mob(player)
            all_sprites.add(m)
            mobs.add(m)

        # mob hits mob and deflects
        check = 0
        for mob in mobs:
            for mob1 in mobs:
                if mob != mob1 and pygame.sprite.collide_circle(mob, mob1):
                    mob.rect.x += 10
                    mob.rect.y += 10
                    check = 1
                    break
            if check == 1:
                check = 0
                break

        # Losing condition.
        if hitCounter > 10:
            game_over = True

        # Winning condiiton.
        if shootCounter > 69:
            game_over = True

        # Draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)

        draw_text(screen, 'ECONOMY', 20, WIDTH / 2 - 50, HEIGHT - 100)
        draw_text(screen, str(hitCounter), 50, WIDTH / 2 - 70, HEIGHT - 60)
        draw_text(screen, 'PORTFOLIO', 20, WIDTH / 2 + 50, HEIGHT - 100)
        draw_text(screen, str(shootCounter), 50, WIDTH / 2 + 70, HEIGHT - 60)
        
        draw_shield_bar(screen, 230, HEIGHT - 70, hitCounter)
        draw_kill_bar(screen, 550, HEIGHT - 70, shootCounter)

        # *after* drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    initializeGame()