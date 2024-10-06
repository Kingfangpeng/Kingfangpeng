import random
import sys
import time
import pygame

class Player(pygame.sprite.Sprite):#玩家飞机
    #存放所有飞机子弹组
    bullets = pygame.sprite.Group()

    def __init__(self,screen):#初始化飞机窗口
        #精灵初始化方法必须调用
        pygame.sprite.Sprite.__init__(self)
        # 飞机
        self.player = pygame.image.load("image/hero1.png")
        #获取矩阵图片对象
        self.rect = self.player.get_rect()
        self.rect.topleft = [480 / 2 - 102 / 2, 500]
        #飞机位置
        # self.x = 480 / 2 - 102 / 2  # 飞机居中，窗口宽度/2-飞机宽度/2
        # self.y = 500
        self.speed = 5  # 飞机速度
        self.screen = screen
        self.bullets = pygame.sprite.Group() #子弹列表

    def move(self):#飞机移动
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.rect.top -= self.speed
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.rect.left -= self.speed
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.rect.bottom += self.speed
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.rect.right += self.speed
        if key_pressed[pygame.K_SPACE]:
            bullet = Bullet(self.screen,self.rect.left,self.rect.top)#传入飞机坐标
            #把子弹装进列表
            self.bullets.add(bullet)
            #存放所有飞机子弹组
            Player.bullets.add(bullet)

    def update(self):
        self.move()
        self.display()
    def display(self):
        # 飞机进入窗口
        self.screen.blit(self.player, self.rect)
        #子弹坐标更新
        self.bullets.update()
        #子弹添加到屏幕
        self.bullets.draw(self.screen)
        #遍历子弹
        # for bullet in self.bullets:
        #     #子弹显示
        #     bullet.move()
        #     bullet.display()

    @classmethod
    def clear_bullets(cls):
        cls.bullets.empty()

class Enemy(pygame.sprite.Sprite):#敌机
    # 存放所有敌机子弹组
    bullets = pygame.sprite.Group()
    def __init__(self,screen):#初始化飞机窗口
        # 飞机
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.enemy = pygame.image.load("image/enemy1.png")
        self.rect = self.enemy.get_rect()
        #随机生成
        x = random.randrange(1, self.screen.get_width(),50)
        #飞机位置
        self.rect.topleft = [x, 0] #左上角位置
        # self.x = 0
        # self.y = 0
        self.speed = 3  # 敌机速度

        self.enemy_bullets = pygame.sprite.Group()
        self.direction = 'right' #敌机移动方向

    def move(self):#敌机移动
        if self.direction == 'right':
            self.rect.right += self.speed
        elif self.direction == 'left':
            self.rect.right -= self.speed

        if self.rect.left > self.screen.get_width()-57:
            self.direction = 'left'
        elif self.rect.left < 0:
            self.direction = 'right'

        self.rect.bottom += self.speed

    def aotu_fire(self):#敌机子弹实例
        random_num = random.randint(1,80)
        if random_num == 4:
            enemy_bullet = Enemy_bullet(self.screen, self.rect.left, self.rect.top)
            self.enemy_bullets.add(enemy_bullet)
            self.bullets.add(enemy_bullet)#存放敌机子弹组

    def update(self):
        self.aotu_fire()
        self.move()
        self.display()
    def display(self):
        # 敌机进入窗口
        self.screen.blit(self.enemy, self.rect)
        self.enemy_bullets.update()
        self.enemy_bullets.draw(self.screen)
        # for enemy_bullet in self.enemy_bullets:
        #     # 子弹显示
        #     enemy_bullet.move()
        #     enemy_bullet.display()
    @classmethod
    def clear_bullets(cls):
        cls.bullets.empty()

#玩家子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 102/2 - 5/2, y -11]
        #坐标
        # self.x = x + 102/2 - 5/2
        # self.y = y -11
        #速度
        self.speed = 8
        self.screen = screen

    def update(self):
        self.rect.top -= self.speed #子弹坐标
        if self.rect.top < -11: #子弹底部出界销毁
            self.kill()
    # def display(self):
    #     self.screen.blit(self.bullet,(self.x,self.y))
    # def move(self):
    #     self.y -= self.speed


