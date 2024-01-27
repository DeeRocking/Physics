import pygame
import math

class Planet:
    # Set up the astronomical constant as the main unit distance scale
    AU = 149.6e6  # In Kilometer
    AU = AU * 1000  # in meter
    # Gravitational constant
    G = 6.67428e-11
    # Set up a distance scale for simulation purpose
    SCALE = 170 / AU    # 1AU = 100 pixels
    # Set up a time step scale for simulation purpose
    TIMESTEP = 3600* 24     # 1 Day

    def __init__(self, x, y, radius, mass, color, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.name = name

        # Initialize the velocity of the planet
        self.x_velocity = 0
        self.y_velocity = 0

        # Initialize the distance from the sun
        self.distance_to_sun = 0

        # Initialize the orbit position of the planet
        self.orbit = []

    def draw(self, win):
        """
        Draws the planet on the screen
        :param win: Pygame window
        :return:
        """
        x = self.x * self.SCALE + win.get_width() / 2
        y = self.y * self.SCALE + win.get_height() * (2 / 3)


        # Draw the planet
        pygame.draw.circle(win,
                           self.color,
                           (x, y),
                           self.radius * self.SCALE * 1e4 * 0.35)

    def draw_orbit(self, win):
        # Draw the orbit as a line made of all the points in the trajectory
        if len(self.orbit) > 2 :
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + win.get_width() / 2
                y = y * self.SCALE + win.get_height() * (2 / 3)
                updated_points.append((x, y))

            star_x, star_y = self.orbit[0]
            current_x, current_y = self.orbit[-1]
            distance = math.sqrt((star_x - current_x) ** 2 + (star_y - current_y) ** 2)


            if len(updated_points) >=  50 :
                l = len(updated_points)
                pygame.draw.lines(win, (0, 0, 0), False, updated_points[:int(0.50 * l) - 1], 5)
                pygame.draw.lines(win, self.color, False, updated_points[int(0.50 * l):], 1)

            else:
                pygame.draw.lines(win, self.color, False, updated_points, 1)
    def attraction(self, other_body):
        """
        Calculates the gravitational attraction between the current planet and a second body
        :param other_body:
        :return: x and y components of the attraction force (fx, fy)
        """
        other_body_x, other_body_y = other_body.x, other_body.y

        # First we calculate the distance between the two bodies
        distance_x = (other_body_x - self.x)
        distance_y = (other_body_y - self.y)

        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other_body.name == 'sun':
            self.distance_to_sun = distance

        # Second we calculate the two component of the Gravitational force
        force_modulus = self.G * (self.mass * other_body.mass) / (distance ** 2)
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force_modulus
        force_y = math.sin(theta) * force_modulus

        return force_x, force_y

    def update_position(self, celestial_bodies):
        # 1. We first calculates the total force exerted on the current planet by all the universe
        total_fx = total_fy = 0
        for body in celestial_bodies:
            if self == body:
                continue

            fx, fy = self.attraction(body)
            total_fx += fx
            total_fy += fy

        # 2. Update the velocity
        self.x_velocity += (total_fx / self.mass) * self.TIMESTEP
        self.y_velocity += (total_fy / self.mass) * self.TIMESTEP

        # 3. Update the position
        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP

        # 4. Set up the trajectory
        self.orbit.append((self.x, self.y))
