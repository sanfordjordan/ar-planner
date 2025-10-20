from datetime import datetime, timedelta
from Objects.boxesObject import Box


class Leg:
  def __init__(self, line):
    self.number = int(line[0])
    self.discipline = line[1]
    self.elevation = int(line[4]) if line[4] != '' else 0
    self.boxes = Box(line[5])
    self.kayakType = line[6]
    self.minTemp = 10
    self.maxTemp = 20
    self.startTime = datetime(2001, 6, 19, 0, 0)
    self.finishTime = datetime(2001, 6, 19, 0, 0)
    self.avgTime =  timedelta(hours=(float(line[2]) + float(line[3])) / 2)
    self.avgTemp = 0
    self.waterReq = 0
    self.sleepDuring = False
    self.food = []
    self.spareSJ = 0
    self.weather = None
    self.clothing = None
    self.gear = None
    self.TASteps = []
    self.batteries = 0
    self.chargeBikeTorch = False
    