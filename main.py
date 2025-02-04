# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "numpy",
#   "PyOpenGL",
#   "PyQt6",
# ]
# ///

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *  # Import GLU module to use gluPerspective
import numpy as np
import signal
# Fix the AttributeError by using the correct attribute for horizontal orientation
from PyQt6.QtCore import Qt



# Constants
NUM_CUBES = 1000
CAMERA_INITIAL_Z = 0.0  # Place the camera in the middle of the range of cube positions
POSITION_RANGE = 15.0
MIN_DISTANCE_FROM_CAMERA = 2.0  # Minimum distance from the camera
SPEED_MIN = 0.1
SPEED_MAX = 1.0
DIRECTION_RANGE = 1.0
LINE_WIDTH = 2.0
PERSPECTIVE_ANGLE = 45.0
PERSPECTIVE_NEAR = 1.0
PERSPECTIVE_FAR = 100.0
CUBE_SIZE = 0.5
EDGE_COLOR = (0.0, 0.0, 0.0)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CAMERA_ANGLE_SPEED = 0.1  # Camera angle speed as a constant

class GLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.num_cubes = NUM_CUBES
        self.cube_positions = self.generate_random_positions(self.num_cubes)
        self.cube_colors = self.generate_random_colors(self.num_cubes)
        self.cube_angles = np.zeros(self.num_cubes)
        self.cube_speeds = self.generate_random_speeds(self.num_cubes)
        self.cube_directions = self.generate_random_directions(self.num_cubes)
        self.camera_angle = 0.0  # Initialize camera angle
        self.camera_angle_speed = CAMERA_ANGLE_SPEED

    def generate_random_positions(self, num_cubes):
        # Generate positions around the camera position (0, 0, CAMERA_INITIAL_Z)
        positions = np.random.uniform(-POSITION_RANGE, POSITION_RANGE, (num_cubes, 3))
        # Ensure cubes are not generated too close to the camera
        mask = np.linalg.norm(positions, axis=1) < MIN_DISTANCE_FROM_CAMERA
        while np.any(mask):
            positions[mask] = np.random.uniform(-POSITION_RANGE, POSITION_RANGE, (np.sum(mask), 3))
            mask = np.linalg.norm(positions, axis=1) < MIN_DISTANCE_FROM_CAMERA
        return positions + np.array([0.0, 0.0, CAMERA_INITIAL_Z])

    def generate_random_colors(self, num_cubes):
        return np.random.rand(num_cubes, 3)

    def generate_random_speeds(self, num_cubes):
        return np.random.uniform(SPEED_MIN, SPEED_MAX, num_cubes)

    def generate_random_directions(self, num_cubes):
        return np.random.uniform(-DIRECTION_RANGE, DIRECTION_RANGE, (num_cubes, 3))

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glLineWidth(LINE_WIDTH)  # Set the line width to LINE_WIDTH for a thicker stroke

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(PERSPECTIVE_ANGLE, w / h, PERSPECTIVE_NEAR, PERSPECTIVE_FAR)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Rotate the camera around the scene
        self.camera_angle += self.camera_angle_speed  # Use the variable for camera angle speed
        glRotatef(self.camera_angle, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.0, CAMERA_INITIAL_Z)

        self.cube_angles += self.cube_speeds  # Increment the rotation angle for each cube

        for i, (x, y, z) in enumerate(self.cube_positions):
            glPushMatrix()
            glTranslatef(x, y, z)
            glRotatef(self.cube_angles[i], *self.cube_directions[i])
            glColor3f(*self.cube_colors[i])
            self.drawBox()
            glPopMatrix()

        self.update()

    def drawBox(self):
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        # Back face
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        # Top face
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        # Bottom face
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        # Right face
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        # Left face
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glEnd()

        # Draw edges
        glColor3f(*EDGE_COLOR)  # Set edge color to black
        glBegin(GL_LINES)
        # Front face edges
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        # Back face edges
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        # Connecting edges
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        glVertex3f(-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE)
        glEnd()

    def set_camera_angle_speed(self, speed):
        self.camera_angle_speed = speed / 100.0  # Adjust speed based on slider value

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle("Cube Field")

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    glWidget = GLWidget()
    layout.addWidget(glWidget)

    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(1, 100)
    slider.setValue(int(CAMERA_ANGLE_SPEED * 100))
    slider.valueChanged.connect(glWidget.set_camera_angle_speed)
    layout.addWidget(slider)

    window.setCentralWidget(central_widget)
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.show()
    app.exec()
