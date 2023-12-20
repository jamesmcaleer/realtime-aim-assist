import pyautogui as pg
import pygame
import time
import sys
import keyboard

WIDTH, HEIGHT = pg.size()

ENEMY = (247, 34, 221) # (187, 0, 248)

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

time.sleep(5)
# im = pg.screenshot('temp.png', region=(WIDTH//2 - 200, HEIGHT//2 - 200, 400, 400))

class EnemyLocator:

    def __init__(self):
        self.image = pg.screenshot('temp.png', region=(WIDTH // 2 - 200, HEIGHT // 2 - 200, 400, 400))

    def take_screenshot(self):
        self.image = pg.screenshot('temp.png', region=(WIDTH // 2 - 200, HEIGHT // 2 - 200, 400, 400))
        return self.image

    def add_points(self):
        self.points = []

        for x in range(0, self.image.width, 5):
            for y in range(0, self.image.height, 5):
                if self.close((x, y), ENEMY, 50):
                    self.points.append((x, y))

        return self.points

    def average_point(self):
        x = 0
        y = 0
        for point in self.points:
            x += point[0]
            y += point[1]

        try:
            self.average_coordinate = (x//len(self.points), y//len(self.points))
            print("coord", self.average_coordinate)
            print("color", self.image.getpixel(self.points[0]))
            return self.average_coordinate

        except ZeroDivisionError:
            print("no icon")

        self.average_coordinate = 0,0
        return (0,0)

    def close(self, cord, enemy, tolerance):
        return (self.image.getpixel(cord)[0] - tolerance <= enemy[0] and self.image.getpixel(cord)[0] + tolerance >= enemy[0]) and (
                    self.image.getpixel(cord)[1] - tolerance <= enemy[1] and self.image.getpixel(cord)[1] + tolerance >= enemy[1]) and \
               (self.image.getpixel(cord)[2] - tolerance <= enemy[2] and self.image.getpixel(cord)[2] + tolerance >= enemy[2])

class AimAssist:
    def __init__(self, e_loc):
        self.locator = e_loc

    def main(self):
        self.locator.take_screenshot()
        self.locator.add_points()
        self.locator.average_point()

class ImageDisplayer:

    def __init__(self, e_loc):
        self.locator = e_loc
        pygame.init()
        self.screen = pygame.display.set_mode((self.locator.image.width, self.locator.image.height))

        self.img = pygame.image.load('temp.png')
        self.img.convert()

        self.rect = self.img.get_rect()
        self.rect.center = self.locator.image.width // 2, self.locator.image.height // 2

    def main(self):
        self.img = pygame.image.load('temp.png')
        self.img.convert()

        self.rect = self.img.get_rect()
        self.rect.center = self.locator.image.width // 2, self.locator.image.height // 2

        self.screen.fill(WHITE)
        self.screen.blit(self.img, self.rect)
        pygame.draw.rect(self.screen, RED, self.rect, 1)

        for cord in self.locator.add_points():
            pygame.draw.circle(self.screen, BLUE, cord, 1)

        pygame.draw.circle(self.screen, RED, self.locator.average_coordinate, 5)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


enemy_locator = EnemyLocator()
image_displayer = ImageDisplayer(enemy_locator)
aim_assist = AimAssist(enemy_locator)

while keyboard.is_pressed('q') == False:
    aim_assist.main()
    image_displayer.main()

