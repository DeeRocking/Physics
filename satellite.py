import pygame
import math
from planet import Planet
import numpy as np

class Satellite(Planet):
    def __init__(self, x, y, radius, mass, color, name):
        super().__init__(x, y, radius, mass, color, name)
        self.SCALE = 170 / self.AU
        self.TIMESTEP = 3600 * 6
        self.TARGET_ACHIEVED = False
        self.TARGET_ANGLE = 0

    def draw_orbit(self, win):
        # Draw the orbit as a line made of all the points in the trajectory
        if len(self.orbit) > 2 :
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + win.get_width() / 2
                y = y * self.SCALE + win.get_height() * (2 / 3)
                updated_points.append((x, y))


            pygame.draw.lines(win, self.color, False, updated_points, 2)
            pygame.draw.line(win, self.color,
                             (win.get_width() / 2, win.get_height() * (2 / 3)), (x, y))
            # pygame.draw.line(win, (0, 255, 0),
            #                  (x, y), ((self.x_velocity / (self.x_velocity **2 + self.y_velocity**2) * self.SCALE) ,
            #                           (self.y_velocity/ (self.x_velocity **2 + self.y_velocity**2) * self.SCALE)))




    def angle(self, target_planet):

        #find the angle between two bodies

        dot_prod = self.x * target_planet.x + self.y * target_planet.y

        vect_magnitude = math.sqrt(self.x**2 + self.y**2) * math.sqrt(target_planet.x**2 + target_planet.y**2)

        cos_angle = dot_prod/vect_magnitude

        angle_in_deg = math.degrees(math.acos(cos_angle))
        #print(angleDeg)
        return angle_in_deg

    def calculate_delta_v1(self, r1, r2, m_sun):
        delta_v1 = math.sqrt((self.G * m_sun / r1)) * ((math.sqrt((2 * r2) / (r1 + r2))) - 1)
        return delta_v1

    def calculate_delta_v2(self, r1, r2, m_sun):
        delta_v2 =  math.sqrt((self.G * m_sun / r2)) * ((math.sqrt((2 * r1) / (r1 + r2))) - 1)
        return delta_v2

    def hohmann_transfert(self, target_planet: Planet, sun_mass=1.98892 * 10**30):
        # Calculate the respective distances of the satellite and the target planet from the sun
        r1 = math.sqrt((self.x**2 + self.y**2))
        r2 = math.sqrt(target_planet.x**2 + target_planet.y**2)

        # Calculate the required velocities changes for the elliptical transfers
        delta_v1 = self.calculate_delta_v1(r1, r2, sun_mass)
        delta_v2 = self.calculate_delta_v2(r1, r2, sun_mass)

        return delta_v1, delta_v2

    def angular_velocity(self, distance, sun_mass=1.98892 * 10 ** 30):
        return math.sqrt(self.G * sun_mass /distance)

    def get_the_perfect_angle_fire(self, target_planet: Planet):
        r1 = math.sqrt((self.x**2 + self.y**2))
        r2 = math.sqrt(target_planet.x**2 + target_planet.y**2)
        mars_time = kepler_3rd_law(r1, r2)
        mars_period = kepler_3rd_law(r2, r2)
        angle_needed = find_launch(mars_time, mars_period)
        self.TARGET_ANGLE = angle_needed

    def satellite_burn_event(self, target_planet: Planet, win):

        r1 = math.sqrt((self.x**2 + self.y**2))
        r2 = math.sqrt(target_planet.x**2 + target_planet.y**2)

        # Get the best time to go to Mars from Earth
        mars_time = kepler_3rd_law(r1, r2)
        mars_period = kepler_3rd_law(r2, r2)
        angle_needed = find_launch(mars_time, mars_period)


        angle_error_bound = 0.01
        error_bound = (0.01 * self.AU) / self.SCALE

        satellite_start_orbital_velocity = self.angular_velocity(r1)
        satellite_end_orbital_velocity = self.angular_velocity(r2)

        current_angle = self.angle(target_planet)
        s_factor = 1
        if angle_needed - error_bound <= current_angle <= angle_needed + error_bound:
            delta_v, _ = self.hohmann_transfert(target_planet)
            initial_velocity = self.x_velocity
            self.x_velocity = satellite_start_orbital_velocity  - delta_v * s_factor
            # self.y_velocity = satellite_start_orbital_velocity - delta_v * s_factor

            l = ["***************************"]
            print(f"{l[0] * 10}")
            print(f"The trip to {target_planet.name} stated!")
            print(f"Burn 1 started, initial velocity : {initial_velocity}, added velocity: {delta_v}, total velocity: {self.x_velocity}!")
            print(f"{l[0] * 10}")

            print(f"Angle diff  {abs(current_angle - angle_needed)}")

            if r2 - error_bound <= r1 <= r2 + error_bound:

                # _, delta_v = self.hohmann_transfert(target_planet)
                v2 = satellite_end_orbital_velocity
                v_a = self.x_velocity
                delta_v = v_a - v2
                self.x_velocity -= delta_v
                # self.y_velocity += delta_v
            #
            #     l = ["***************************"]
            #     print(f"{l[0] * 10}")
            #     print(f"The trip to {target_planet.name} stated!")
            #     print(f"Burn 2 started, added velocity: {delta_v}, total velocity: {self.x_velocity}!")
            #     print(f"{l[0] * 10}")
            # if (self.x_velocity**2 + self.y_velocity**2) == satellite_start_orbital_velocity:
            #     print(f"{target_planet.name} orbital velocity {satellite_start_orbital_velocity}")
            #     print(f"{self.name} orbital velocity {(self.x_velocity**2 + self.y_velocity**2)}")
            #     self.TARGET_ACHIEVED = True






def kepler_3rd_law(r1, r2):
    a = (r1 + r2) / 2
    # Period of full ellipse in 1 year
    p = math.sqrt(a**3) * 12
    return p

def find_launch(T, p):
    angle_for_launch = (-1 * (360 * (T / 12) / (p / 12) - 180))
    return min(abs(angle_for_launch), 360)

