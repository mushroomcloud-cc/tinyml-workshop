import sys
import os

class DataFile:
    def __init__(self):
        base_path = os.path.dirname(__file__)

        self.File = None
        self.File = open( base_path + "/data/data.csv", "a+")


    def __del__(self):
        if self.File != None:
            self.File.flush()
            self.File.close()


    def Write(self, data):
        if len(data) >= 6:
            for i in range(6):
                if i > 0: self.File.write("\t")
                self.File.write(str(data[i]))

            self.File.write("\n")   


    