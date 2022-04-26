from cmath import rect
import pygame
import random
import os


FPS = 60
WIDTH = 500
HEIGH = 600
DEGREE_OF_DIFFICULTY = 1.6  # 1 is the normal difficulty.
CAPTION = "Space War"
PLAYER_LIFE = 3
FULL = 10
OFFSET = 2
POWERFULL_DURATION = 8000

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


# init game and create the screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption(CAPTION)
clock =  pygame.time.Clock()

# loading resources
# loading pictures
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30,30)))

    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img","shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img","gun.png")).convert()

# loading sounds
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")), 
    pygame.mixer.Sound(os.path.join("sound","expl1.wav")), 
]
player_expl_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.4)


# font setting
font_name = os.path.join("font","font.ttf") 
def draw_text(surf, text, size, x=WIDTH/2, y=20):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# draw init screen
def draw_init_screen():
    
    screen.blit(background_img, (0, 0)) 
    draw_text(screen, "太空生存战", 64, WIDTH/2, HEIGH/4)
    draw_text(screen, "<- ->移动飞船 空白键发射子弹～", 22, WIDTH/2, HEIGH/2)
    draw_text(screen, "按任意键开始游戏！", 18, WIDTH/2, HEIGH * 3/4)
    pygame.display.update()

    waiting_init_screen = True
    while waiting_init_screen:
        clock.tick(FPS)
        # get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            else:
                if event.type == pygame.KEYUP:
                    waiting_init_screen = False
                    return False

# create the space craft
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.power = 1
        self.power_time = 0

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGH - 10
        self.speedx = 8
        self.health = FULL
        self.lives = PLAYER_LIFE
        # draw_text(self.image, str(self.health), 12, self.image.get_rect().centerx, self.image.get_rect().centery)

    def update(self):
        now = pygame.time.get_ticks()
        if self.power > 0 and now - self.power_time > POWERFULL_DURATION:
            self. power -= 1
            self.power_time = now

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedx
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedx

        rect = screen.get_rect()
        if not rect.contains(self.rect):
            if self.rect.top < 0: self.rect.top = 0
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.bottom > HEIGH: self.rect.bottom = HEIGH
            if self.rect.right > WIDTH: self.rect.right = WIDTH
        # draw_text(self.image, str(self.health), 20, self.image.get_rect().centerx, self.image.get_rect().centery)

    def shoot(self):
        i = 0
        while i <= self.power:
            if i == 0:
                offset = 0
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet) 
                bullets.add(bullet)
            else:
                offset = i * OFFSET
                bulletl = Bullet(self.rect.centerx, self.rect.top, -offset)
                bulletr = Bullet(self.rect.centerx, self.rect.top, offset)
                all_sprites.add(bulletl) 
                all_sprites.add(bulletr) 
                bullets.add(bulletl)
                bullets.add(bulletr)
            i += 1
        shoot_sound.play()

# create the rocks
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2 * 0.85)
        self.life = int(self.radius * DEGREE_OF_DIFFICULTY / 10)
        # pygame.draw.circle(self.image_ori, RED, self.rect.center, self.radius)
        # draw_text(self.image, str(self.life), 12, self.rect.centerx, self.rect.centery)
        self.rect.centerx = random.randrange(0, WIDTH)
        self.rect.top = 0 - self.rect.height
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 8)
        self.rot_degree = random.randrange(-4, 4)
        self.total_degree = 0

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect =  self.image.get_rect( )
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy
        # draw_text(self.image, str(self.life), 12, self.image.get_rect().centerx, self.image.get_rect().centery)
        
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGH:
            self.rect.centerx = random.randrange(0, WIDTH)
            self.rect.top = 0 - self.rect.height
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 6)

# create the bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, offset=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.offset = offset

    def update(self):
        self.rect.centery += self.speedy
        self.rect.centerx += self.offset
        if self.rect.bottom < 0:
            self.kill()

# create the explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center            

# create the Power
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield'])
        self.image = power_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4

    def update(self):
        self.rect.centery += self.speedy
        if self.rect.top > HEIGH:
            self.kill() 

# create a new rock
def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def new_power(center):           
    if random.random() > 0.92:
        pow = Power(center)
        all_sprites.add(pow)
        powers.add(pow)

# draw craft health rectangle on the screen
def draw_health(surf, hp, x, y):
    if hp < 0: hp =0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/10)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# draw craft lives on the screen
def draw_lives(surf, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = WIDTH - 30 * (i + 1)
        img_rect.y = 10
        surf.blit(img, img_rect)


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()

player = Player()
all_sprites.add(player) 
for i in range(10):
    new_rock()
score = 0
pygame.mixer.music.play(-1)


# 游戏回圈
running = True
game_initial = True
while running:
    
    if game_initial:
        if draw_init_screen():
            break
        game_initial = False

        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player) 
        for i in range(10):
            new_rock()
        score = 0

    clock.tick(FPS)
    # get user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # game update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, False, True)
    for rock, bullet in hits.items():
        if rock.life>0:
            rock.life -= 1
        else:
            rock.kill()
            new_rock()
            score += rock.radius
            expl = Explosion(rock.rect.center, 'lg')
            all_sprites.add(expl)
            random.choice(expl_sounds).play()
            new_power(rock.rect.center)

    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.life
        if player.health >0:
            score += hit.radius
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            random.choice(expl_sounds).play()
        else:
            death_expl = Explosion(hit.rect.center, 'player')
            all_sprites.add(death_expl)
            player_expl_sound.play()
            player.lives -= 1
            player.health = FULL
    if player.lives == 0 and not(death_expl.alive()): 
        # running = False 
        game_initial = True

    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:  
        if hit.type == 'shield':
            player.health = FULL
            shield_sound.play()
        elif hit.type == 'gun': 
            player.power += 1
            player.power_time = pygame.time.get_ticks()
            gun_sound.play()

    # display the game
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18)
    draw_health(screen, player.health, 5, 10)
    draw_lives(screen, player.lives, player_mini_img)
    pygame.display.update()

pygame.quit()