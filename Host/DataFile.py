import sys
import os

class DataFile:
    def __init__(self):
        self.File = None
        self.BasePath = os.path.dirname(__file__)


    def __del__(self):
        self.Close()


    def Write(self, data):
        if self.File == None:
            self.Open()

        if len(data) >= 6:
            for i in range(6):
                if i > 0: self.File.write("\t")
                self.File.write(str(data[i]))

            self.File.write("\n")   


    def Open(self):       
        self.File = None
        self.File = open(self.BasePath + "/data/data.csv", "a+")


    def Close(self):
        if self.File != None:
            self.File.flush()
            self.File.close()

        self.File = None

    