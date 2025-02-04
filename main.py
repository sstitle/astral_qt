# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "flickrapi",
#   "PyQt6",
#   "numpy",
#   "PyOpenGL",
# ]
# ///

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *  # Import GLU module to use gluPerspective
import numpy as np

class GLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.num_cubes = 10
        self.cube_positions = self.generate_random_positions(self.num_cubes)
        self.cube_colors = self.generate_random_colors(self.num_cubes)
        self.cube_angles = np.zeros(self.num_cubes)
        self.cube_speeds = self.generate_random_speeds(self.num_cubes)
        self.cube_directions = self.generate_random_directions(self.num_cubes)

    def generate_random_positions(self, num_cubes):
        return np.random.uniform(-5.0, 5.0, (num_cubes, 3))

    def generate_random_colors(self, num_cubes):
        return np.random.rand(num_cubes, 3)

    def generate_random_speeds(self, num_cubes):
        return np.random.uniform(0.1, 1.0, num_cubes)

    def generate_random_directions(self, num_cubes):
        return np.random.uniform(-1.0, 1.0, (num_cubes, 3))

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / h, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10.0)

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
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Back face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        # Top face
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        # Bottom face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        # Right face
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        # Left face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glEnd()

        # Draw edges
        glColor3f(0.0, 0.0, 0.0)  # Set edge color to black
        glBegin(GL_LINES)
        # Front face edges
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        # Back face edges
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        # Connecting edges
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glEnd()

if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    glWidget = GLWidget()
    window.setCentralWidget(glWidget)
    window.resize(800, 600)
    window.show()
    app.exec()
