from asyncio.windows_events import NULL
import socket
from unittest import skip
from PerformanceCounter import PerformanceCounter
from SensorChart import SensorChart
from DataFile import DataFile

class UdpServer:
    def __init__(self):
        self.Sample = []
        self.Data = []
        self.Idle = True
        self.SampleCount = 0

        self.Counter = PerformanceCounter()
        self.Chart = SensorChart()
        self.DataFile = DataFile()

        self.Server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.Server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536 * 16)
        self.Server.settimeout(0.5)

        ip = self.GetLocalIP("192.168.10")
        print(ip)
        self.Server.bind((ip, 8000)) 


    def Run(self):
        self.Chart.Run(self.Recv) 
        self.DataFile = NULL


    def Recv(self):
        self.Data = [0] * 9

        try:
            data, address = self.Server.recvfrom(40)

            #print(len(data), data)
            reader = lambda p: int.from_bytes(data[p:p + 4], byteorder="little", signed=True)

            c = reader(0)    
            for i in range(9):
               self.Data[i]  = reader((i + 1) * 4)
            
            if self.Idle: 
                self.Sample = []
                self.Idle = False

            while self.AddData(c, self.Data[:]) < c:
                continue 


        except socket.timeout:
            if not self.Idle:
                if len(self.Sample) == 120:
                    self.SampleCount += 1
                    for d in self.Sample:
                        self.DataFile.Write(d)
                else:
                    self.Sample = []
                    
                print("Sample: ", self.SampleCount)

            self.DataFile.Close()
            self.Counter.Reset()
            self.Idle = True

        except Exception as e:
            self.Data = []
            print("error", e.args)


    def AddData(self, c, d):
            self.Sample.append(d)

            [count, t] = self.Counter.Frame()
            print(count, int(t * 1000), c, d)

            self.Chart.Draw(d, self.Sample)

            return count


    def GetLocalIP(self, mask):
        host_name = socket.gethostname()
        ips = socket.gethostbyname_ex(host_name)[2]

        for ip in ips:
            if ip.startswith(mask):
                ret = ip    

        return ret       



if __name__ == '__main__':
    Server = UdpServer()
    Server.Run()
