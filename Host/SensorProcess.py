##

from asyncio.windows_events import NULL
import socket
from PerformanceCounter import PerformanceCounter
from SensorChart import SensorChart
from DataFile import DataFile

raw_data = []

class UdpServer:
    def __init__(self):
        self.Counter = PerformanceCounter()
        self.Chart = SensorChart()
        self.DataFile = DataFile()

        self.Server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.Server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536 * 16)
        self.Server.settimeout(1)

        ip = self.GetLocalIP("192.168.10")
        print(ip)
        self.Server.bind((ip, 8000)) 


    def Run(self):
        self.Chart.Run(self.Recv) 
        self.DataFile = NULL


    def Recv(self):
        raw_data = [0] * 9

        try:
            data, address = self.Server.recvfrom(36)

            #print(len(data), data)
            reader = lambda p: int.from_bytes(data[p:p + 4], byteorder="little", signed=True)

            for i in range(9):
               raw_data[i]  = reader(i * 4)

        except socket.timeout:
            raw_data = []
            self.DataFile.Close()

        except Exception as e:
            raw_data = []
            print("error", e.args)

        [count, t] = self.Counter.Frame()
        print(count, t, raw_data)

        self.DataFile.Write(raw_data)
        self.Chart.Draw(raw_data)


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
