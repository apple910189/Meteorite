import pygame as pg
import pygame.sprite
import random
import os

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
# 創建視窗
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Meteorite")
clock = pg.time.Clock()
# 載入圖片
background_img = pg.image.load(os.path.join("img", "background.png")).convert()  # 轉換成pg好讀取的形式
player_img = pg.image.load(os.path.join("img", "player.png")).convert()  # 轉換成pg好讀取的形式
rock_img = pg.image.load(os.path.join("img", "rock.png")).convert()  # 轉換成pg好讀取的形式
bullet_img = pg.image.load(os.path.join("img", "bullet.png")).convert()  # 轉換成pg好讀取的形式

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

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = rock_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 定位 匡起來 這行要放前面！否則後面畫圓會出事
        self.radius = self.rect.width * 0.8 / 2  # 設定碰撞石頭半徑
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)  # 畫出圓形
        # self.image = pg.Surface((30,40))  # 平面
        # self.image.fill(RED)
        self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)  # 設定初始座標x 以中心點為標準點
        self.rect.y = random.randrange(-50, -40)  # 設定初始座標y
        self.speedy = random.randrange(3, 11)
        self.speedx = random.randrange(-10, 11)
        self.rotate_degree = 5

    def rotate(self):
        self.image = pg.transform.rotate(self.image,self.rotate_degree)

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


all_sprites = pg.sprite.Group()  # sprite群組放sprite物件
rocks = pg.sprite.Group()
bullets = pg.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)  # 將rock加到rocks群組，之後與bullets群組做碰撞判斷


# 遊戲迴圈
running = True
while running:
    clock.tick(FPS)  # 限制一秒鐘迴圈所跑的次數
    # get data 回傳一個列表，裡面是各種操作的事件
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
    # update game
    all_sprites.update()  # 執行all_sprites裡面每一個物件的update函式
    hits = pg.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        r = Rock()
        all_sprites.add(r)  # 碰撞後新增石頭，並加入群組重生
        rocks.add(r)

    hits2 = pg.sprite.spritecollide(player, rocks, False, pg.sprite.collide_circle)  # 判斷碰撞 player and rocks
    if hits2:
        running = False

    # screen display
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)  # 把all_sprites裡面的東西都畫到screen上
    pg.display.update()

pg.quit()