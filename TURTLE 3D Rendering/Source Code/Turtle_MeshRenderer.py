"""
Made by: Gaurav Shukla
19-04-2024

Letters WAD correspond to the cube's rotation in the  X Y or Z axis so pressing these buttons let u alter them as described.
I did use lots of tutorials to get this to kind of work :/
I am aware there is overlap due to lack of z indexing however i could not get those solutions working.
Features:
- ultra high speed rendering
- polygon filler
- mesh projector
- camera
- textures
- anti-overlap strats for example face sorting
- shaders (ultra simple dulling based on distance)
** i also know this looks off due to the highlights travelling to opposite sides however this models the light source to be the face itself closest to the camera.

CUBE POINT LOGIC :
    7-------6
   /|      /|
  4-------5 |
  | |     | |
  | 3-----|-2
  |/      |/
  0-------1

"""
import math
import time
import turtle
from turtle import Turtle

class Renderer(Turtle):
    def __init__(self, screen, keymap=None):
        super(Renderer, self).__init__()
        if keymap is None: self.keymap = ["w", "a", "d"]
        self.color("blue", "green")  # Set the pen color and fill color

        # Set the turtle speed to the fastest
        self.speed(0)
        # Screen
        self.screen = screen
        # Turn off the animation
        turtle.tracer(False)

        # Camera parameters (adjust as needed)
        self.focal_length = 500  # Focal length (distance from camera to projection plane)

        # Rotation angles
        self.x_angle = 0
        self.y_angle = 0
        self.z_angle = 0

    # Function to update rotation

    def rotate_x(self):
        self.x_angle = (self.x_angle + 10) % 360

    def rotate_y(self):
        self.y_angle = (self.y_angle + 10) % 360

    def rotate_z(self):
        self.z_angle = (self.z_angle + 10) % 360

    # Rotation matrices

    @staticmethod
    def x_rotation_matrix(angle):
        rad = math.radians(angle)
        return [
            [1, 0, 0],
            [0, math.cos(rad), -math.sin(rad)],
            [0, math.sin(rad), math.cos(rad)]
        ]

    @staticmethod
    def y_rotation_matrix(angle):
        rad = math.radians(angle)
        return [
            [math.cos(rad), 0, math.sin(rad)],
            [0, 1, 0],
            [-math.sin(rad), 0, math.cos(rad)]
        ]

    @staticmethod
    def z_rotation_matrix(angle):
        rad = math.radians(angle)
        return [
            [math.cos(rad), -math.sin(rad), 0],
            [math.sin(rad), math.cos(rad), 0],
            [0, 0, 1]
        ]

    # Function to apply rotation to a point

    def apply_rotation(self, point, x_angle, y_angle, z_angle):
        x_rotated = self.multiply_matrix_vector(self.x_rotation_matrix(x_angle), point)
        y_rotated = self.multiply_matrix_vector(self.y_rotation_matrix(y_angle), x_rotated)
        z_rotated = self.multiply_matrix_vector(self.z_rotation_matrix(z_angle), y_rotated)
        return z_rotated

    # Function to multiply matrix and vector

    @staticmethod
    def multiply_matrix_vector(matrix, vector):
        return [
            sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3)
        ]

    # Perspective projection function

    def project_to_screen(self, point_3d):
        x, y, z = point_3d
        x_proj = x * self.focal_length / (z + self.focal_length)
        y_proj = y * self.focal_length / (z + self.focal_length)
        return x_proj, y_proj

    # Function to draw a filled polygon

    def draw_filled_polygon(self, points):
        self.begin_fill()
        for point in points:
            x_proj, y_proj = self.project_to_screen(point)
            self.goto(x_proj, y_proj)
        self.end_fill()

    # Function to draw the cube

    def draw_cube(self, mesh):
        self.clear()
        rotated_points = [self.apply_rotation(point, self.x_angle, self.y_angle, self.z_angle) for point in mesh["vertex"]]
        # Sort faces by average Z value (distance from the viewer)
        faces = [([rotated_points[i] for i in face], sum(rotated_points[i][2] for i in face)) for face in mesh["faces"]]
        faces.sort(key=lambda x: x[1], reverse=True)  # Sort faces by distance
        # Draw and fill the sides
        #base = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
        base = [0, 1, 0]
        # Draw each face
        i = 5
        self.screen.colormode(255)
        for face, _ in faces:
            self.fillcolor(round((base[0] * (255 / (i + 1)))), round((base[1] * (255 / (i + 1)))),
                           round((base[2] * (255 / (i + 1)))))
            self.draw_filled_polygon(face)
            i -= 1

    def render(self, mesh):
        # Initial drawing of the cube
        self.screen.onkeypress(self.rotate_x, self.keymap[0])
        self.screen.onkeypress(self.rotate_y, self.keymap[1])
        self.screen.onkeypress(self.rotate_z, self.keymap[2])
        self.screen.listen()
        while True:
            self.z_angle += 0.1
            self.x_angle += 0.1
            self.y_angle += 0.1
            self.draw_cube(mesh)
            self.hideturtle()
            turtle.update()


if __name__ == "__main__":
    # Set up the screen
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("3D Cube Projection :)")

    mesh = {
        "faces":
            [
             [0, 1, 2, 3],  # Front face
             [4, 5, 6, 7],  # Back face
             [0, 1, 5, 4],  # Right face
             [2, 3, 7, 6],  # Left face
             [0, 3, 7, 4],  # Top face
             [1, 2, 6, 5]   # Bottom face
            ],
        "vertex":
            [
                (100, 100, 100),  # Vertex A
                (100, -100, 100),  # Vertex B
                (-100, -100, 100),  # Vertex C
                (-100, 100, 100),  # Vertex D
                (100, 100, -100),  # Vertex E
                (100, -100, -100),  # Vertex F
                (-100, -100, -100),  # Vertex G
                (-100, 100, -100),  # Vertex H
            ],
        "textures":
            [
                ['C:/Users/gs030/Downloads/backdrop1.png', ["faces"]],
            ]
    }

    renderer = Renderer(screen)
    renderer.render(mesh)