import pygame as pg
import pygame.sprite
import random
import os

# 常數 new branch j
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 500
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
HEIGHT = 600

# 遊戲初始化
pg.init()
pg.mixer.init()  # 音效模組初始化

# 創建視窗
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Meteorite")
clock = pg.time.Clock()

# 載入圖片
background_img = pg.image.load(os.path.join("img", "background.png")).convert()  # 轉換成pg好讀取的形式
player_img = pg.image.load(os.path.join("img", "player.png")).convert()  # 轉換成pg好讀取的形式
# rock_img = pg.image.load(os.path.join("img", "rock.png")).convert()  # 轉換成pg好讀取的形式
bullet_img = pg.image.load(os.path.join("img", "bullet.png")).convert()  # 轉換成pg好讀取的形式
rock_imgs = []
for i in range(7):
    rock_imgs.append(pg.image.load(os.path.join("img", f"rock{i}.png")).convert())

# 載入音效
shoot_sound = pg.mixer.Sound(os.path.join("sound", "shoot.wav"))
expl_sounds = [
    pg.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pg.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pg.mixer.music.load(os.path.join("sound", "background.ogg"))
pg.mixer.music.set_volume(0.5)

# 文字設定
font_name = pg.font.match_font("arial")

# 將文字呈現在平面上
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)  # create font with it's type and size
    text_surface = font.render(text, True, WHITE)  # render the text on a text surface
    text_rect = text_surface.get_rect()  # get the text's rect
    text_rect.centerx = x  # set the text_rect's position
    text_rect.top = y
    surf.blit(text_surface, text_rect)  # draw the text on surface of the argument

# 畫出血條
def draw_health(surf, hp, x, y):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)  # 設定外匡矩形
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)  # 設定填滿矩形
    pg.draw.rect(surf, GREEN, fill_rect)  # 畫出綠條
    pg.draw.rect(surf, WHITE, outline_rect, 2)  # 畫出外匡

def new_rock():
    r = Rock()
    all_sprites.add(r)  # 碰撞後新增石頭，並加入群組重生
    rocks.add(r)

# 創建類別Player去繼承內建的Sprite類別
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((50,40))  # 平面
        self.image = pg.transform.scale(player_img, (50, 38))  #
        self.image.set_colorkey(BLACK)  # 將圖片中的顏色設為透明
        self.radius = 20  # 設定碰撞飛船半徑
        self.rect = self.image.get_rect()  # 定位 匡起來 這行要放前面！否則下面畫圓會找不到rect
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)  # 畫出圓形
        # self.image.fill(GREEN)
        # self.rect.x = 495 # 以左上角為標準點
        # elf.rect.y = 595
        self.rect.centerx = WIDTH/2  # 以中心點為標準點
        self.rect.bottom = HEIGHT-10
        self.speedx = 9
        self.health = 100

    def update(self):
        key_pressed = pg.key.get_pressed()  # 回傳一組布林值，表達鍵盤上按鍵是否有被按下
        if key_pressed[pg.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pg.K_LEFT]:
            self.rect.x -= self.speedx
        # if self.rect.x > WIDTH:
        #     self.rect.left = 0
        # self.rect.x += 3
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # self.image_ori = rock_imgs[random.randrange(0, 6)]  # 沒轉動過的圖
        self.image_ori = random.choice(rock_imgs)  # 沒轉動過的圖
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()  # 複製圖片包含所有屬性
        self.rect = self.image.get_rect()  # 定位 匡起來 這行要放前面！否則後面畫圓會出事
        self.radius = int(self.rect.width * 0.8 / 2)  # 設定碰撞石頭半徑
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)  # 畫出圓形
        # self.image = pg.Surface((30,40))  # 平面
        # self.image.fill(RED)
        self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)  # 設定初始座標x 以中心點為標準點
        self.rect.y = random.randrange(-180, -100)  # 設定初始座標y
        self.speedy = random.randrange(3, 6)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-10, 11)

    def rotate(self):  # transform.rotate 造成圖片失真
        self.total_degree += self.rotate_degree  # 每次轉動都增加度數，但會加超過360度
        self.total_degree = self.total_degree % 360  # 防止超過360度繼續無限疊加
        self.image = pg.transform.rotate(self.image_ori, self.total_degree)
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
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        #  self.image.fill(YELLOW)
        self.rect = self.image.get_rect()  # 定位 匡起來
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# 參數初始化
all_sprites = pg.sprite.Group()  # sprite群組放sprite物件
rocks = pg.sprite.Group()
bullets = pg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_rock()  # 將rock加到rocks群組，之後與bullets群組做碰撞判斷
score = 0
pg.mixer.music.play(-1)

# 遊戲迴圈
running = True
while running:
    clock.tick(FPS)  # 限制一秒鐘迴圈所跑的次數
    # 取得事件 回傳一個列表，裡面是各種操作的事件
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
    # 更新動作
    all_sprites.update()  # 執行all_sprites裡面每一個物件的update函式
    hits = pg.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        new_rock()

    hits2 = pg.sprite.spritecollide(player, rocks, True, pg.sprite.collide_circle)  # 判斷碰撞 player and rocks
    for hit in hits2:
        new_rock()
        player.health -= hit.radius
        if player.health <=0:
            running = False

    # 畫面呈現
    # screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)  # 把all_sprites裡面的東西都畫到screen上
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 10)
    pg.display.update()

pg.quit()