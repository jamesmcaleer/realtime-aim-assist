import pyautogui as pg
import pygame
import time
import sys
WIDTH, HEIGHT = pg.size()

ENEMY = (247, 34, 221) # (187, 0, 248)

WHITE = (255,255,255)
RED = (255,0,0)

time.sleep(5)
im = pg.screenshot('temp.png', region=(WIDTH//2 - 200, HEIGHT//2 - 200, 400, 400))

class EnemyFinder:

    def __init__(self, screenshot):
        self.sc = screenshot
        self.width = self.sc.width
        self.height = self.sc.height


    def add_points(self):
        self.points = []

        for x in range(0, self.width, 5):
            for y in range(0, self.height, 5):
                if self.close((x, y), ENEMY, 5):
                    self.points.append((x, y))

        return self.points

    def average_point(self):
        x = 0
        y = 0
        for point in self.points:
            x += point[0]
            y += point[1]

        self.average_coordinate = (x//len(self.points), y//len(self.points))
        print(self.average_coordinate)
        return self.average_coordinate

    def close(self, cord, enemy, tolerance):
        return (self.sc.getpixel(cord)[0] - tolerance <= enemy[0] and self.sc.getpixel(cord)[0] + tolerance >= enemy[0]) and (
                    self.sc.getpixel(cord)[1] - tolerance <= enemy[1] or self.sc.getpixel(cord)[1] + tolerance >= enemy[1]) and \
            self.sc.getpixel(cord)[2] - tolerance <= enemy[2] or self.sc.getpixel(cord)[2] + tolerance >= enemy[2]


class ImageDisplayer:

    def __init__(self, eFinder):
        self.finder = eFinder
        pygame.init()
        self.screen = pygame.display.set_mode((self.finder.width, self.finder.height))

        self.img = pygame.image.load('temp.png')
        self.img.convert()

        self.rect = self.img.get_rect()
        self.rect.center = self.finder.width // 2, self.finder.height // 2

    def main(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.img, self.rect)
        pygame.draw.rect(self.screen, RED, self.rect, 1)

        for cord in self.finder.add_points():
            pygame.draw.circle(self.screen, WHITE, cord, 1)

        pygame.draw.circle(self.screen, RED, ef.average_point(), 5)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


ef = EnemyFinder(im)
id = ImageDisplayer(ef)

while True:
    id.main()