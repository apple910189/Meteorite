import pygame
import random
import os

# 常數 new branch o
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 500
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
HEIGHT = 600

# 遊戲初始化
pygame.init()
pygame.mixer.init()  # 音效模組初始化

# 創建視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteorite")
clock = pygame.time.Clock()

# 載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()  # convert轉換成pygame好讀取的形式
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)

power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()

# 載入音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))

die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.5)

# 文字設定
font_name = os.path.join("font.ttf")
# font_name = pygame.font.match_font("arial")


def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# 將文字呈現在平面上
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)  # 設定字型及大小
    text_surface = font.render(text, True, WHITE)  # 將文字渲染到文字平面，文字，鋸齒，顏色
    text_rect = text_surface.get_rect()  # 產生文字匡
    text_rect.centerx = x  # 文字匡定位
    text_rect.top = y
    surf.blit(text_surface, text_rect)  # 利用Blit將文字匡與文字平面結合

# 畫出血條
def draw_health(surf, hp, x, y):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # 設定外匡矩形
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)  # 設定填滿矩形
    pygame.draw.rect(surf, GREEN, fill_rect)  # 畫出綠條
    pygame.draw.rect(surf, WHITE, outline_rect, 2)  # 畫出外匡

def new_rock():
    r = Rock()
    all_sprites.add(r)  # 碰撞後新增石頭，並加入群組重生
    rocks.add(r)

# 創建類別Player去繼承內建的Sprite類別
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))  #
        self.image.set_colorkey(BLACK)  # 將圖片中的顏色設為透明
        self.radius = 20  # 設定碰撞飛船半徑
        self.rect = self.image.get_rect()  # 定位 匡起來 這行要放前面！否則下面畫圓會找不到rect
        self.rect.centerx = WIDTH/2  # 以中心點為標準點
        self.rect.bottom = HEIGHT-10
        self.speedx = 9
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun_lv = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun_lv > 1 and now - self.gun_time > 5000:
            self.gun_lv -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2  # 以中心點為標準點
            self.rect.bottom = HEIGHT - 10
        key_pressed = pygame.key.get_pressed()  # 回傳一組布林值，表達鍵盤上按鍵是否有被按下
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not self.hidden:
            if self.gun_lv == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun_lv >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun_lv += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image_ori = rock_imgs[random.randrange(0, 6)]  # 沒轉動過的圖
        self.image_ori = random.choice(rock_imgs)  # 沒轉動過的圖
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()  # 複製圖片包含所有屬性
        self.rect = self.image.get_rect()  # 定位 匡起來 這行要放前面！否則後面畫圓會出事
        self.radius = int(self.rect.width * 0.8 / 2)  # 設定碰撞石頭半徑
        self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)  # 設定初始座標x 以中心點為標準點
        self.rect.y = random.randrange(-180, -100)  # 設定初始座標y
        self.speedy = random.randrange(3, 6)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-10, 11)

    def rotate(self):  # transform.rotate 造成圖片失真
        self.total_degree += self.rotate_degree  # 每次轉動都增加度數，但會加超過360度
        self.total_degree = self.total_degree % 360  # 防止超過360度繼續無限疊加
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        # 先把中心點存起來，轉動之後重新定位中心點
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)  # 以中心點為標準點
            self.rect.y = random.randrange(-50, -40)
            self.speedy = random.randrange(3, 11)
            self.speedx = random.randrange(-10, 11)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        #  self.image.fill(YELLOW)
        self.rect = self.image.get_rect()  # 定位 匡起來
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -60

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()  # 定位 匡起來
        self.rect.center = center
        self.frame = 0  # 爆炸圖片編號，從零開始
        self.last_update = pygame.time.get_ticks()  # 記錄初始化到現在經過的毫秒數
        self.frame_rate = 50  # 設定經過多少毫秒進入到下一張圖片

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):  # 如果是最後一張爆炸圖片，則刪掉自己
                self.kill()
            else:  # 反之則更新到下一張圖片
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center  # 記錄原本中心點
                self.rect = self.image.get_rect()  # 產生新的定位匡
                self.rect.center = center  # 其中心點定位在原本的中心點

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 定位 匡起來
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# 參數初始化
all_sprites = pygame.sprite.Group()  # sprite群組放sprite物件
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_rock()  # 將rock加到rocks群組，之後與bullets群組做碰撞判斷
score = 0
pygame.mixer.music.play(-1)

# 遊戲迴圈
running = True
while running:
    clock.tick(FPS)  # 限制一秒鐘迴圈所跑的次數
    # 取得事件 回傳一個列表，裡面是各種操作的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新動作
    all_sprites.update()  # 執行all_sprites裡面每一個物件的update函式

    # 子彈與石頭碰撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')  # 產生爆炸
        all_sprites.add(expl)  # 加入all_sprites裡面才能畫出爆炸
        if random.random() > 0.5:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    # 石頭與玩家碰撞
    hits2 = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)  # 判斷碰撞 player and rocks
    for hit in hits2:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')  # 產生爆炸
        all_sprites.add(expl)  # 加入all_sprites裡面才能畫出爆炸
        if player.health <= 0:
            die_sound.play()
            death_expl = Explosion(player.rect.center, 'player')  # 產生爆炸
            all_sprites.add(death_expl)
            player.lives -= 1
            player.health = 100
            player.hide()  # 玩家死亡後，隱藏一段時間再重生
            # running = False
    if player.lives == 0 and not (death_expl.alive()):  #
        running = False

    # 寶物與玩家碰撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':  # hit只能做迭代與判斷，不能編輯
            shield_sound.play().set_volume(0.5)
            # if hit.speedy == 3:  # hit可以抓到player與powers的屬性
            player.health += 20
            # hit.speedy = 70    # hit只能做迭代與判斷，不能編輯
            if player.health > 100:
                player.health = 100
        elif hit.type == 'gun':
            gun_sound.play().set_volume(0.5)
            player.gunup()
    # 畫面呈現
    # screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)  # 把all_sprites裡面的東西都畫到screen上
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 10)
    draw_lives(screen, player.lives, player_mini_img, WIDTH-90, 10)
    pygame.display.update()

pygame.quit()