#敌机子弹类
class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self,screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        # 图片
        self.image = pygame.image.load("image/bullet2.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 57/2, y + 43]
        #坐标
        # self.x = x + 57/2
        # self.y = y + 43
        #速度
        self.speed = 3

        self.screen = screen

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > self.screen.get_height():
            self.kill()
    # def display(self):
    #     self.screen.blit(self.enemy_bullet,(self.x,self.y))
    # def move(self):
    #     self.y += self.speed

#碰撞
class Bomb():
    def __init__(self,screen, type):
        self.screen = screen
        if type == "enemy":
            #加载爆炸
            self.bimage = [pygame.image.load(f"image/enemy1_down{v}.png")
                           for v in range(1,5)]
        else:
            self.bimage = [pygame.image.load(f"image/me_destroy_{v}.png")
                           for v in range(1,5)]
        # 设置当前爆炸播放索引
        self.bindex = 0
        # 爆炸设置
        self.bPos = [0, 0]
        # 是否可见
        self.bVisible = False

    def action(self,rect):
        #爆炸方法
        #爆炸坐标
        self.bPos[0] = rect.left
        self.bPos[1] = rect.top
        self.bVisible = True

    def draw(self):
        if not self.bVisible:
            return
        self.screen.blit(self.bimage[self.bindex], (self.bPos[0], self.bPos[1]))
        self.bindex += 1
        if self.bindex >= len(self.bimage):
            #下标到爆炸最后，重置
            self.bindex = 0
            self.bVisible = False

#游戏声音
class Gamesound():
    def __init__(self):
        pygame.mixer.init() #音乐模块初始化
        pygame.mixer.music.load("music/game_music.ogg")
        pygame.mixer.music.set_volume(0.2) #声音大小

        self.__bome = pygame.mixer.Sound("music/use_bomb.wav")
    def bgplay(self):
        pygame.mixer.music.play(-1) #开始播放 遍数：-1无限循环

    def bomeplay(self):
        pygame.mixer.Sound.play(self.__bome)

#地图
class Gamebg():
    def __init__(self,screen):
        self.bgimage1 = pygame.image.load("image/background.png")
        self.bgimage2 = pygame.image.load("image/background.png")
        self.screen = screen
        #移动
        self.y1 = 0
        self.y2 = -self.screen.get_height()

    def draw(self):#绘制地图
        self.screen.blit(self.bgimage1, (0,self.y1,))
        self.screen.blit(self.bgimage2, (0,self.y2,))

    #移动地图
    def move(self):
        self.y1 += 2
        self.y2 += 2
        if self.y1 >= self.screen.get_height():
            self.y1 = 0
        if self.y2 >=0:
            self.y2 = -self.screen.get_height()


class Manager():
    #敌机定时器
    create_enemy_id = 10
    #游戏结束
    gameover_id = 11
    #是否结束
    is_gameover = False
    #倒计时
    over_time = 3

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((480, 700),0,32)
        self.bg = pygame.image.load("image/background.png")
        #地图
        self.gamebg = Gamebg(self.screen)
        #玩家精灵
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group() #敌机
        #爆炸对象
        self.player_bome = Bomb(self.screen, 'Player')
        self.enemy_bome = Bomb(self.screen, 'enemy')
        self.sound = Gamesound()
    def exit(self):
        pygame.quit()
        sys.exit()

    def show_over_text(self):
        self.drawText(f"game over {Manager.over_time}",100,
                      self.screen.get_height()/2,textHeight=50, textColor= (255, 0, 0))

    def game_over_timer(self):
        self.show_over_text()
        Manager.over_time -= 1
        if Manager.over_time == 0:
            pygame.time.set_timer(Manager.gameover_id,0)
            Manager.over_time = 3
            Manager.is_gameover = False
            self.start_game()

    def start_game(self):
        Enemy.clear_bullets()
        Player.clear_bullets()
        manager = Manager()
        manager.main()

    def new_player(self):
        player = Player(self.screen)
        self.players.add(player)

    def new_enemy(self):
        enemy = Enemy(self.screen)
        self.enemies.add(enemy)

    #绘制文字
    def drawText(self, text, x, y, textHeight=30, textColor=(255,0,0),bgColor = None):
        #通过字体文件获取字体对象
        font_obj = pygame.font.Font('font/font.ttf', textHeight)
        #配置显示的文字
        text_obj = font_obj.render(text, True, textColor)
        #获取显示的对象
        text_rect = text_obj.get_rect()
        #坐标
        text_rect.topleft = (x, y)
        #绘制字到指定区域
        self.screen.blit(text_obj, text_rect)

    def main(self):
        self.sound.bgplay()
        #创建玩家和敌机对象
        self.new_player()
        self.new_enemy()
        #开启定时器
        pygame.time.set_timer(Manager.create_enemy_id, 1000)
        while True:
            #背景图
            #self.screen.blit(self.bg, (0, 0))
            self.gamebg.move()#移动
            self.gamebg.draw()#地图显示至窗口
            #文字
            self.drawText('score:0', 0, 0)
            #游戏结束
            if Manager.is_gameover:
                self.show_over_text()
                #pygame.time.set_timer(Manager.gameover_id,1000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: #退出事件
                    self.exit()
                elif event.type == Manager.create_enemy_id:
                    #创建一个敌机
                    self.new_enemy()
                elif event.type == Manager.gameover_id:
                    self.game_over_timer()

            #调用爆炸对象
            self.player_bome.draw()
            self.enemy_bome.draw()
            #判断碰撞 返回字典
            iscollide = pygame.sprite.groupcollide(self.players,self.enemies,True,True)

            if iscollide:
                Manager.is_gameover = True
                #开启倒计时
                pygame.time.set_timer(Manager.gameover_id, 1000)
                #从字典 iscollide 中获取第一个键值对。items() 返回字典中的 (key, value) 对。这里的第一个项就是玩家与敌机的碰撞对象。
                items = list(iscollide.items())[0]#碰撞的对象
                print(items)
                x = items[0] #碰撞玩家
                y = items[1][0] #碰撞的第一个敌机
                #玩家爆炸图片
                self.player_bome.action(x.rect)
                self.enemy_bome.action(y.rect)
                #爆炸声音
                self.sound.bomeplay()
            #玩家子弹和敌机碰撞
            is_enemy = pygame.sprite.groupcollide(Player.bullets,self.enemies,True,True)
            if is_enemy:
                items = list(is_enemy.items())[0]
                print(items)
                y = items[1][0]
                self.enemy_bome.action(y.rect)
                self.sound.bomeplay()
            #敌机子弹和玩家碰撞
            if self.players.sprites():
                isover = pygame.sprite.spritecollide(self.players.sprites()[0],Enemy.bullets,True)
                # is_player = pygame.sprite.groupcollide(Enemy.bullets,self.players,True,True)
                if isover:
                    Manager.is_gameover = True
                    pygame.time.set_timer(Manager.gameover_id, 1000)
                    self.player_bome.action(self.players.sprites()[0].rect)
                    #把玩家移除精灵组
                    self.players.remove(self.players.sprites()[0])
                    self.sound.bomeplay()

            #显示
            self.players.update()
            self.enemies.update()

            pygame.display.update()
            time.sleep(0.01)


if __name__ == '__main__':
    manager = Manager()
    manager.main()



