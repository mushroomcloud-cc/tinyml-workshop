import socket
import struct

from OpenGL import GLUT, GLU, GL

from PerformanceCounter import PerformanceCounter


raw_data = []


AxisColor = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
BarScale = [0.00005, 0.00005, 0.00005, 0.00005, 0.00005, 0.00005, 0.0015, 0.0015, 0.0015]

class UdpServer:
    def __init__(self):
        self.Counter = PerformanceCounter()

        self.Server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.Server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536 * 16)
        self.Server.bind(("192.168.10.13", 8000))
        
    def Run(self):
        GLUT.glutInit()
        GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGBA)
        GLUT.glutInitWindowSize(600, 600)
        GLUT.glutCreateWindow("3D")
        GLUT.glutDisplayFunc(self.Draw)
        GLUT.glutIdleFunc(self.Recv)

        GLUT.glutMainLoop()


    def Recv(self):
        raw_data = [0]*9
        delta = 0
        raw_count = 0

        try:
            data, address = self.Server.recvfrom(44)

            #print(len(data), data)
            reader = lambda p: int.from_bytes(data[p:p + 2], byteorder="little", signed=True)



            for i in range(9):
               raw_data[i]  = reader(i * 2)
            '''
            q0 = struct.unpack("f", data[20:24])[0]
            q1 = struct.unpack("f", data[24:28])[0]        
            q2 = struct.unpack("f", data[28:32])[0]
            q3 = struct.unpack("f", data[32:36])[0]
            '''
            #delta = struct.unpack("f", data[36:40])[0]
            #raw_count = int.from_bytes(data[40:44],  byteorder="little", signed=False)

        except Exception as e:
            raw_data = []
            print("error", e.args)

        # t =  count / (now_time - last_tick)
        [count, t] = self.Counter.Frame()
        #print(count, t, raw_data)

        self.Draw(raw_data)


    def Draw(self, data=None):
        glClear(GL_COLOR_BUFFER_BIT)

        '''
        glPushMatrix()
        glColor3f(1, 1, 1)
        #glRotate(180, 0, 0, 1)
        
        if q != None:
            v = q.getVector()
            angle = q.getAngle() * 180 / 3.14 * 2 # 四元数角 * 2

            glRotate(angle, v[0], v[2], v[1])

        glutWireTeapot(0.4)
        glPopMatrix()
        '''
        glBegin(GL_LINES)

        if data != None:
            for i in range(len(data)):
                x = i * 0.1 - 0.9
                y = 0.75 + data[i] / 4 * BarScale[i]
                c = AxisColor[i % 3]

                glColor3f(c[0], c[1], c[2])
                glVertex3f(x, 0.75, 0)
                glVertex3f(x, y, 0)

        glEnd()
        glFlush()


if __name__ == '__main__':
    Server = UdpServer()
    Server.Run() 