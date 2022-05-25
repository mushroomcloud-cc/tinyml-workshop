

from OpenGL import GLUT, GLU, GL

AxisColor = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
BarScale = [0.00005, 0.00005, 0.00005, 0.00005, 0.00005, 0.00005, 0.0015, 0.0015, 0.0015]

class SensorChart:
    def __init__(self):
        GLUT.glutInit()
        GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGBA)
        GLUT.glutInitWindowSize(600, 600)
        GLUT.glutCreateWindow("3D")


    def Run(self, proc):
        GLUT.glutDisplayFunc(self.Draw)
        GLUT.glutIdleFunc(proc)

        GLUT.glutMainLoop()


    def Draw(self, data=None):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBegin(GL.GL_LINES)

        if data != None:
            for i in range(len(data)):
                x = i * 0.1 - 0.9
                y = 0.75 + data[i] / 4 * 0.00001
                c = AxisColor[i % 3]

                GL.glColor3f(c[0], c[1], c[2])
                GL.glVertex3f(x, 0.75, 0)
                GL.glVertex3f(x, y, 0)

        GL.glEnd()
        GL.glFlush()