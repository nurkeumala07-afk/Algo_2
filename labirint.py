from pygame import *

win_width = 700
win_height = 500
display.set_caption('Maze')
window = display.set_mode((win_width, win_height))
back = (209, 219, 255)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'

        if self.rect.x >= win_width - 85:
            self.side = 'left'
        
        
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()



w1 = GameSprite('platform2.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png',370, 100, 50, 400)


monster = Enemy('cyborg.png', win_width - 80, 180, 80, 80, 5)
monster2 = Enemy('cyborg.png', win_width - 200, 300, 80, 80, 5)


barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)


bullets = sprite.Group()

monsters = sprite.Group()
monsters.add(monster)
monsters.add(monster2)

pacman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)    
# monster = GameSprite('cyborg.png', win_width - 80, 180, 80, 80)
final_sprite = GameSprite('pac-1.png', win_width - 80, win_height - 80, 80, 80)

run = True
finish = False

while run:
    time.delay(50)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        
        elif e.type == KEYDOWN:
            if e.key == K_a:
                print('kiri ditekan')
                pacman.x_speed = -5
            
            elif e.key == K_d:
                pacman.x_speed =+5

            elif e.key == K_w:
                pacman.y_speed = -5
            
            elif e.key == K_s:
                pacman.y_speed = +5

            elif e.key == K_SPACE:
                pacman.fire()

        
        elif e.type == KEYUP:
            if e.key == K_a:
                print('kiri dilepas')
                pacman.x_speed = 0
            elif e.key == K_d:
                pacman.x_speed = 0
            elif e.key == K_w:
                pacman.y_speed =0
            elif e.key == K_s:
                pacman.y_speed = 0

    if not finish :
        window.fill(back)
        w1.draw()
        w2.draw()
        pacman.draw()
        pacman.update()
        # monster.draw()
        # monster.update()
        final_sprite.draw()

        
        bullets.update()
        bullets.draw(window)

        monsters.update()
        monsters.draw(window)

        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)


        if sprite.collide_rect(pacman, monster):
            finish = True
            img = image.load('game-over_1.png')
            window.fill((209, 219, 255))
            window.blit(transform.scale(img, (700, 500)), (0, 0))
        
        
        if sprite.collide_rect(pacman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((209, 219, 255))
            window.blit(transform.scale(img, (700, 500)), (0, 0))

        if sprite.spritecollide(pacman, barriers, False):
            print('Menabrak tembok')
            pacman.rect.x = 5
            pacman.rect.y = win_height - 80

    display.update()








