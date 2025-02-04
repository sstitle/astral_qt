# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "flickrapi",
#   "PyQt6",
#   "PyOpenGL",
# ]
# ///

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *

class GLWidget(QOpenGLWidget):
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(1.0, -1.0, 0.0)
        glEnd()

app = QApplication([])
window = QMainWindow()
glWidget = GLWidget()
window.setCentralWidget(glWidget)
window.resize(800, 600)
window.show()
app.exec()
