import sys
import pygame
import random
from math import floor
from pygame.locals import *

def contain(point, gametype):
    for obj in point:
        if obj.get_type() == gametype:
            return True
    return False

def init_window():
        pygame.init()
        pygame.display.set_mode((512, 512))
        pygame.display.set_caption('Packman')


class GameObject(pygame.sprite.Sprite):
      def __init__(self, img, x, y, tile_size, map_size):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.image.load(img)
          self.screen_rect = None #Переменная, хранящая размеры для отрисовки.
          self.x = x
          self.y = y
          self.tile_size = tile_size
          self.map_size = map_size
          self.set_coord(x,y)
          self.type = gameobject
          self.exists = True

      def destroy(self):
          self.exists = False

      def alive(self):
          return self.exists

      def set_coord(self, x, y):
          self.x = x
          self.y = y
          self.screen_rect = Rect(floor(x) * self.tile_size, floor(y) * self.tile_size, self.tile_size, self.tile_size)

      def set_type(self, newtype):
          self.type = newtype

      def get_type(self):
          return self.type
      def get_x(self):
          return self.x

      def get_y(self):
          return self.y

      def draw(self, scr):
          scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))

      def move(self, world, direction, distance):
          field = world.get_map()
          current_x = self.get_x()
          current_y = self.get_y()
          world.object_to_field(self, current_x, current_y)
          if direction == 0  or distance == 0:
              pass
          elif direction == 1:
              if contain(field[current_x][current_y + 1], 'Wall'):
                  pass
              else:
                  world.replace(self, current_x, current_y, current_x, current_y + 1)
                  self.move(self, world, direction, distance - 1)
          elif direction == 2:
            if contain(field[current_x + 1][current_y], 'Wall'):
                pass
            else:
                world.replace(self, current_x, current_y, current_x + 1, current_y)
                self.move(self, world, direction, distance - 1)
          elif direction == 3:
            if contain(field[current_x][current_y - 1], 'Wall'):
                pass
            else:
                world.replace(self, current_x, current_y, current_x, current_y - 1)
                self.move(self, world, direction, distance - 1)
          elif direction == 4:
            if contain(field[current_x - 1][current_y], 'Wall'):
                pass
            else:
                world.replace(self, current_x, current_y, current_x - 1, current_y)
                self.move(self, world, direction, distance - 1)



class BluePortal(GameObject):
    def __init__(self, x, y, tile_size, map_size, target_x, target_y):
         GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size, 'Portal')
         self.status = 0
         self.target_x = target_x
         self.target_y = target_y

    def get_target_x(self):
        return self.target_x

    def get_target_y(self):
        return self.target_y

    def me_with_object(self, obj, world):
        if obj.get_type() == 'Pacman':
            self.status = 4
            world.replace(obj, obj.get_x(), obj.get_y(), self.get_target_x(), self.get_target_y())

    def logic(self, world):
        if self.status > 0:
            self.status -= 1

class OrangePortal(GameObject):
    def __init__(self, x, y, tile_size, map_size, target_x, target_y):
         GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size, 'Portal')
         self.status = 0
         self.target_x = target_x
         self.target_y = target_y

    def get_target_x(self):
        return self.target_x

    def get_target_y(self):
        return self.target_y

    def me_with_object(self, obj, world):
        if obj.get_type() == 'Pacman':
            self.status = 4
            world.replace(obj, obj.get_x(), obj.get_y(), self.get_target_x(), self.get_target_y())


    def logic(self, world):
        if self.status > 0:
            self.status -= 1

class Wall(GameObject):
    def __init__(self, x, y, tile_size, map_size):
         GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size, 'Wall')

    def me_with_object(self, obj, world):
        pass

    def logic(self, world):
        pass

class Candy(GameObject):
    def __init__(self, x, y, tile_size, map_size):
          GameObject.__init__(self, './resources/ghost.png', x, y, tile_size, map_size, 'Wall')

    def me_with_object(self, obj, world):
        if obj.get_type() == 'Pacman':
            self.destroy()

    def logic(self, world):
        pass




class Game:
      def __init__(self, config):
          self.map = parse(config) #Считываем конфиг, и создаем игровую карту.

      def get_map(self):
          return self.map


      def object_to_field(self, who, with_x, with_y):
         for obj in self.map[with_x][with_y]:
             who.me_with_object(obj, self)

      def replace(self, who, from_x, from_y, to_x, to_y):
          for i in range(len(self.map[from_x][from_y])):
              if self.map[from_x][from_y][i] is who:
                  self.map[to_x][to_y].append(who)
                  self.map[from_x][from_y].pop(i)
                  who.set_coord(to_x, to_y)
                  break

      def gametick(self):
          for x in self.map:
             for y in x:
                 for obj in y:
                     if obj.alive():
                         obj.logic()
                     else:
                         del(obj)
          for x in self.map:
              for y in x:
                  for obj in y:
                      obj.draw()

      def process_events(events, packman):
           for event in events:
                 if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        sys.exit(0)
                 elif event.type == KEYDOWN:
                        if event.key == K_LEFT:
                                packman.direction = 2
                        elif event.key == K_RIGHT:
                                packman.direction = 4
                        elif event.key == K_UP:
                                packman.direction = 1
                        elif event.key == K_DOWN:
                                packman.direction = 3
                        elif event.key == K_SPACE:
                                packman.direction = 0

      def mainloop(self, screen, backgraund):
         while True:
                self.process_events(pygame.event.get())
                pygame.time.delay(300)
                self.gametick()
                draw_background(screen, background)
                ghost.draw(screen)
                pygame.display.update()

if __name__ == '__main__':
        init_window()
        tile_size = 32
        map_size = 16
        background = pygame.image.load("./resources/background.png")
        screen = pygame.display.get_surface()
        game = Game(config)
        game.mainloop(screen, background)
