import sys
import math
import random
import pygame as pg

def main():
    pg.init()

# Color Table
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LT_GRAY = (180, 180, 180)
GRAY = (120, 120, 120)
DK_GRAY = (80, 80 ,80)
RED = (255, 0, 0)

class Particle(pg.sprite.Sprite):
    # Builds ejecta particles
    gas_colors = {'S02': LT_GRAY, 'CO2': GRAY, 'H2S': DK_GRAY, 'H20': WHITE}
    
    VENT_LOCATION_XY = (320, 306)
    IO_SURFACE_Y = 348
    GRAVITY = 0.7 # pixels per frame added to dy each game loop
    VELOCITY_SO2 = 12 # pixels per frame

    # vel_scalar = {'S02': 1, 'CO2': 1.45, 'H2S': 1.9, 'H20': 3.6}
    vel_scalar = {'S02': 1.71, 'CO2': 1.72, 'H2S': 1.73, 'H20': 1.74}


    def __init__(self, screen, background, lifespan):
        super().__init__()
        self.screen = screen
        self.background = background
        self.image = pg.Surface((4,4))
        self.rect = self.image.get_rect()
        # for all gasses
        self.gas = random.choice(list(Particle.gas_colors.keys()))
        # self.color = Particle.gas_colors[self.gas]

        self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]
        self.color = Particle.interpolate_color((255, 120, 80), (255, 60, 60), self.vel)
        self.x, self.y = Particle.VENT_LOCATION_XY
        self.lifespan = lifespan
        self.initial_velocity = self.vel
        self.segments = []
        self.vector()


    def vector(self):
        # Calculate particle vector at launch
        orient = random.uniform(60, 120) #90 is vertical
        radians = math.radians(orient)
        self.dx = self.vel * math.cos(radians)
        self.dy = -self.vel * math.sin(radians)


    def update(self):
        # Apply gravity, draw path, and handle boundary conditions
        self.dy += Particle.GRAVITY
        pg.draw.line(self.background, self.color, (self.x, self.y), (self.x + self.dx, self.y + self.dy))
        self.x += self.dx
        self.y += self.dy

        new_segment = {'start_pos': (self.x, self.y),
                       'end_pos': (self.x + self.dx, self.y + self.dy),
                       'lifespan': self.lifespan}
        self.segments.append(new_segment)

        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()

        if self.x < 0 or self.x > self.screen.get_width():
            self.kill()

        if self.y < 0 or self.y > self.screen.get_width():
            self.kill()


        velocity_magnitude = math.sqrt(self.dx**2 + self.dy**2)

        normalized_velocity = min(velocity_magnitude / self.initial_velocity, 1)
        print(normalized_velocity)

        
        self.color = Particle.interpolate_color((255, 120, 80), (255, 60, 60), normalized_velocity)

        #self.image.fill(self.color)

    @staticmethod
    def interpolate_color(color1, color2, factor):
        # Interpolate between 2 colors

        factor = min(max(factor, 0), 0.8)

        return (
            int(color1[0] + (color2[0] - color1[0]) * factor),
            int(color1[1] + (color2[1] - color1[1]) * factor),
            int(color1[2] + (color2[2] - color1[2]) * factor),
        )


def main():
    # Set up and run screen and loop
    screen = pg.display.set_mode((639, 360))
    pg.display.set_caption('Volcano Simulator')
    background = pg.image.load('tvashtar_plume.gif').convert()

    # Set up color-coded legend
    legend_font = pg.font.SysFont('None', 24)
    water_label = legend_font.render('--- H20', True, WHITE, BLACK)
    h2s_label = legend_font.render('--- H2S', True, DK_GRAY, BLACK)
    co2_label = legend_font.render('--- CO2', True, GRAY, BLACK)
    so2_label = legend_font.render('--- SO2/S2', True, LT_GRAY, BLACK)

    particles = pg.sprite.Group()
    clock = pg.time.Clock()

    while True:
        clock.tick(60)
        particles.add(Particle(screen, background, lifespan=80))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        screen.blit(background, (0,0))
        screen.blit(water_label, (40, 20))
        screen.blit(h2s_label, (40, 40))
        screen.blit(co2_label, (40, 60))
        screen.blit(so2_label, (40, 80))

        particles.update()
        particles.draw(screen)

        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    main()