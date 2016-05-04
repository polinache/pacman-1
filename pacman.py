import sys
import pygame
from pygame.locals import *
from math import floor
import random


def init_window():
        pygame.init()
        pygame.display.set_mode((512, 512))
        pygame.display.set_caption('Packman')


def draw_background(scr, img=None):
        if img:
                scr.blit(img, (0, 0))
        else:
                bg = pygame.Surface(scr.get_size())
                bg.fill((0, 0, 0))
                scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
        def __init__(self, img, x, y, tile_size, map_size):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(img)
                self.screen_rect = None
                self.x = 0
                self.y = 0
                self.tick = 0
                self.tile_size = tile_size
                self.map_size = map_size
                self.set_coord(x, y)

        def set_coord(self, x, y):
                self.x = x
                self.y = y
                self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size )

        def game_tick(self):
                self.tick += 1

        def draw(self, scr):
                scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
        def __init__(self, x, y, tile_size, map_size):
                GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size)
                self.direction = 0                # 0 - неподвижно, 1 - вправо, 2 = вниз, 3 - влево, 4 - вверх
                self.velocity = 1       # Скорость в клетках / игровой тик

        def game_tick(self):
                super(Ghost, self).game_tick()
                if self.tick % 10 == 0 or self.direction == 0: # Каждые 10 тиков случайно выбираем направление движения. Вариант self.direction == 0 соотвествует моменту первого вызова метода game_tick() у обьекта
                        self.direction = random.randint(1, 4)

                if self.direction == 1:                        # Для каждого направления движения увеличиваем координату до тех пор пока не достгнем стены. Далее случайно меняем напрвление движения
                        self.x += self.velocity
                        if self.x >= self.map_size-1:
                                self.x = self.map_size-1
                                self.direction = random.randint(1, 4)
                elif self.direction == 2:
                        self.y += self.velocity
                        if self.y >= self.map_size-1:
                                self.y = self.map_size-1
                                self.direction = random.randint(1, 4)
                elif self.direction == 3:
                        self.x -= self.velocity
                        if self.x <= 0:
                                self.x = 0
                                self.direction = random.randint(1, 4)
                elif self.direction == 4:
                        self.y -= self.velocity
                        if self.y <= 0:
                                self.y = 0
                                self.direction = random.randint(1, 4)
                self.set_coord(self.x, self.y)


class Pacman(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/pacman.png', x, y, tile_size, map_size)
        self.direction = 0
        self.velocity = 1
        self.bonus = 0
        self.hp = 100

    def swallow(self):
        super(Pacman, self).game_tick()
        if self.bonus != 10:
            for i in range(len(food)):
                if (self.x == food[i].x)and(self.y == food[i].y):
                    food[i].x = food[i].y = 100
                    self.bonus += 1
        else:
            exit('You win!')
            
    def damage(self):
        super(Pacman, self).game_tick()
        if self.hp > 0:
            for gh in ghost:
                if (self.x == gh.x)and(self.y == gh.y):
                    self.hp -= random.randint(32, 51)
                    print('HP:', self.hp)
        else:
            exit('You lost.')


    def game_tick(self):
        super(Pacman, self).game_tick()
        x1 = self.x
        y1 = self.y
        if self.direction == 1:
            self.x += self.velocity
            if self.x >= self.map_size-1:
                self.x = self.map_size-1
        elif self.direction == 2:
            self.y += self.velocity
            if self.y >= self.map_size-1:
                self.y = self.map_size-1
        elif self.direction == 3:
            self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
        for wall in thewall:
            if self.x == wall.x and self.y == wall.y:
                self.x = x1
                self.y = y1
        self.swallow()
        self.damage()
        self.set_coord(self.x, self.y)


def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0

class Food(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/food.bmp', x, y, tile_size, map_size)
"""
class Map:
        def __init__(self, w, h):
                self.map = [[list()]*x for i in range(y)]

        # Функция возвращает список обьектов в данной точке карты
        def get(self, x, y):
                return self.map[x][y]
"""

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
        GameObject.__init__(self, './resources/wall.png', x, y, tile_size, map_size)

"""
def process_events(events):
        for event in events:
                if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        sys.exit(0)
"""

if __name__ == '__main__':
        init_window()
        tile_size = 32
        map_size = 16
        pacman = Pacman(1, 1, tile_size, map_size)
        map_file = open('map.txt', 'r')
        food_file = open('food.txt', 'r')
        thewall = []
        ghost = []
        food = []
        number_of_ghosts = random.randint(3, 8)
        A = map_file.readlines()
        B = food_file.readlines()
        for i in range(len(A)-1):
            A[i] = list(map(int, A[i].split()))
            thewall.append(Wall(A[i][0], A[i][1], tile_size, map_size))
        for i in range(number_of_ghosts):
            ghost.append(Ghost(random.randint(1, 15), random.randint(1, 15), tile_size, map_size))
        for i in range(len(B)):
            B[i] = list(map(int, B[i].split()))
            food.append(Food(B[i][0], B[i][1], tile_size, map_size))
        background = pygame.image.load("./resources/background.png")
        screen = pygame.display.get_surface()

        while 1:
                process_events(pygame.event.get(), pacman)
                pygame.time.delay(300)
                for i in range(len(ghost)):
                    ghost[i].game_tick()
                pacman.game_tick()
                draw_background(screen, background)
                for i in range(len(thewall)):
                    thewall[i].draw(screen)
                for i in range(len(food)):
                    if food[i].x != 100:
                        food[i].draw(screen)
                for i in range(len(ghost)):
                    ghost[i].draw(screen)
                pacman.draw(screen)
                pygame.display.update()
