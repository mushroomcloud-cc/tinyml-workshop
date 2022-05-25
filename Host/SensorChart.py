

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


    def Draw(self, data=None, data_his=None):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glBegin(GL.GL_LINES)

        YScale = lambda y: y / 5 * 0.00001 

        # Draw Bars
        if data != None:
            for i in range(len(data)):
                x = i * 0.1 - 0.9
                y = 0.75 + YScale(data[i])
                c = AxisColor[i % 3]

                GL.glColor3f(c[0], c[1], c[2])
                GL.glVertex3f(x, 0.75, 0)
                GL.glVertex3f(x, y, 0)

        # Draw Curves
        if data_his != None and len(data_his) > 0:
            size = len(data_his)
            for i in range(6):
                c = AxisColor[i % 3]
                y0 = 0.1 if i > 2 else -0.6
                GL.glColor3f(c[0], c[1], c[2])
                    
                px = -1
                py = y0 + YScale(data_his[0][i])   
                for k in range(size - 1):
                    x = -1 + (k + 1) *  2 / 120
                    y =  y0 + YScale(data_his[k + 1][i])
                    GL.glVertex3f(px, py, 0)
                    GL.glVertex3f(x, y, 0)
                    px = x
                    py = y


        GL.glEnd()
        GL.glFlush()