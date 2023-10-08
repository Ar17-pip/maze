from pygame import *
mixer.init()
font.init()

window = display.set_mode((700, 500))
display.set_caption("Лабиринт")
clock = time.Clock()
FPS= 60
background = transform.scale(image.load("background.jpg"),(700, 500))
money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")
font = font.SysFont('Arial', 70)
win = font.render("YOU WIN!", True, (255, 215, 0))
lose = font.render("YOU LOSE!", True, (255,0,0))
mixer.music.load("jungles.ogg")
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_s] and self.rect.y < 495:
            self.rect.y += self.speed
        if keys_pressed[K_w] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys_pressed[K_a] and self.rect.x > 10:     
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 695:       
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 500:
            self.direction = "right"
        if self.rect.x >= 700 - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1,color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


wall_1 = Wall(15, 200, 50, 100, 0, 17, 400)
wall_2 = Wall(15, 200, 50, 225, 100, 17, 400)
wall_3 = Wall(15, 200, 50, 350, 0, 17, 400)
wall_4 = Wall(15, 200, 50, 475, 100, 17, 400)
hero = Player("hero.png", 20, 20, 5)
cyborg = Enemy("cyborg.png", 650, 350, 1)
treasure = GameSprite("treasure.png", 550,430,1)

finish = False
game = True
while game:
   

    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0, 0))
        hero.update()
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()  
        wall_4.draw_wall() 
        hero.reset()
        cyborg.update()
        cyborg.reset()
        treasure.reset()
        
        if sprite.collide_rect(hero, treasure):
            finish = True
            money.play()
            window.blit(win, (200, 200))
        if sprite.collide_rect(hero, cyborg) or sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2) or sprite.collide_rect(hero, wall_3):
            finish = True
            kick.play()
            window.blit(lose, (200, 200))
        

    display.update()
    clock.tick(FPS)