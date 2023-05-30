import math
import random
import numpy as np
import pygame.sprite

POINT_SIZE = 5
POINTS = [(182, 177), (205, 142), (283, 140), (339, 176), (324, 244), (248, 306), (187, 279), (220, 236), (241, 218),
          (274, 202), (262, 253), (786, 184), (876, 148), (974, 270), (773, 290), (776, 220), (881, 211), (771, 276),
          (861, 245), (868, 327), (877, 252), (792, 269), (904, 299), (915, 299), (258, 686), (508, 580), (716, 618),
          (409, 575), (352, 561), (556, 669), (297, 659), (707, 686), (395, 737), (589, 628), (401, 671), (463, 661),
          (568, 735), (615, 731), (568, 522), (465, 504), (434, 500), (988, 643), (981, 633), (940, 584), (1065, 573),
          (1113, 644), (1037, 718), (949, 697), (903, 614), (938, 571), (1007, 586), (1067, 664), (1066, 678),
          (916, 592), (888, 668), (952, 676), (1090, 633), (971, 643), (1040, 629), (1106, 603), (1012, 653),
          (911, 649), (942, 541), (1083, 511), (1169, 527), (1208, 634), (1150, 682), (1013, 543), (963, 532),
          (1098, 563), (1141, 612), (554, 509), (469, 464), (363, 467), (289, 548), (196, 594), (247, 688), (465, 709),
          (588, 662), (590, 577), (337, 666), (584, 613), (286, 636), (540, 620), (396, 644), (386, 607), (416, 622),
          (502, 639), (433, 617), (800, 191), (715, 230), (765, 175), (731, 304), (739, 128), (935, 110), (1018, 189),
          (892, 221), (815, 151), (785, 117), (951, 184), (846, 178), (965, 216), (919, 262), (829, 298), (904, 359),
          (770, 342), (989, 321), (988, 341), (1013, 242), (1014, 226), (1055, 216), (1080, 171), (938, 105),
          (989, 164), (1029, 143), (1030, 108), (1038, 98), (1065, 78), (1106, 75), (1124, 116), (1127, 184),
          (1075, 239), (1053, 263), (1044, 312), (1026, 336), (1081, 360), (1003, 369), (895, 364), (798, 382),
          (779, 378), (643, 615), (640, 665), (679, 671), (644, 696), (591, 711), (528, 713), (453, 718), (493, 769),
          (249, 253), (267, 275), (122, 276), (108, 174), (186, 92), (379, 66), (469, 122), (344, 237), (165, 204),
          (244, 184), (73, 257), (266, 186), (214, 224), (1271, 353), (1307, 351), (1318, 383), (1301, 391),
          (1269, 396), (1270, 379), (1256, 330), (1297, 319), (1337, 351), (1346, 390), (1280, 438), (1236, 400),
          (1237, 359), (1314, 424), (1319, 424)]
WIDTH, HEIGHT = 1366, 768

BLACK = 0, 0, 0
LIGHTBLACK = 25, 25, 25
LIGHTERBLACK = 39, 39, 55
WHITE = 255, 255, 255
DARK_WHITE = 200, 200, 230
PINK = (223, 0, 125)
LIGHTBEIGE = 181, 136, 99
PURPLE = (155, 31, 233)
BROWN = (89, 62, 49)
GREEN = (0, 255, 1)
ORANGE = (250, 154, 0)
RED = 250, 41, 76
GRAY = (185, 224, 226)
BLUE = (0, 0, 255)
YELLOW = (253, 253, 4)

MEANS_COLOR = [RED, GREEN, BLUE, PURPLE, YELLOW, ORANGE]


def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def draw_star(screen, color, center, radius, num_points):
    points = []
    angle = math.pi / num_points

    for i in range(num_points * 2):
        radius_star = radius if i % 2 == 0 else radius // 2
        x = center[0] + math.cos(i * angle) * radius_star
        y = center[1] + math.sin(i * angle) * radius_star
        points.append((x, y))

    pygame.draw.polygon(screen, color, points)


class Centroid:
    def __init__(self, id_centroid, size=20):
        self.pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.id_cluster = id_centroid
        self.size = size

    def draw(self, win):
        draw_star(win, MEANS_COLOR[self.id_cluster], self.pos, self.size, 4)


class Point:
    def __init__(self, x, y, id_cluster=-1, size=10):
        self.pos = x, y
        self.id_cluster = id_cluster
        self.size = size

    def draw(self, win):
        pygame.draw.circle(win, MEANS_COLOR[self.id_cluster], self.pos, self.size)
        pygame.draw.circle(win, BLACK, self.pos, self.size, 1)


class Game:
    def __init__(self, win):
        self.game_is_on = True
        self.win = win

        self.k = 5
        self.points = []
        self.means = [Centroid(i) for i in range(self.k)]

        self.iterations = 0

        self.load_points()

    def load_points(self):
        for point in POINTS:
            self.points.append(Point(point[0], point[1]))

    def run(self):
        clock = pygame.time.Clock()
        while self.game_is_on:
            clock.tick(60)
            self.win.fill(DARK_WHITE)
            self.events()
            self.draw(self.win)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_is_on = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.points.append(Point(event.pos[0], event.pos[1]))
                    print([p.pos for p in self.points])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_kmeans()

    def next_kmeans(self):
        # Assign every point to a centroid
        for point in self.points:
            min_dist = np.Inf

            for mean in self.means:
                d = distance(mean.pos, point.pos)
                if d < min_dist:
                    min_dist = d
                    point.id_cluster = mean.id_cluster

        # Move the centroids to the center of their points
        for mean in self.means:
            sum_x = 0
            sum_y = 0
            n_points = 0
            for point in self.points:
                if point.id_cluster == mean.id_cluster:
                    sum_x += point.pos[0]
                    sum_y += point.pos[1]
                    n_points += 1
            if n_points > 0:
                mean.pos = sum_x / n_points, sum_y / n_points

        self.iterations += 1

    def draw(self, win):
        for point in self.points:
            point.draw(win)
        for mean in self.means:
            mean.draw(win)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("K-Means")
    game = Game(win)
    game.run()
    pygame.quit()
