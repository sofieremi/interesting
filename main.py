import pygame as pg
import random
import math

vec2, vec3 = pg.math.Vector2, pg.math.Vector3

RES = WIDTH, HEIGHT = 1200, 675
NUM_STARS = 2000
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
COLORS = 'gold crimson orangered yellow'.split()
Z_DISTANCE = 40
ALPHA = 120


def get_pos3d(scale_pos=35):
    angle = random.uniform(0, 2 * math.pi)
    radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
    # radius = random.randrange(HEIGHT // 4, HEIGHT // 3) * scale_pos
    x = radius * math.sin(angle)
    y = radius * math.cos(angle)
    return vec3(x, y, Z_DISTANCE)


class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = get_pos3d()
        # self.vel = random.uniform(0.05, 0.25)
        self.vel = random.uniform(0.45, 0.95)
        self.color = random.choice(COLORS)
        self.screen_pos = vec2(0, 0)
        self.size = 10

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)
        mouse_pos = CENTER - vec2(pg.mouse.get_pos())
        self.screen_pos == mouse_pos

    def draw(self):
        pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for i in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in self.stars]


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.Clock = pg.time.Clock()
        self.starfield = Starfield(self)

    def run(self):
        while True:
            # self.screen.fill('black')
            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run()

            pg.display.flip()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.Clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
