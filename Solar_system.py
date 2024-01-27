import numpy as np
import pygame
import math

from planet import Planet
from star import Star
from satellite import Satellite
import random


pygame.init()

#__________________________________________ WINDOW SET UP ______________________________________________________________
WIDTH = 1500
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

# _______________________________________ RGB COLORS ___________________________________________________________________
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (60, 149, 237)
# _________________________________________ PLANET DATA FROM NASA _____________________________________________________
PLANET_DATA = {
    'Mercury': {'Diameter in km': 4879, 'Mass in kg': 0.330 * 10**24, 'Distance from Sun in 10^6 km': 57.9e6},
    'Venus': {'Diameter in km': 12104, 'Mass in kg': 4.87 * 10**24, 'Distance from Sun in 10^6 km': 108.2e6},
    'Earth': {'Diameter in km': 12756, 'Mass in kg': 5.97 * 10**24, 'Distance from Sun in 10^6 km': 149.6e6},
    'Mars': {'Diameter in km': 6792, 'Mass in kg': 0.642 * 10**24, 'Distance from Sun in 10^6 km': 228.0e6},
    'Jupiter': {'Diameter in km': 142984, 'Mass in kg': 1898 * 10**24, 'Distance from Sun in 10^6 km': 778.5e6},
    'Saturn': {'Diameter in km': 120536, 'Mass in kg': 568 * 10**24, 'Distance from Sun in 10^6 km': 1432.0e6},
    'Uranus': {'Diameter in km': 51118, 'Mass in kg': 86.8 * 10**24, 'Distance from Sun in 10^6 km': 2867.0e6},
    'Neptune': {'Diameter in km': 49528, 'Mass in kg': 1020 * 10**24, 'Distance from Sun in 10^6 km': 4515.0e6},
    'Pluto': {'Diameter in km': 2376, 'Mass in kg': 0.013 * 10**24, 'Distance from Sun in 10^6 km': 5906.4e6},
    'Moon': {'Diameter in km': 3475, 'Mass in kg': 0.073 * 10**24, 'Distance from Sun in 10^6 km': 0.384e6}
}
# _________________________________________ PYGAME MAIN FUNCTION _______________________________________________________
def main():
    run = True
    clock = pygame.time.Clock()
    font1 = pygame.font.Font('SourceSansPro-Bold.ttf', 20)

    # _______________________________________ PLANETS AND SUN INITIALIZATION ___________________________________________
    sun = Star()

    mercury = Planet(x=-1 * (PLANET_DATA['Mercury']['Distance from Sun in 10^6 km'] * 1000) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Mercury']['Diameter in km'] * 1000),
                   mass= PLANET_DATA['Mercury']['Mass in kg'],
                   color=(100, 60, 60),
                     name='Mercury')
    # Initial y velocity of the planet
    mercury.y_velocity = 47.4 *1000

    venus = Planet(x=1 * (PLANET_DATA['Venus']['Distance from Sun in 10^6 km'] * 1000) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Venus']['Diameter in km'] * 1000),
                   mass= PLANET_DATA['Venus']['Mass in kg'],
                   color=(120, 40, 40),
                   name='Venus'
                   )
    # Initial y velocity of the planet
    venus.y_velocity = -35.02 * 1000

    earth = Planet(x=-1 * (PLANET_DATA['Earth']['Distance from Sun in 10^6 km'] * 1000) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Earth']['Diameter in km'] * 1000 ),
                   mass= PLANET_DATA['Earth']['Mass in kg'],
                   color=BLUE,
                   name='Earth')
    # Initial y velocity of the planet
    earth.y_velocity = 29.783 * 1000

    mars = Planet(x=-1 * (PLANET_DATA['Mars']['Distance from Sun in 10^6 km'] * 1000) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Mars']['Diameter in km'] * 1000),
                   mass= PLANET_DATA['Mars']['Mass in kg'],
                   color=RED,
                  name='Mars')
    # Initial y velocity of the planet
    mars.y_velocity = 24.077 * 1000

    jupiter = Planet(x=-1 * (PLANET_DATA['Jupiter']['Distance from Sun in 10^6 km'] * 1000) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Jupiter']['Diameter in km'] * 1000 * 0.3),
                   mass= PLANET_DATA['Jupiter']['Mass in kg'],
                   color=(200, 200, 200),
                     name='Jupiter')
    # Initial y velocity of the planet
    jupiter.y_velocity = 13.1 * 1000

    saturn = Planet(x=-1 * (PLANET_DATA['Saturn']['Distance from Sun in 10^6 km'] * 1000 * 0.5) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Saturn']['Diameter in km'] * 1000),
                   mass= PLANET_DATA['Saturn']['Mass in kg'],
                   color=RED, name='Saturn')
    uranus = Planet(x=-1 * (PLANET_DATA['Uranus']['Distance from Sun in 10^6 km'] * 1000 * 0.5) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Uranus']['Diameter in km'] * 1000),
                   mass= PLANET_DATA['Uranus']['Mass in kg'],
                   color=RED, name='Uranus')
    neptune = Planet(x=-1 * (PLANET_DATA['Neptune']['Distance from Sun in 10^6 km'] * 1000 * 0.5) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Neptune']['Diameter in km'] * 1000 * 0.5),
                   mass= PLANET_DATA['Neptune']['Mass in kg'],
                   color=(0, 255, 0), name='Neptune')
    pluto = Planet(x=-1 * (PLANET_DATA['Pluto']['Distance from Sun in 10^6 km'] * 1000 * 0.1) ,
                   y=0,
                   radius=(0.5 * PLANET_DATA['Pluto']['Diameter in km'] * 1000),
                   mass= PLANET_DATA['Pluto']['Mass in kg'],
                   color=WHITE, name='Pluto')

    # moon = Satellite(x=-1 * ((-PLANET_DATA['Moon']['Distance from Sun in 10^6 km']  + PLANET_DATA['Earth']['Distance from Sun in 10^6 km']) * 1000) ,
    #                y=0,
    #                radius=(0.5 * PLANET_DATA['Moon']['Diameter in km'] * 1000),
    #                mass= PLANET_DATA['Moon']['Mass in kg'],
    #                color=(230, 230, 255),
    #                  name='Moon')
    #
    #
    # # Initial y velocity of the Moon
    # moon.y_velocity = 1 * 1000   + earth.y_velocity

    celestial = {
        'sun': sun,
        'mercury': mercury,
        'venus': venus,
        'earth': earth,
        'mars': mars,
        # 'jupiter': jupiter,
        # 'moon': moon
    }

    # Initialize an artificial Satellite for space exploration
    pre_factor = 4.5 * 1e1
    mass_factor = 0.3
    pre_factor_relative_to_the_moon = 0.01 * pre_factor
    hubble = Satellite(x=1 * (
            -pre_factor_relative_to_the_moon * PLANET_DATA['Moon']['Distance from Sun in 10^6 km'] * 1000 +
            celestial['earth'].x),
                       y=0,
                       radius=(0.5 * PLANET_DATA['Moon']['Diameter in km'] * 1000),
                       mass=PLANET_DATA['Moon']['Mass in kg'] * mass_factor,
                       color=(255, 10, 230),
                       name='Hubble')

    # Initial y velocity of the Moon
    hubble.y_velocity = 0 * 1000 + earth.y_velocity

    planets = [celestial[planet] for planet in list(celestial)]


    # ___________________________________________ PYGAME MAIN Y LOOP ___________________________________________________
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    hubble.satellite_burn_event(celestial['mars'], WIN)

        # pygame.draw.ellipse(
        #     WIN, (255, 0, 0),
        #     [WIN.get_width() / 2, 0, WIN.get_width() / 10, WIN.get_height()],
        #
        # )


        # Render the celestial bodies
        for body in list(celestial):
            celestial[body].update_position(planets)
            celestial[body].draw_orbit(WIN)
            celestial[body].draw(WIN)

            pre_factor =  4.5 * 1e1
            moon = Satellite(x=1 * (
                        pre_factor * PLANET_DATA['Moon']['Distance from Sun in 10^6 km'] * 1000 + celestial['earth'].x),
                             y=(pre_factor* PLANET_DATA['Moon']['Distance from Sun in 10^6 km'] * 1000 + celestial['earth'].y),
                             radius=(0.5 * PLANET_DATA['Moon']['Diameter in km'] * 1000),
                             mass=PLANET_DATA['Moon']['Mass in kg'],
                             color=(230, 230, 255),
                             name='Moon')

            # Initial y velocity of the Moon
            moon.y_velocity = -1 * 1000 + earth.y_velocity

            moon.update_position(planets)
            moon.draw_orbit(WIN)
            moon.draw(WIN)


            hubble.update_position(planets)
            hubble.draw_orbit(WIN)
            hubble.draw(WIN)



        WIN.blit(font1.render("Satellite current position: " + str((np.round(hubble.x, 2), np.round(hubble.y, 2))) + " km",
                              True, "White"), (90, 70))
        WIN.blit(
            font1.render("Satellite current velocity: " + str((np.round(hubble.x_velocity, 2), np.round(hubble.y_velocity, 2))) + " km",
                         True, "White"), (90, 50))

        WIN.blit(
            font1.render("Target orbital reached: " + str(hubble.TARGET_ACHIEVED),
                         True, "red"), (90, 30))

        hubble.get_the_perfect_angle_fire(celestial['mars'])
        WIN.blit(
            font1.render("Target Angle to start: " + str(hubble.TARGET_ANGLE),
                         True, "yellow"), (90, 90))

        pygame.draw.line(WIN, celestial['mars'].color,
                         (WIDTH / 2, HEIGHT * (2 / 3)),
                         (celestial['mars'].x * celestial['mars'].SCALE + WIDTH / 2 ,
                          celestial['mars'].y *celestial['mars'].SCALE + HEIGHT * (2 / 3)))



        # Update the window
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()